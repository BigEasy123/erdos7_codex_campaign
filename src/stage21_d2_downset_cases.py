#!/usr/bin/env python3
from itertools import product
import argparse,time,sys
import numpy as np
from scipy.optimize import milp,LinearConstraint,Bounds
from scipy.sparse import lil_matrix
sys.path.insert(0,'/mnt/data')
from stage20_fixed_extrema_downset_agg import DIMS,ATOMS,OTHER,EXT,parsepat,bits,osupp,restrict,subset,ALPHA,BETA,HRHS
ZH=HRHS-ALPHA-BETA

def all_downsets():
 out=[]
 for M in range(1<<8):
  if not (M&1): continue
  ok=True
  for U in range(8):
   if M>>U&1:
    for T in range(8):
     if subset(T,U) and not(M>>T&1): ok=False;break
    if not ok:break
  if ok:out.append(M)
 return out
DS=all_downsets()
PAIRS=[(a,b) for a in DS for b in DS if (b&~a)==0]
assert len(DS)==19 and len(PAIRS)==148,(len(DS),len(PAIRS))

def residual(ext):
 cfg={m:v for m,v in map(parsepat,EXT[ext-1])};R=[]
 for a in ATOMS:
  if not any(tuple(a[i] for i in bits(m))==v for m,v in cfg.items()):R.append(a)
 assert len(R)==303
 return cfg,R

def build(ext=1,target_idx=0,pair_idx=0):
 cfg,R=residual(ext);target=R[target_idx];M1,M2=PAIRS[pair_idx];Ms={1:M1,2:M2}
 names=[];lb=[];ub=[];integ=[]
 def add(n,lo=0,hi=np.inf,integer=False):
  j=len(names);names.append(n);lb.append(lo);ub.append(hi);integ.append(1 if integer else 0);return j
 xidx={};xvals={};node={}
 for t in (1,2):
  for T in range(8):
   if not (Ms[t]>>T&1):continue
   S=osupp(T);Sm=sum(1<<i for i in S);arr=[];ids=[]
   for vals in product(*[range(DIMS[i]) for i in S]):
    if any((m&~Sm)==0 and restrict(vals,S,bits(m))==v for m,v in cfg.items()):continue
    for z in range(3**t):
     j=add(('x',t,T,vals,z),0,1,True);xidx[t,T,vals,z]=j;arr.append((vals,z));ids.append(j)
   if not ids:return None,dict(reason=('empty_node',t,T),target=target,pair=(M1,M2))
   xvals[t,T]=arr;node[t,T]=ids
 # H dual on all deep leaves, selected classes excuse covered points
 deep=[(a,z) for a in R for z in range(9)]
 Hy={u:[] for u in deep};Hsup={};l3=lambda e:(e+1)**3-e**3
 for e in range(4):
  for b5,b7,b11 in product(range(2),repeat=3):
   if e==b5==b7==b11==0:continue
   ell2=(2*e+1)*(3 if b5 else 1)*(3 if b7 else 1)*(3 if b11 else 1)
   ell3=l3(e)*l3(b5)*l3(b7)*l3(b11);wt=ALPHA*ell2+BETA*ell3
   km=(e,b5,b7,b11);groups={}
   for a,z in deep:
    key=()
    if e>=1:key+=(a[0],)
    if e>=2:key+=(z%(3**(e-1)),)
    if b5:key+=(a[1],)
    if b7:key+=(a[2],)
    if b11:key+=(a[3],)
    groups.setdefault(key,[]).append((a,z))
   arr=[]
   for key,mem in groups.items():
    j=add(('yH',km,key));arr.append(j)
    for u in mem:Hy[u].append(j)
   Hsup[km]=(wt,arr)
 rows=[];los=[];his=[]
 def row(d,lo=-np.inf,hi=np.inf):rows.append(d);los.append(lo);his.append(hi)
 # exactly one residue for every modulus in fixed downsets
 for k,ids in node.items():row({j:1 for j in ids},1,1)
 # comparable residues incompatible, aggregate by coarse choice
 dcomp=0
 selected=list(node)
 for u,U in selected:
  SU=osupp(U)
  for t,T in selected:
   if (t,T)==(u,U) or t>u or not subset(T,U):continue
   ST=osupp(T);groups={}
   for uv,zu in xvals[u,U]:
    rv=restrict(uv,SU,ST);zt=zu%(3**t);j2=xidx.get((t,T,rv,zt))
    if j2 is not None:groups.setdefault(j2,[]).append(xidx[u,U,uv,zu])
   for j2,js in groups.items():
    d={j2:1};d.update({jf:1 for jf in js});row(d,hi=1);dcomp+=1
 # target exhaustion
 for z in range(9):
  d={}
  for t,T in selected:
   S=osupp(T);v=tuple(target[i] for i in S);j=xidx.get((t,T,v,z%(3**t)))
   if j is not None:d[j]=1
  if not d:return None,dict(reason=('uncoverable_leaf',z),target=target,pair=(M1,M2))
  row(d,lo=1)
 # H bad dual
 for km,(wt,arr) in Hsup.items():row({j:1 for j in arr},hi=wt)
 for a,z in deep:
  d={j:1 for j in Hy[a,z]}
  for t,T in selected:
   S=osupp(T);v=tuple(a[i] for i in S);j=xidx.get((t,T,v,z%(3**t)))
   if j is not None:d[j]=d.get(j,0)+ZH
  row(d,lo=ZH)
 n=len(names);A=lil_matrix((len(rows),n))
 for r,d in enumerate(rows):
  for j,v in d.items():A[r,j]=v
 con=LinearConstraint(A.tocsr(),np.array(los),np.array(his))
 return (np.zeros(n),np.array(integ),Bounds(np.array(lb),np.array(ub)),con),dict(target=target,pair=(M1,M2),node=node,xidx=xidx,xvals=xvals,names=names,dcomp=dcomp,rows=len(rows),bins=sum(integ))

def solve_case(ext,target,pair,tlim=10,presolve=True):
 built,meta=build(ext,target,pair)
 if built is None:return 'INFEASIBLE_PRE',None,meta
 c,ii,b,con=built
 r=milp(c,integrality=ii,bounds=b,constraints=con,options={'time_limit':tlim,'mip_rel_gap':0,'presolve':presolve})
 msg=r.message.lower()
 if r.success:return 'FEASIBLE',r,meta
 if 'infeasible' in msg:return 'INFEASIBLE',r,meta
 return 'UNKNOWN',r,meta

def run(ext=1,target=0,tlim=10,start=0,end=148,out=None):
 counts={};unknown=[];feas=[];st=time.time();fo=open(out,'a') if out else None
 for k in range(start,min(end,len(PAIRS))):
  s,r,m=solve_case(ext,target,k,tlim)
  counts[s]=counts.get(s,0)+1
  line=f'{k}\t{s}\tM1={m["pair"][0]:02x}\tM2={m["pair"][1]:02x}\trows={m.get("rows",0)}\tbins={m.get("bins",0)}\n'
  print(line.strip(),flush=True)
  if fo:fo.write(line);fo.flush()
  if s=='UNKNOWN':unknown.append(k)
  if s=='FEASIBLE':
   feas.append(k)
   print('FOUND FEASIBLE CASE',k,flush=True)
   # keep going, to classify all
 if fo:fo.close()
 print('SUMMARY',counts,'unknown',unknown,'feasible',feas,'elapsed',time.time()-st,flush=True)
 return counts,unknown,feas
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--ext',type=int,default=1);ap.add_argument('--target',type=int,default=0);ap.add_argument('--time',type=float,default=5);ap.add_argument('--start',type=int,default=0);ap.add_argument('--end',type=int,default=148);ap.add_argument('--out');a=ap.parse_args();run(a.ext,a.target,a.time,a.start,a.end,a.out)
