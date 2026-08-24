#!/usr/bin/env python3
from itertools import product
import sys,time,numpy as np
from scipy.optimize import milp,LinearConstraint,Bounds
from scipy.sparse import lil_matrix
sys.path.insert(0,'/mnt/data/erdos2275')
import state2275_hn_milp as b
D=b.D;R=b.R;FUT=b.FUT;Q=b.Q;FIX=b.FIX
ALPHA=b.ALPHA;BETA=b.BETA;HRHS=b.HRHS;CONST=b.CONST;ZH=HRHS-CONST
bits=b.bits;osupp=b.osupp;restrict=b.restrict;subset=b.subset
# deep choices by t and T prefiltered against fixed shallow classes
X={}
for t in (1,2):
 for T in range(8):
  S=osupp(T);Sm=sum(1<<i for i in S);arr=[]
  for v in product(*[range(D[i]) for i in S]):
   if any(subset(m,Sm) and restrict(v,S,bits(m))==mv for m,mv in FIX.items()):continue
   for q in range(3**t):arr.append((v,q))
  X[t,T]=arr

def build(M1,M2):
 assert (M2&~M1)==0
 names=[];lb=[];ub=[];ii=[]
 def add(n,lo=0,hi=np.inf,integer=False):
  j=len(names);names.append(n);lb.append(lo);ub.append(hi);ii.append(1 if integer else 0);return j
 qidx={(m,v):add(('q',m,v),0,1,True) for m in FUT for v in Q[m]}
 Ms={1:M1,2:M2};xidx={}
 for t in (1,2):
  for T in range(8):
   if Ms[t]>>T&1:
    for v,q in X[t,T]:xidx[t,T,v,q]=add(('x',t,T,v,q),0,1,True)
 # exhausted depth1 parents (a,r mod3)
 eidx={(a,r):add(('e',a,r),0,1,True) for a in R for r in range(3)}
 # H dual on D2 leaves q=0..8
 deep=[(a,q) for a in R for q in range(9)];Hy={u:[] for u in deep};Hsup={};l3=lambda e:(e+1)**3-e**3
 for e in range(4):
  for b5,b7,b11 in product(range(2),repeat=3):
   if e==b5==b7==b11==0:continue
   ell2=(2*e+1)*(3 if b5 else 1)*(3 if b7 else 1)*(3 if b11 else 1)
   ell3=l3(e)*l3(b5)*l3(b7)*l3(b11);wt=ALPHA*ell2+BETA*ell3
   km=(e,b5,b7,b11);groups={}
   for a,q in deep:
    key=()
    if e>=1:key+=(a[0],)
    if e>=2:key+=(q%(3**(e-1)),)
    if b5:key+=(a[1],)
    if b7:key+=(a[2],)
    if b11:key+=(a[3],)
    groups.setdefault(key,[]).append((a,q))
   arr=[]
   for key,mem in groups.items():
    j=add(('y',km,key));arr.append(j)
    for u in mem:Hy[u].append(j)
   Hsup[km]=(wt,arr)
 rows=[];los=[];his=[]
 def row(d,lo=-np.inf,hi=np.inf):rows.append(d);los.append(lo);his.append(hi)
 # future squarefree completion
 for m in FUT:row({j:1 for (mm,v),j in qidx.items() if mm==m},1,1)
 for i,m in enumerate(FUT):
  Im=bits(m)
  for n in FUT[i+1:]:
   if not subset(m,n):continue
   In=bits(n)
   for mv in Q[m]:
    jm=qidx[m,mv];js=[qidx[n,nv] for nv in Q[n] if restrict(nv,In,Im)==mv]
    if js:row({jm:1,**{j:1 for j in js}},hi=1)
 # exactly one at each present modulus
 nodes=[]
 for t in (1,2):
  for T in range(8):
   if Ms[t]>>T&1:
    nodes.append((t,T));row({j:1 for (tt,TT,v,q),j in xidx.items() if tt==t and TT==T},1,1)
 # all comparable deep moduli incompatible
 for t,T in nodes:
  ST=osupp(T)
  for u,U in nodes:
   if (t,T)==(u,U) or t>u or not subset(T,U):continue
   SU=osupp(U)
   for tv,tq in X[t,T]:
    jt=xidx[t,T,tv,tq];js=[]
    for uv,uq in X[u,U]:
     if uq%(3**t)==tq and restrict(uv,SU,ST)==tv:js.append(xidx[u,U,uv,uq])
    if js:row({jt:1,**{j:1 for j in js}},hi=1)
 # deep vs future squarefree divisor incompatibility
 for t,T in nodes:
  S=osupp(T);Sm=sum(1<<i for i in S)
  for m in FUT:
   if not subset(m,Sm):continue
   I=bits(m)
   for qv in Q[m]:
    jq=qidx[m,qv];js=[xidx[t,T,xv,qq] for xv,qq in X[t,T] if restrict(xv,S,I)==qv]
    if js:row({jq:1,**{j:1 for j in js}},hi=1)
 # choose some first-exhausted depth1 parent
 row({j:1 for j in eidx.values()},lo=1)
 for (a,r),je in eidx.items():
  # parent must survive future shallow q classes
  for m in FUT:
   I=bits(m);av=tuple(a[i] for i in I);jq=qidx.get((m,av))
   if jq is not None:row({je:1,jq:1},hi=1)
  # parent must survive all t1 classes (none matching it)
  for T in range(8):
   if M1>>T&1:
    S=osupp(T);av=tuple(a[i] for i in S);jx=xidx.get((1,T,av,r))
    if jx is not None:row({je:1,jx:1},hi=1)
  # all three t2 children are covered by t2 classes
  for k in range(3):
   q=r+3*k; d={je:1}
   for T in range(8):
    if M2>>T&1:
     S=osupp(T);av=tuple(a[i] for i in S);jx=xidx.get((2,T,av,q))
     if jx is not None:d[jx]=d.get(jx,0)-1
   row(d,hi=0)
 # H bad dual
 for km,(wt,arr) in Hsup.items():row({j:1 for j in arr},hi=wt)
 for a,q in deep:
  d={j:1 for j in Hy[a,q]}
  for m in FUT:
   I=bits(m);av=tuple(a[i] for i in I);jq=qidx.get((m,av))
   if jq is not None:d[jq]=d.get(jq,0)+ZH
  for t,T in nodes:
   S=osupp(T);av=tuple(a[i] for i in S);qq=q%(3**t);jx=xidx.get((t,T,av,qq))
   if jx is not None:d[jx]=d.get(jx,0)+ZH
  row(d,lo=ZH)
 n=len(names);A=lil_matrix((len(rows),n))
 for rr,d in enumerate(rows):
  for j,v in d.items():A[rr,j]=v
 return np.zeros(n),np.array(ii),Bounds(np.array(lb),np.array(ub)),LinearConstraint(A.tocsr(),np.array(los),np.array(his)),dict(names=names,qidx=qidx,xidx=xidx,eidx=eidx,nodes=nodes)

def solve(M1,M2,tlim=120):
 st=time.time();c,ii,bd,con,meta=build(M1,M2);print('D2',hex(M1),hex(M2),'vars',len(c),'bins',ii.sum(),'rows',con.A.shape[0],flush=True)
 r=milp(c,integrality=ii,bounds=bd,constraints=con,options={'time_limit':tlim,'mip_rel_gap':0,'presolve':True})
 print(r.message,'inc',r.x is not None,'gap',getattr(r,'mip_gap',None),'sec',time.time()-st,flush=True)
 if r.x is not None:
  ex=[x for x,j in meta['eidx'].items() if r.x[j]>.5];print('ex',ex[:5])
 return r
if __name__=='__main__':
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('--M1',default='0xf');ap.add_argument('--M2',default='0xf');ap.add_argument('--time',type=float,default=120);a=ap.parse_args();solve(int(a.M1,0),int(a.M2,0),a.time)
