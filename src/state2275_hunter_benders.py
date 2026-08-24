#!/usr/bin/env python3
from fractions import Fraction as F
import sys,time,math,json,argparse
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import vstack,lil_matrix,csr_matrix
sys.path.insert(0,'/mnt/data/erdos2275')
import state2275_tower_heavy_bbmst_v3 as base
import state2275_hn_milp as s
P=(3,5,7,11);R=s.R;N=len(R)

def qres(m,es):
 q=1
 for i,e in zip(s.bits(m),es):q*=P[i]**(e-1)
 return q

def maxforest(nodes): # nodes=(jvar,q,w_density)
 edges=[]
 for a in range(len(nodes)):
  for b in range(a+1,len(nodes)):
   qa,qb=nodes[a][1],nodes[b][1]
   if math.gcd(qa,qb)==1:edges.append((F(1,qa*qb),a,b))
 edges.sort(reverse=True,key=lambda z:z[0]);par=list(range(len(nodes)))
 def find(x):
  while par[x]!=x:par[x]=par[par[x]];x=par[x]
  return x
 out=[]
 for w,a,b in edges:
  x,y=find(a),find(b)
  if x!=y:par[x]=y;out.append((w,a,b))
 return out

def run(cut=.02,maxit=12,tlim=25,total=110,out=None):
 z=base.build(cut)
 if z is None:return {'status':'preinf'}
 c,ii,bd,con,meta=z; A0=con.A;lo0=con.lb;hi0=con.ub
 # candidate info per atom
 cand={aidx:[] for aidx in range(N)}
 for (m,h,v),j in meta['xidx'].items():
  es,w=meta['hv'][m][h];q=qres(m,es)
  I=s.bits(m)
  # x var contributes to every atom in this shallow cylinder
  for aidx,a in enumerate(R):
   if tuple(a[i] for i in I)==v:cand[aidx].append((j,q,w,m,h))
 tailvars={aidx:[] for aidx in range(N)}
 for (m,v),j in meta['tidx'].items():
  I=s.bits(m)
  for aidx,a in enumerate(R):
   if tuple(a[i] for i in I)==v:tailvars[aidx].append(j)
 cuts=[];seen=set();records=[];st0=time.time()
 for it in range(maxit):
  if time.time()-st0>total:break
  if cuts:
   C=lil_matrix((len(cuts),len(c))) ; clo=[];chi=[]
   for rr,(d,rhs) in enumerate(cuts):
    for j,v in d.items():C[rr,j]=v
    clo.append(-np.inf);chi.append(rhs)
   A=vstack([A0,C.tocsr()],format='csr');lo=np.r_[lo0,np.array(clo)];hi=np.r_[hi0,np.array(chi)]
  else:A=A0;lo=lo0;hi=hi0
  st=time.time();r=milp(c,integrality=ii,bounds=bd,constraints=LinearConstraint(A,lo,hi),options={'time_limit':tlim,'mip_rel_gap':0,'presolve':True});sec=time.time()-st
  print('iter',it,'status',r.status,r.message,'inc',r.x is not None,'sec',sec,'cuts',len(cuts),flush=True)
  if r.x is None:
   status='infeasible' if r.status==2 else 'unknown';return {'status':status,'iter':it,'cuts':len(cuts),'records':records,'elapsed':time.time()-st0}
  ex=[a for a,j in meta['eidx'].items() if r.x[j]>.5]
  invalid=[];new=0;potential=[]
  for aidx in ex:
   nodes=[q for q in cand[aidx] if r.x[q[0]]>.5]
   forest=maxforest(nodes)
   sumw=sum((q[2] for q in nodes),F(0)); corr=sum((e[0] for e in forest),F(0));tail=sum((F(str(r.x[j])) for j in tailvars[aidx]),F(0))
   cap=sumw-corr+tail
   if cap>=1:potential.append(aidx);continue
   invalid.append((aidx,float(cap),len(nodes),len(forest)))
   # witness-specific forest linear Hunter cut, valid globally because active subset of a forest remains a forest.
   # e - sum w*x - tail + sum_edges wij*(x_i+x_j) <= sum_edges wij
   d={meta['eidx'][aidx]:1.0}
   for j,q,w,m,h in nodes:d[j]=d.get(j,0)-float(w)
   for j in tailvars[aidx]:d[j]=d.get(j,0)-1.0
   rhs=0.0
   for wij,u,v in forest:
    ju=nodes[u][0];jv=nodes[v][0];ww=float(wij);rhs+=ww;d[ju]=d.get(ju,0)+ww;d[jv]=d.get(jv,0)+ww
   # key rounded sparse signature
   key=(aidx,tuple(sorted((j,round(v,14)) for j,v in d.items() if abs(v)>1e-14)),round(rhs,14))
   if key not in seen:seen.add(key);cuts.append((d,rhs));new+=1
  rec={'it':it,'exhausted':len(ex),'potential':len(potential),'invalid':len(invalid),'newcuts':new,'sec':sec,'mincap':min((x[1] for x in invalid),default=1.0),'maxcap':max((x[1] for x in invalid),default=1.0)};records.append(rec)
  print('  exhausted',len(ex),'Hunter-potential',len(potential),'invalid',len(invalid),'newcuts',new,'caprange',rec['mincap'],rec['maxcap'],flush=True)
  if not invalid:
   return {'status':'hunter_feasible_bad','iter':it,'cuts':len(cuts),'records':records,'elapsed':time.time()-st0}
  if new==0:return {'status':'stalled','iter':it,'cuts':len(cuts),'records':records,'elapsed':time.time()-st0}
 res={'status':'limit','iters':len(records),'cuts':len(cuts),'records':records,'elapsed':time.time()-st0}
 if out:open(out,'w').write(json.dumps(res,indent=2))
 return res
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--cut',type=float,default=.02);ap.add_argument('--maxit',type=int,default=12);ap.add_argument('--time',type=float,default=25);ap.add_argument('--total',type=float,default=110);ap.add_argument('--out');a=ap.parse_args();z=run(a.cut,a.maxit,a.time,a.total,a.out);print('RESULT',json.dumps(z,indent=2));
 if a.out:open(a.out,'w').write(json.dumps(z,indent=2))
