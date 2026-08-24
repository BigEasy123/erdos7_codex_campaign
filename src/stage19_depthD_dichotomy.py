#!/usr/bin/env python3
from itertools import product
import sys,time
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix
sys.path.insert(0,'/mnt/data')
from stage17_global_depth1_packet_milp import (
    DIMS,PUB_EXTREMA,normalize_pub_pattern,pattern_members,ATOMS,
    choices_for,subsetmask,compatible_patterns,pattern_matches_atom
)
ALPHA=0.011800206435906386
BETA=0.0010516899397334059
HRHS=0.48249312963046986
ZF=9.019-0.25
OTHER=(1,2,3)

def build(ext=1,D=2,force_all=False):
    cfg=[normalize_pub_pattern(s) for s in PUB_EXTREMA[ext-1]]
    cov=set()
    for p in cfg: cov |= pattern_members(p)
    Rsh=[ATOMS[j] for j in range(len(ATOMS)) if j not in cov]
    leaves=range(3**D)
    Rdeep=[(a,q) for a in Rsh for q in leaves]
    # shallow legal patterns for each optional support; choices_for includes z, strip z duplicates
    pats={T:[] for T in range(8)}
    for T in range(8):
        seen=set()
        for p,z,S,x in choices_for(ext,T):
            if p in seen: continue
            seen.add(p)
            if any(pattern_matches_atom(p,a) for a in Rsh): pats[T].append((p,S,x))
    names=[];lb=[];ub=[];integ=[]
    def add(name,lo=0,hi=np.inf,integer=False):
        i=len(names);names.append(name);lb.append(lo);ub.append(hi);integ.append(1 if integer else 0);return i
    xidx={}; choices={}
    for t in range(1,D+1):
      for T in range(8):
        arr=[]
        for p,S,x in pats[T]:
          for q in range(3**t):
            arr.append((p,q,S,x))
        choices[t,T]=arr
        for k,c in enumerate(arr): xidx[t,T,k]=add(('x',t,T,k),0,1,True)
    eidx={a:add(('e',a),0,1,True) for a in Rsh}
    # F dual on shallow atoms
    Fbyatom={a:[] for a in Rsh};Fsupport={}
    for mask in range(1,16):
        I=tuple(i for i in range(4) if mask>>i&1);groups={}
        for a in Rsh:groups.setdefault(tuple(a[i] for i in I),[]).append(a)
        arr=[]
        for key,mem in groups.items():
            j=add(('yF',mask,key));arr.append(j)
            for a in mem:Fbyatom[a].append(j)
        Fsupport[mask]=arr
    # HN linear B dual on expanded deep points, exponent e3=0..D+1
    Bbypt={u:[] for u in Rdeep};Bsupport={}
    l3=lambda e:(e+1)**3-e**3
    for e3 in range(D+2):
      for b5,b7,b11 in product(range(2),repeat=3):
        if e3==b5==b7==b11==0:continue
        ell2=(2*e3+1)*(3 if b5 else 1)*(3 if b7 else 1)*(3 if b11 else 1)
        ell3=l3(e3)*l3(b5)*l3(b7)*l3(b11)
        ell=ALPHA*ell2+BETA*ell3
        km=(e3,b5,b7,b11); groups={}
        for a,q in Rdeep:
            key=()
            if e3>=1:key+=(a[0],)
            if e3>=2:key+=(q%(3**(e3-1)),)
            if b5:key+=(a[1],)
            if b7:key+=(a[2],)
            if b11:key+=(a[3],)
            groups.setdefault(key,[]).append((a,q))
        arr=[]
        for key,mem in groups.items():
            j=add(('yB',km,key));arr.append(j)
            for u in mem:Bbypt[u].append(j)
        Bsupport[km]=(ell,arr)
    ZB=HRHS-ALPHA-BETA
    n=len(names);rows=[];los=[];his=[]
    def rowadd(d,lo=-np.inf,hi=np.inf):rows.append(d);los.append(lo);his.append(hi)
    # one class per actual modulus 3^(t+1)*d; pure powers forced by divisor completion
    for t in range(1,D+1):
      for T in range(8):
        row={xidx[t,T,k]:1 for k in range(len(choices[t,T]))}
        low=1 if (T==0 or force_all) else 0
        rowadd(row,low,1)
    # comparable nodes: (t,T) <= (u,U), compatible shallow + compatible p-adic residue forbidden
    conflict=0
    nodes=[(t,T) for t in range(1,D+1) for T in range(8)]
    for ni,(t,T) in enumerate(nodes):
      for u,U in nodes[ni+1:]:
        comparable=(t<=u and subsetmask(T,U)) or (u<=t and subsetmask(U,T))
        if not comparable:continue
        for k,(p,q,*_) in enumerate(choices[t,T]):
          for l,(pp,qq,*_) in enumerate(choices[u,U]):
            if not compatible_patterns(p,pp):continue
            rr=min(t,u)
            if q%(3**rr)==qq%(3**rr):
                rowadd({xidx[t,T,k]:1,xidx[u,U,l]:1},-np.inf,1);conflict+=1
    # Exhausted shallow atom iff all D-deep leaves are covered (one-way sufficient for dual adversary)
    for a in Rsh:
      for leaf in leaves:
        d={eidx[a]:1}
        for t in range(1,D+1):
          rr=leaf%(3**t)
          for T in range(8):
            for k,(p,q,*_) in enumerate(choices[t,T]):
              if q==rr and pattern_matches_atom(p,a):d[xidx[t,T,k]]=d.get(xidx[t,T,k],0)-1
        rowadd(d,-np.inf,0)
    # F dual certifies min F >= 9.019 on nonexhausted shallow atoms
    for mask,arr in Fsupport.items():rowadd({j:1 for j in arr},-np.inf,3**mask.bit_count()-0.75)
    for a in Rsh:
        d={j:1 for j in Fbyatom[a]};d[eidx[a]]=ZF;rowadd(d,ZF,np.inf)
    # HN dual certifies linear bias gate bad on surviving deep points
    for km,(ell,arr) in Bsupport.items():rowadd({j:1 for j in arr},-np.inf,ell)
    for a,leaf in Rdeep:
        d={j:1 for j in Bbypt[(a,leaf)]}
        for t in range(1,D+1):
          rr=leaf%(3**t)
          for T in range(8):
            for k,(p,q,*_) in enumerate(choices[t,T]):
              if q==rr and pattern_matches_atom(p,a):d[xidx[t,T,k]]=d.get(xidx[t,T,k],0)+ZB
        rowadd(d,ZB,np.inf)
    A=lil_matrix((len(rows),n),dtype=float)
    for r,d in enumerate(rows):
      for j,v in d.items():A[r,j]=v
    meta=dict(names=names,xidx=xidx,eidx=eidx,choices=choices,Rsh=Rsh,Rdeep=Rdeep,conflicts=conflict)
    return np.zeros(n),np.array(integ),Bounds(np.array(lb),np.array(ub)),LinearConstraint(A.tocsr(),np.array(los),np.array(his)),meta

def solve(ext=1,D=2,time_limit=300,force_all=False):
    c,integ,bounds,cons,meta=build(ext,D,force_all)
    print('built ext',ext,'D',D,'vars',len(c),'rows',cons.A.shape[0],'binary',integ.sum(),'conflicts',meta['conflicts'],flush=True)
    t=time.time();res=milp(c,integrality=integ,bounds=bounds,constraints=cons,options={'time_limit':time_limit,'mip_rel_gap':0.0,'presolve':True})
    print('elapsed',time.time()-t,'status',res.message,'success',res.success,'gap',getattr(res,'mip_gap',None),flush=True)
    if res.x is not None:
      ex=[a for a,j in meta['eidx'].items() if res.x[j]>.5];print('exhausted',len(ex))
      for t in range(1,D+1):
       for T in range(8):
        sel=[meta['choices'][t,T][k] for k in range(len(meta['choices'][t,T])) if res.x[meta['xidx'][t,T,k]]>.5]
        if sel:print('node',t,format(T,'03b'),sel)
    return res,meta
if __name__=='__main__':
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('--ext',type=int,default=1);ap.add_argument('--D',type=int,default=2);ap.add_argument('--time',type=int,default=300);ap.add_argument('--force-all',action='store_true')
 a=ap.parse_args();solve(a.ext,a.D,a.time,a.force_all)
