#!/usr/bin/env python3
from fractions import Fraction as F
import sys,time,math,json,argparse
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import vstack,lil_matrix
sys.path.insert(0,'/mnt/data/erdos2275')
import state2275_tower_heavy_bbmst_v3 as base
import state2275_hn_milp as s
P=(3,5,7,11);R=s.R;N=len(R)

def qres(m,es):
 q=1
 for i,e in zip(s.bits(m),es): q*=P[i]**(e-1)
 return q

def maxforest(nodes):
 # nodes entries (jvar,q,w,m,h); choose max-weight forest among coprime residual moduli
 edges=[]
 for a in range(len(nodes)):
  for b in range(a+1,len(nodes)):
   qa,qb=nodes[a][1],nodes[b][1]
   if math.gcd(qa,qb)==1:
    edges.append((F(1,qa*qb),a,b))
 edges.sort(reverse=True,key=lambda z:z[0]); par=list(range(len(nodes)))
 def find(x):
  while par[x]!=x:
   par[x]=par[par[x]];x=par[x]
  return x
 out=[]
 for w,a,b in edges:
  x,y=find(a),find(b)
  if x!=y: par[x]=y;out.append((w,a,b))
 return out

def build_context(cut=.02, maximize_exhaustion=True):
 z=base.build(cut)
 if z is None:return None
 c,ii,bd,con,meta=z
 # Objective helps HiGHS find a structured incumbent instead of arbitrary feasibility point.
 if maximize_exhaustion:
  c=np.zeros_like(c)
  for j in meta['eidx'].values(): c[j]=-1.0
 A0=con.A;lo0=con.lb;hi0=con.ub
 cand={aidx:[] for aidx in range(N)}
 for (m,h,v),j in meta['xidx'].items():
  es,w=meta['hv'][m][h];q=qres(m,es);I=s.bits(m)
  for aidx,a in enumerate(R):
   if tuple(a[i] for i in I)==v:cand[aidx].append((j,q,w,m,h))
 tailvars={aidx:[] for aidx in range(N)}
 for (m,v),j in meta['tidx'].items():
  I=s.bits(m)
  for aidx,a in enumerate(R):
   if tuple(a[i] for i in I)==v:tailvars[aidx].append(j)
 return c,ii,bd,A0,lo0,hi0,meta,cand,tailvars

def make_cut(aidx, active_nodes, all_nodes, tail_ids, meta):
 forest=maxforest(active_nodes)
 # GLOBAL valid Hunter cut:
 # e <= sum_{ALL incident heavy i} w_i x_i + sum tail
 #      - sum_{edge uv in incumbent forest} w_uv (x_u+x_v-1)
 # Forest remains a forest on whatever subset is later active; singleton terms for all
 # potential classes ensure newly activated classes are paid for.
 d={meta['eidx'][aidx]:1.0}
 for j,q,w,m,h in all_nodes:
  d[j]=d.get(j,0)-float(w)
 for j in tail_ids:d[j]=d.get(j,0)-1.0
 rhs=0.0
 for wij,u,v in forest:
  ju=active_nodes[u][0];jv=active_nodes[v][0];ww=float(wij)
  rhs+=ww;d[ju]=d.get(ju,0)+ww;d[jv]=d.get(jv,0)+ww
 return d,rhs,forest

def hunter_cap(active_nodes, tailmass):
 forest=maxforest(active_nodes)
 return sum((q[2] for q in active_nodes),F(0))-sum((e[0] for e in forest),F(0))+F(str(tailmass)),forest

def solve_with_cuts(ctx,cuts,tlim):
 c,ii,bd,A0,lo0,hi0,meta,cand,tailvars=ctx
 if cuts:
  C=lil_matrix((len(cuts),len(c)));chi=np.empty(len(cuts))
  for rr,(d,rhs) in enumerate(cuts):
   for j,v in d.items():C[rr,j]=v
   chi[rr]=rhs
  A=vstack([A0,C.tocsr()],format='csr'); lo=np.r_[lo0,np.full(len(cuts),-np.inf)]; hi=np.r_[hi0,chi]
 else:A=A0;lo=lo0;hi=hi0
 return milp(c,integrality=ii,bounds=bd,constraints=LinearConstraint(A,lo,hi),
             options={'time_limit':tlim,'mip_rel_gap':0,'presolve':True})

def run(cut=.02,maxit=30,tlim=60,total=600,out=None):
 ctx=build_context(cut,True)
 if ctx is None:return {'status':'preinf'}
 c,ii,bd,A0,lo0,hi0,meta,cand,tailvars=ctx
 cuts=[];seen=set();records=[];st0=time.time();last_witness=None
 print('MODEL cut',cut,'vars',len(c),'binary',int(ii.sum()),'base_rows',A0.shape[0],flush=True)
 for it in range(maxit):
  if time.time()-st0>total:break
  rem=max(1,min(tlim,total-(time.time()-st0)))
  st=time.time();r=solve_with_cuts(ctx,cuts,rem);sec=time.time()-st
  print('iter',it,'status',r.status,r.message,'inc',r.x is not None,'sec',round(sec,3),'cuts',len(cuts),'obj',getattr(r,'fun',None),flush=True)
  if r.x is None:
   status='infeasible' if r.status==2 else 'unknown'
   res={'status':status,'iter':it,'cuts':len(cuts),'records':records,'elapsed':time.time()-st0}
   if out:open(out,'w').write(json.dumps(res,indent=2))
   return res
  ex=[a for a,j in meta['eidx'].items() if r.x[j]>.5]
  invalid=[];new=0;potential=[]
  for aidx in ex:
   active=[q for q in cand[aidx] if r.x[q[0]]>.5]
   tailmass=sum(r.x[j] for j in tailvars[aidx])
   cap,forest=hunter_cap(active,tailmass)
   if cap>=1-F(1,10**10): potential.append(aidx);continue
   invalid.append((aidx,float(cap),len(active),len(forest)))
   d,rhs,forest=make_cut(aidx,active,cand[aidx],tailvars[aidx],meta)
   key=(aidx,tuple(sorted((j,round(v,13)) for j,v in d.items() if abs(v)>1e-13)),round(rhs,13))
   if key not in seen:seen.add(key);cuts.append((d,rhs));new+=1
  rec={'it':it,'exhausted':len(ex),'potential':len(potential),'invalid':len(invalid),'newcuts':new,'sec':sec,
       'mincap':min((x[1] for x in invalid),default=1.0),'maxcap':max((x[1] for x in invalid),default=1.0),
       'objective':float(r.fun) if r.fun is not None else None}
  records.append(rec)
  print('  exhausted',len(ex),'Hunter-potential',len(potential),'invalid',len(invalid),'newcuts',new,
        'caprange',rec['mincap'],rec['maxcap'],flush=True)
  last_witness={'exhausted':ex,'potential':potential}
  if not invalid:
   res={'status':'hunter_feasible_bad','iter':it,'cuts':len(cuts),'records':records,'elapsed':time.time()-st0,
        'exhausted':ex,'potential':potential}
   if out:open(out,'w').write(json.dumps(res,indent=2))
   return res
  if new==0:
   res={'status':'stalled','iter':it,'cuts':len(cuts),'records':records,'elapsed':time.time()-st0}
   if out:open(out,'w').write(json.dumps(res,indent=2))
   return res
 res={'status':'limit','iters':len(records),'cuts':len(cuts),'records':records,'elapsed':time.time()-st0,'last':last_witness}
 if out:open(out,'w').write(json.dumps(res,indent=2))
 return res

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--cut',type=float,default=.02);ap.add_argument('--maxit',type=int,default=30);ap.add_argument('--time',type=float,default=60);ap.add_argument('--total',type=float,default=600);ap.add_argument('--out');a=ap.parse_args()
 z=run(a.cut,a.maxit,a.time,a.total,a.out);print('RESULT',json.dumps(z,indent=2))
