#!/usr/bin/env python3
import sys,random,time,math
from itertools import product
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix
sys.path.insert(0,'/mnt/data')
from stage17_global_depth1_packet_milp import *
ALPHA=0.011800206435906386; BETA=0.0010516899397334059; HRHS=0.48249312963046986

def base(ext,D):
 cfg=[normalize_pub_pattern(s) for s in PUB_EXTREMA[ext-1]];cov=set()
 for p in cfg:cov|=pattern_members(p)
 R=[ATOMS[j] for j in range(len(ATOMS)) if j not in cov]
 pats={T:[] for T in range(8)}
 for T in range(8):
  seen=set()
  for p,z,S,x in choices_for(ext,T):
   if p in seen:continue
   seen.add(p)
   if any(pattern_matches_atom(p,a) for a in R):pats[T].append((p,S,x))
 ch={}
 for t in range(1,D+1):
  for T in range(8):ch[t,T]=[(p,q,S,x) for p,S,x in pats[T] for q in range(3**t)]
 return R,ch

def nodele(A,B):
 t,T=A;u,U=B;return t<=u and subsetmask(T,U)
def pair_ok(A,c,B,d):
 if c is None or d is None:return True
 if not(nodele(A,B) or nodele(B,A)):return True
 p,q,*_=c;pp,qq,*_=d
 if not compatible_patterns(p,pp):return True
 rr=min(A[0],B[0]);return q%(3**rr)!=qq%(3**rr)
def feasible(sel):
 it=list(sel.items())
 for i,(A,c) in enumerate(it):
  if c is None:continue
  for B,d in it[i+1:]:
   if not pair_ok(A,c,B,d):return False
 return True

def residuals(R,sel,D):
 deep=[];sh=[]
 for a in R:
  anysurv=False
  for leaf in range(3**D):
   hit=False
   for (t,T),c in sel.items():
    if c is None:continue
    p,q,*_=c
    if q==leaf%(3**t) and pattern_matches_atom(p,a):hit=True;break
   if not hit:deep.append((a,leaf));anysurv=True
  if anysurv:sh.append(a)
 return sh,deep

def Fmin(sh):
 if not sh:return 1e9
 n=len(sh);nv=n+15;c=np.zeros(nv)
 for mask in range(1,16):c[n+mask-1]=3**mask.bit_count()-.75
 rows=[]
 for mask in range(1,16):
  I=tuple(i for i in range(4) if mask>>i&1);groups={}
  for t,a in enumerate(sh):groups.setdefault(tuple(a[i] for i in I),[]).append(t)
  for mem in groups.values():rows.append((mask,mem))
 A=lil_matrix((len(rows),nv));b=np.zeros(len(rows))
 for r,(mask,mem) in enumerate(rows):
  for t in mem:A[r,t]=1
  A[r,n+mask-1]=-1
 E=np.zeros((1,nv));E[0,:n]=1
 res=linprog(c,A_ub=A.tocsr(),b_ub=b,A_eq=E,b_eq=[1],bounds=[(0,None)]*nv,method='highs')
 return .25+res.fun

def Hmin(deep,D):
 if not deep:return 1e9
 mods=[];l3=lambda e:(e+1)**3-e**3
 for e3 in range(D+2):
  for b5,b7,b11 in product(range(2),repeat=3):
   if e3==b5==b7==b11==0:continue
   e2=(2*e3+1)*(3 if b5 else 1)*(3 if b7 else 1)*(3 if b11 else 1)
   e3w=l3(e3)*l3(b5)*l3(b7)*l3(b11)
   mods.append((e3,b5,b7,b11,ALPHA*e2+BETA*e3w))
 n=len(deep);nv=n+len(mods);c=np.zeros(nv)
 for k,m in enumerate(mods):c[n+k]=m[-1]
 rows=[]
 for k,(e,b5,b7,b11,w) in enumerate(mods):
  groups={}
  for t,(a,q) in enumerate(deep):
   key=()
   if e>=1:key+=(a[0],)
   if e>=2:key+=(q%(3**(e-1)),)
   if b5:key+=(a[1],)
   if b7:key+=(a[2],)
   if b11:key+=(a[3],)
   groups.setdefault(key,[]).append(t)
  for mem in groups.values():rows.append((k,mem))
 A=lil_matrix((len(rows),nv));b=np.zeros(len(rows))
 for r,(k,mem) in enumerate(rows):
  for t in mem:A[r,t]=1
  A[r,n+k]=-1
 E=np.zeros((1,nv));E[0,:n]=1
 res=linprog(c,A_ub=A.tocsr(),b_ub=b,A_eq=E,b_eq=[1],bounds=[(0,None)]*nv,method='highs')
 return ALPHA+BETA+res.fun

def evalstate(R,sel,D):
 sh,de=residuals(R,sel,D);return Fmin(sh),Hmin(de,D),len(sh),len(de)
def search(ext=1,D=2,secs=180,seed=1):
 random.seed(seed);R,ch=base(ext,D);nodes=list(ch)
 sel={A:None for A in nodes}
 # pure p powers forced
 for A in nodes:
  if A[1]==0:
   opts=ch[A][:];random.shuffle(opts)
   for c in opts:
    sel[A]=c
    if feasible(sel):break
 # sparse random optional fill
 for A in nodes:
  if A[1]==0:continue
  if random.random()<.45:
   opts=ch[A][:];random.shuffle(opts)
   for c in opts[:200]:
    sel[A]=c
    if feasible(sel):break
   else:sel[A]=None
 cur=evalstate(R,sel,D)
 def score(v):return min(v[0]-9.019,(v[1]-HRHS)*5)
 best=(score(cur),cur,dict(sel));print('start',best[:2],flush=True)
 end=time.time()+secs;it=0;cache={}
 while time.time()<end:
  it+=1;A=random.choice(nodes);old=sel[A]
  opts=ch[A]
  cand=random.choice(opts) if (A[1]==0 or random.random()<.8) else None
  sel[A]=cand
  if not feasible(sel):sel[A]=old;continue
  key=tuple((A,repr(sel[A])) for A in nodes)
  nv=cache.get(key)
  if nv is None:nv=evalstate(R,sel,D);cache[key]=nv
  ns=score(nv);cs=score(cur);temp=max(.002,.12*(end-time.time())/secs)
  if ns>=cs or random.random()<math.exp((ns-cs)/temp):cur=nv
  else:sel[A]=old
  if ns>best[0]:
   best=(ns,nv,dict(sel));print('iter',it,'BEST',best[0],nv,flush=True)
   if nv[0]>9.019 and nv[1]>HRHS:
    print('FOUND BOTH BAD',flush=True);break
 print('FINAL',best[0],best[1])
 for A in nodes:
  if best[2][A] is not None:print(A,best[2][A])
 return best
if __name__=='__main__':
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('--ext',type=int,default=1);ap.add_argument('--D',type=int,default=2);ap.add_argument('--secs',type=int,default=180);ap.add_argument('--seed',type=int,default=1)
 a=ap.parse_args();search(a.ext,a.D,a.secs,a.seed)
