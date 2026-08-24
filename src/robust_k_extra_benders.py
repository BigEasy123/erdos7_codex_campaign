#!/usr/bin/env python3
import sys,time,json,pickle,os
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import lil_matrix
sys.path.insert(0,'/mnt/data/erdos2275')
import qonly_bbmst_benders_ck as q
import state2275_hn_milp as s
FT=q.FT;FC=q.FC;FZ=q.FZ;N=q.N;R=q.R;FUT=q.FUT
# q vars + extra z + total deleted h
names=[];lb=[];ub=[];ii=[]
def add(n,lo=0,hi=1,integer=True):
 j=len(names);names.append(n);lb.append(lo);ub.append(hi);ii.append(1 if integer else 0);return j
qidx={(m,tuple(v)):add(('q',m,tuple(v))) for m in FUT for v in s.Q[m]}
zidx={a:add(('z',a)) for a in range(N)}
hidx={a:add(('h',a)) for a in range(N)}
base=[]
def row(d,lo=-np.inf,hi=np.inf):base.append((d,lo,hi))
for m in FUT:row({j:1 for (mm,v),j in qidx.items() if mm==m},1,1)
# q comparability
for m in FUT:
 Im=s.bits(m)
 for n in FUT:
  if m>=n or (m&~n):continue
  In=s.bits(n)
  for (mm,v),jm in qidx.items():
   if mm!=m:continue
   for (nn,w),jn in qidx.items():
    if nn==n and s.restrict(w,In,Im)==v:row({jm:1,jn:1},hi=1)
# h exact OR of direct q hits and extra z
for a,x in enumerate(R):
 hits=[j for (m,v),j in qidx.items() if q.hit(x,m,v)]
 for j in hits: row({hidx[a]:1,j:-1},lo=0)
 row({hidx[a]:1,zidx[a]:-1},lo=0)
 d={hidx[a]:1,zidx[a]:-1}
 for j in hits:d[j]=d.get(j,0)-1
 row(d,hi=0)
 # no need waste z on direct deletion; enforce z + each hit <=1 to count genuinely extra only
 for j in hits: row({zidx[a]:1,j:1},hi=1)
# symmetry rows on q only, same safe restricted-growth
POS=[12,13,14,15]
for coord,D in [(2,6),(3,10)]:
 for k,m in enumerate(POS):
  I=s.bits(m);pos=I.index(coord)
  for r in range(4,D):
   d={}
   for (mm,v),j in qidx.items():
    if mm==m and v[pos]==r:d[j]=d.get(j,0)+1
   for mp in POS[:k]:
    Ip=s.bits(mp);pp=Ip.index(coord)
    for (mm,v),j in qidx.items():
     if mm==mp and v[pp]==r-1:d[j]=d.get(j,0)-1
   if d:row(d,hi=0)

def solve_master(cuts,k,tlim=10):
 rows=list(base)
 rows.append(({j:1 for j in zidx.values()},-np.inf,float(k)))
 for mu,delta in cuts:
  rows.append(({hidx[a]:float(mu[a]) for a in range(N) if mu[a]>1e-15},float(delta),np.inf))
 A=lil_matrix((len(rows),len(names)));lo=[];hi=[]
 for r,(d,l,h) in enumerate(rows):
  for j,v in d.items():A[r,j]=v
  lo.append(l);hi.append(h)
 return milp(np.zeros(len(names)),integrality=np.array(ii),bounds=Bounds(np.array(lb),np.array(ub)),constraints=LinearConstraint(A.tocsr(),np.array(lo),np.array(hi)),options={'time_limit':tlim,'mip_rel_gap':0,'presolve':True})

def run_k(k,maxit=100,total=120):
 ck=pickle.load(open('QONLY_BENDERS_FINISH_CK.pkl','rb')); cuts=list(ck['cuts'])
 seen=set();recs=[];maxF=-1;st=time.time()
 for it in range(maxit):
  rem=total-(time.time()-st)
  if rem<=0:break
  z=solve_master(cuts,k,min(12,max(2,rem)))
  print('k',k,'it',it,'status',z.status,'inc',z.x is not None,'cuts',len(cuts),'sec',time.time()-st,flush=True)
  if z.x is None:
   stat='closed' if z.status==2 else 'timeout'
   return {'k':k,'status':stat,'it':it,'cuts':len(cuts),'maxF':maxF,'records':recs,'elapsed':time.time()-st}
  sel=[(m,v) for (m,v),j in qidx.items() if z.x[j]>.5]
  extra=[a for a,j in zidx.items() if z.x[j]>.5]
  H=np.array([z.x[hidx[a]]>.5 for a in range(N)])
  sig=(tuple(sel),tuple(extra))
  if sig in seen:return {'k':k,'status':'repeat','it':it,'cuts':len(cuts),'maxF':maxF,'records':recs}
  seen.add(sig)
  surv=[a for a,d in zip(R,H) if not d]
  F,mu=q.Foracle(surv);maxF=max(maxF,F)
  rec={'it':it,'F':float(F),'survivors':len(surv),'extra_n':len(extra),'extra':[list(R[a]) for a in extra],'sel':[(m,list(v)) for m,v in sel]};recs.append(rec)
  print('  F',F,'surv',len(surv),'extra',len(extra),flush=True)
  if F>=FT-1e-9:
   return {'k':k,'status':'Fbad','F':float(F),'it':it,'cuts':len(cuts),'maxF':maxF,'record':rec,'records':recs,'elapsed':time.time()-st}
  full=np.zeros(N);kk=0
  for a,d in enumerate(H):
   if not d:full[a]=mu[kk];kk+=1
  delta=1-(F-FC)/FZ
  cuts.append((full,float(delta)+1e-10));rec['delta']=float(delta)
 return {'k':k,'status':'limit','cuts':len(cuts),'maxF':maxF,'records':recs,'elapsed':time.time()-st}

if __name__=='__main__':
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('k',type=int);ap.add_argument('--total',type=float,default=120);args=ap.parse_args()
 out=run_k(args.k,total=args.total);print(json.dumps({x:y for x,y in out.items() if x!='records'},indent=2));json.dump(out,open(f'ROBUST_K{args.k}_BENDERS.json','w'),indent=2)
