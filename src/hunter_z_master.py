#!/usr/bin/env python3
import sys,json,time,argparse,math
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import lil_matrix,vstack,hstack,csr_matrix
sys.path.insert(0,'/mnt/data/erdos2275')
import state2275_hunter_benders_v2 as hb
from fractions import Fraction as F
CUTLOG='/mnt/data/erdos2275/HUNTER_V2_CUTLOG.json'

def build():
 ctx=hb.build_context(.02,False)
 c0,ii0,bd0,A0,lo0,hi0,meta,cand,tailvars=ctx
 logs=json.load(open(CUTLOG))
 # q lookup per parent and x var
 qlookup={}
 wlookup={}
 for a,nodes in cand.items():
  for j,q,w,m,h in nodes:qlookup[a,j]=q;wlookup[a,j]=w
 forests=[];fseen=set();edgekeys=set()
 for sig in logs:
  a=sig['aidx']; aset=set(sig['active']);active=[q for q in cand[a] if q[0] in aset]
  ff=hb.maxforest(active); edges=[]
  for wij,u,v in ff:
   j1,j2=sorted((active[u][0],active[v][0]));key=(a,j1,j2);edgekeys.add(key);edges.append(key)
  fkey=(a,tuple(sorted(edges)))
  if fkey not in fseen:fseen.add(fkey);forests.append((a,tuple(sorted(edges))))
 edgekeys=sorted(edgekeys);zidx={e:len(c0)+k for k,e in enumerate(edgekeys)}
 n=len(c0)+len(edgekeys)
 c=np.zeros(n);ii=np.r_[ii0,np.zeros(len(edgekeys),dtype=int)]
 lb=np.r_[bd0.lb,np.zeros(len(edgekeys))];ub=np.r_[bd0.ub,np.ones(len(edgekeys))]
 # extend base A with zero cols
 A0e=hstack([A0,csr_matrix((A0.shape[0],len(edgekeys)))],format='csr')
 rows=[];los=[];his=[]
 def row(d,lo=-np.inf,hi=np.inf):rows.append(d);los.append(lo);his.append(hi)
 # AND envelope
 for (a,j1,j2),z in zidx.items():
  row({z:1,j1:-1},hi=0);row({z:1,j2:-1},hi=0);row({j1:1,j2:1,z:-1},hi=1)
 # exact z-Hunter forest inequalities
 for a,edges in forests:
  d={meta['eidx'][a]:1.0}
  for j,q,w,m,h in cand[a]:d[j]=d.get(j,0)-float(w)
  for j in tailvars[a]:d[j]=d.get(j,0)-1.0
  for e in edges:
   q1=qlookup[a,e[1]];q2=qlookup[a,e[2]]
   d[zidx[e]]=d.get(zidx[e],0)+1.0/(q1*q2)
  row(d,hi=0)
 C=lil_matrix((len(rows),n))
 for rr,d in enumerate(rows):
  for j,v in d.items():C[rr,j]=v
 A=vstack([A0e,C.tocsr()],format='csr');lo=np.r_[lo0,np.array(los)];hi=np.r_[hi0,np.array(his)]
 return c,ii,Bounds(lb,ub),LinearConstraint(A,lo,hi),meta,cand,tailvars,forests,zidx

def run(t=22,out=None):
 z=build();c,ii,b,con,meta,cand,tailvars,forests,zidx=z
 print('zmaster vars',len(c),'binary',int(ii.sum()),'rows',con.A.shape[0],'forests',len(forests),'zedges',len(zidx),flush=True)
 st=time.time();r=milp(c,integrality=ii,bounds=b,constraints=con,options={'time_limit':t,'mip_rel_gap':0,'presolve':True});sec=time.time()-st
 rec={'status':int(r.status),'message':r.message,'incumbent':r.x is not None,'sec':sec,'vars':len(c),'binary':int(ii.sum()),'rows':con.A.shape[0],'forests':len(forests),'zedges':len(zidx)}
 print(rec,flush=True)
 if r.x is not None:
  ex=[a for a,j in meta['eidx'].items() if r.x[j]>.5];bad=[];pot=[]
  for a in ex:
   active=[q for q in cand[a] if r.x[q[0]]>.5];tail=sum(r.x[j] for j in tailvars[a]);cap,f=hb.hunter_cap(active,tail)
   (pot if float(cap)>=1-1e-10 else bad).append((a,float(cap),len(active),len(f)))
  rec.update(exhausted=len(ex),potential=len(pot),invalid=len(bad),invalid_detail=bad,potential_detail=pot)
  print('ex',len(ex),'potential',len(pot),'invalid',len(bad),flush=True)
 if out:json.dump(rec,open(out,'w'),indent=2)
 return r,rec
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--time',type=float,default=22);ap.add_argument('--out');a=ap.parse_args();run(a.time,a.out)
