#!/usr/bin/env python3
from itertools import product
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix

D=(2,4,6,10)
AT=list(product(*[range(d) for d in D]))
LINE='11** 1*1* *22* 123* 1**1 *3*2 13*3'
ALPHA=0.011800206435906386
BETA=0.0010516899397334059
HRHS=0.48249312963046986
CONST=ALPHA+BETA
ZH=HRHS-CONST
FUT=(12,13,14,15)

def bits(m): return tuple(i for i in range(4) if m>>i&1)
def osupp(T): return (0,)+tuple(i+1 for i in range(3) if T>>i&1)
def parse(s):
    I=tuple(i for i,c in enumerate(s) if c!='*')
    m=sum(1<<i for i in I)
    return m,tuple(int(s[i])-1 for i in I)
def restrict(vals,S,U):
    pos={s:i for i,s in enumerate(S)}
    return tuple(vals[pos[u]] for u in U)
def subset(a,b): return (a & ~b)==0

FIX=dict(parse(s) for s in LINE.split())

def fixed_covered(a):
    for m,v in FIX.items():
        I=bits(m)
        if tuple(a[i] for i in I)==v:return True
    return False
R=[a for a in AT if not fixed_covered(a)]

# q choices for future squarefree supports, prefiltered against fixed comparable lower classes
Q={}
for m in FUT:
    I=bits(m); arr=[]
    for v in product(*[range(D[i]) for i in I]):
        bad=False
        for t,tv in FIX.items():
            if subset(t,m):
                if restrict(v,I,bits(t))==tv:
                    bad=True;break
        if not bad:arr.append(v)
    Q[m]=arr

# Deep choices prefiltered against fixed squarefree divisor classes
X={}
for T in range(8):
    S=osupp(T); Sm=sum(1<<i for i in S);arr=[]
    for v in product(*[range(D[i]) for i in S]):
        bad=False
        for m,mv in FIX.items():
            if subset(m,Sm) and restrict(v,S,bits(m))==mv:
                bad=True;break
        if bad:continue
        for z in range(3):arr.append((v,z))
    X[T]=arr


def build(target,M=255):
    # M bitset over T=0..7; require downset externally. target must survive final q completion.
    names=[];lb=[];ub=[];integ=[]
    def add(name,lo=0,hi=np.inf,integer=False):
        j=len(names); names.append(name); lb.append(lo);ub.append(hi);integ.append(1 if integer else 0); return j
    qidx={}
    for m in FUT:
        I=bits(m)
        for v in Q[m]:
            # target must remain after final squarefree completion
            if tuple(target[i] for i in I)==v: continue
            qidx[m,v]=add(('q',m,v),0,1,True)
    xidx={}
    for T in range(8):
        if not (M>>T)&1: continue
        for v,z in X[T]: xidx[T,v,z]=add(('x',T,v,z),0,1,True)

    # H dual variables
    deep=[(a,z) for a in R for z in range(3)]
    Hy={u:[] for u in deep}; Hsup={}
    l3=lambda e:(e+1)**3-e**3
    for e in range(3):
      for b5,b7,b11 in product(range(2),repeat=3):
        if e==b5==b7==b11==0:continue
        ell2=(2*e+1)*(3 if b5 else 1)*(3 if b7 else 1)*(3 if b11 else 1)
        ell3=l3(e)*l3(b5)*l3(b7)*l3(b11)
        wt=ALPHA*ell2+BETA*ell3
        km=(e,b5,b7,b11); groups={}
        for a,z in deep:
            key=()
            if e>=1:key+=(a[0],)
            if e>=2:key+=(z,)
            if b5:key+=(a[1],)
            if b7:key+=(a[2],)
            if b11:key+=(a[3],)
            groups.setdefault(key,[]).append((a,z))
        arr=[]
        for key,mem in groups.items():
            j=add(('y',km,key),0,np.inf,False);arr.append(j)
            for u in mem:Hy[u].append(j)
        Hsup[km]=(wt,arr)

    rows=[];los=[];his=[]
    def row(d,lo=-np.inf,hi=np.inf): rows.append(d);los.append(lo);his.append(hi)

    # one q per future support
    for m in FUT:
        ids=[j for (mm,v),j in qidx.items() if mm==m]
        if not ids:return None,{'reason':('no_q',m)}
        row({j:1 for j in ids},1,1)
    # q future-future comparability
    for i,m in enumerate(FUT):
      Im=bits(m)
      for n in FUT[i+1:]:
        if not subset(m,n):continue
        In=bits(n)
        # aggregate by coarse choice
        for mv in Q[m]:
            jm=qidx.get((m,mv))
            if jm is None:continue
            js=[]
            for nv in Q[n]:
                jn=qidx.get((n,nv))
                if jn is not None and restrict(nv,In,Im)==mv: js.append(jn)
            if js: row({jm:1,**{j:1 for j in js}},hi=1)

    # exactly one deep class per support in M
    for T in range(8):
        if not (M>>T)&1:continue
        ids=[j for (TT,v,z),j in xidx.items() if TT==T]
        if not ids:return None,{'reason':('no_x',T)}
        row({j:1 for j in ids},1,1)

    # deep-deep comparability at same depth
    Ts=[T for T in range(8) if (M>>T)&1]
    for T in Ts:
      ST=osupp(T)
      for U in Ts:
        if T>=U or not subset(T,U):continue
        SU=osupp(U)
        # for each coarse choice aggregate matching finer choices
        for tv,tz in X[T]:
            jt=xidx.get((T,tv,tz))
            if jt is None:continue
            js=[]
            for uv,uz in X[U]:
                ju=xidx.get((U,uv,uz))
                if ju is not None and uz==tz and restrict(uv,SU,ST)==tv:js.append(ju)
            if js: row({jt:1,**{j:1 for j in js}},hi=1)

    # deep vs future q divisor incompatibility
    for T in Ts:
      S=osupp(T); Sm=sum(1<<i for i in S)
      for m in FUT:
        if not subset(m,Sm):continue
        I=bits(m)
        for qv in Q[m]:
            jq=qidx.get((m,qv))
            if jq is None:continue
            js=[]
            for xv,z in X[T]:
                jx=xidx.get((T,xv,z))
                if jx is not None and restrict(xv,S,I)==qv:js.append(jx)
            if js: row({jq:1,**{j:1 for j in js}},hi=1)

    # target exhaustion: every z leaf hit by at least one selected deep class matching target
    for z in range(3):
        d={}
        for T in Ts:
            S=osupp(T); tv=tuple(target[i] for i in S)
            j=xidx.get((T,tv,z))
            if j is not None:d[j]=1
        if not d:return None,{'reason':('target_uncoverable',z)}
        row(d,lo=1)

    # H dual budgets
    for km,(wt,arr) in Hsup.items(): row({j:1 for j in arr},hi=wt)
    # H dual point cover; q/deep deletions excuse points
    for a,z in deep:
        d={j:1 for j in Hy[(a,z)]}
        # future squarefree deletion (same for all z)
        for m in FUT:
            I=bits(m); av=tuple(a[i] for i in I)
            jq=qidx.get((m,av))
            if jq is not None:d[jq]=d.get(jq,0)+ZH
        # deep deletion
        for T in Ts:
            S=osupp(T); av=tuple(a[i] for i in S)
            jx=xidx.get((T,av,z))
            if jx is not None:d[jx]=d.get(jx,0)+ZH
        row(d,lo=ZH)

    n=len(names);A=lil_matrix((len(rows),n),dtype=float)
    for r,d in enumerate(rows):
        for j,v in d.items():A[r,j]=v
    return (np.zeros(n),np.array(integ),Bounds(np.array(lb),np.array(ub)),LinearConstraint(A.tocsr(),np.array(los),np.array(his))),dict(names=names,qidx=qidx,xidx=xidx,rows=len(rows),bins=sum(integ),target=target,M=M)

def solve(target,M=255,tlim=60):
    built,meta=build(target,M)
    if built is None:
        print('PREINF',meta);return None,meta
    c,ii,b,con=built
    print('build target',target,'M',hex(M),'vars',len(c),'bins',ii.sum(),'rows',con.A.shape[0],flush=True)
    r=milp(c,integrality=ii,bounds=b,constraints=con,options={'time_limit':tlim,'mip_rel_gap':0.0,'presolve':True})
    print('status',r.message,'success',r.success,'gap',getattr(r,'mip_gap',None),'inc',r.x is not None,flush=True)
    if r.x is not None:
        qs=[];xs=[]
        for (m,v),j in meta['qidx'].items():
            if r.x[j]>.5:qs.append((m,v))
        for (T,v,z),j in meta['xidx'].items():
            if r.x[j]>.5:xs.append((T,v,z))
        print('q',qs);print('x',xs)
    return r,meta



def build_any(M=255):
    names=[];lb=[];ub=[];integ=[]
    def add(name,lo=0,hi=np.inf,integer=False):
        j=len(names);names.append(name);lb.append(lo);ub.append(hi);integ.append(1 if integer else 0);return j
    qidx={}
    for m in FUT:
      for v in Q[m]:qidx[m,v]=add(('q',m,v),0,1,True)
    xidx={}
    for T in range(8):
      if (M>>T)&1:
       for v,z in X[T]:xidx[T,v,z]=add(('x',T,v,z),0,1,True)
    eidx={a:add(('e',a),0,1,True) for a in R}
    deep=[(a,z) for a in R for z in range(3)]
    Hy={u:[] for u in deep};Hsup={};l3=lambda e:(e+1)**3-e**3
    for e in range(3):
      for b5,b7,b11 in product(range(2),repeat=3):
        if e==b5==b7==b11==0:continue
        ell2=(2*e+1)*(3 if b5 else 1)*(3 if b7 else 1)*(3 if b11 else 1)
        ell3=l3(e)*l3(b5)*l3(b7)*l3(b11);wt=ALPHA*ell2+BETA*ell3
        km=(e,b5,b7,b11);groups={}
        for a,z in deep:
          key=()
          if e>=1:key+=(a[0],)
          if e>=2:key+=(z,)
          if b5:key+=(a[1],)
          if b7:key+=(a[2],)
          if b11:key+=(a[3],)
          groups.setdefault(key,[]).append((a,z))
        arr=[]
        for key,mem in groups.items():
          j=add(('y',km,key),0,np.inf,False);arr.append(j)
          for u in mem:Hy[u].append(j)
        Hsup[km]=(wt,arr)
    rows=[];los=[];his=[]
    def row(d,lo=-np.inf,hi=np.inf):rows.append(d);los.append(lo);his.append(hi)
    for m in FUT:row({j:1 for (mm,v),j in qidx.items() if mm==m},1,1)
    # q comparability
    for i,m in enumerate(FUT):
      Im=bits(m)
      for n in FUT[i+1:]:
       if not subset(m,n):continue
       In=bits(n)
       for mv in Q[m]:
        jm=qidx[m,mv];js=[qidx[n,nv] for nv in Q[n] if restrict(nv,In,Im)==mv]
        if js:row({jm:1,**{j:1 for j in js}},hi=1)
    Ts=[T for T in range(8) if (M>>T)&1]
    for T in Ts:row({j:1 for (TT,v,z),j in xidx.items() if TT==T},1,1)
    # deep comparable
    for T in Ts:
      ST=osupp(T)
      for U in Ts:
       if T>=U or not subset(T,U):continue
       SU=osupp(U)
       for tv,tz in X[T]:
        jt=xidx[T,tv,tz];js=[xidx[U,uv,uz] for uv,uz in X[U] if uz==tz and restrict(uv,SU,ST)==tv]
        if js:row({jt:1,**{j:1 for j in js}},hi=1)
    # deep vs future squarefree divisor incompatibility
    for T in Ts:
      S=osupp(T);Sm=sum(1<<i for i in S)
      for m in FUT:
       if not subset(m,Sm):continue
       I=bits(m)
       for qv in Q[m]:
        jq=qidx[m,qv];js=[xidx[T,xv,z] for xv,z in X[T] if restrict(xv,S,I)==qv]
        if js:row({jq:1,**{j:1 for j in js}},hi=1)
    # choose at least one final-squarefree-surviving exhausted parent
    row({j:1 for j in eidx.values()},lo=1)
    for a,je in eidx.items():
      for m in FUT:
        I=bits(m);av=tuple(a[i] for i in I);jq=qidx.get((m,av))
        if jq is not None:row({je:1,jq:1},hi=1)
      for z in range(3):
        d={je:1}
        for T in Ts:
          S=osupp(T);av=tuple(a[i] for i in S);jx=xidx.get((T,av,z))
          if jx is not None:d[jx]=d.get(jx,0)-1
        row(d,hi=0)
    for km,(wt,arr) in Hsup.items():row({j:1 for j in arr},hi=wt)
    for a,z in deep:
      d={j:1 for j in Hy[a,z]}
      for m in FUT:
        I=bits(m);av=tuple(a[i] for i in I);jq=qidx.get((m,av))
        if jq is not None:d[jq]=d.get(jq,0)+ZH
      for T in Ts:
        S=osupp(T);av=tuple(a[i] for i in S);jx=xidx.get((T,av,z))
        if jx is not None:d[jx]=d.get(jx,0)+ZH
      row(d,lo=ZH)
    n=len(names);A=lil_matrix((len(rows),n),dtype=float)
    for r,d in enumerate(rows):
      for j,v in d.items():A[r,j]=v
    return (np.zeros(n),np.array(integ),Bounds(np.array(lb),np.array(ub)),LinearConstraint(A.tocsr(),np.array(los),np.array(his))),dict(names=names,qidx=qidx,xidx=xidx,eidx=eidx,rows=len(rows),bins=sum(integ),M=M)

def solve_any(M=255,tlim=60):
    import time
    st=time.time();built,meta=build_any(M);c,ii,b,con=built
    print('ANY build M',hex(M),'vars',len(c),'bins',ii.sum(),'rows',con.A.shape[0],flush=True)
    r=milp(c,integrality=ii,bounds=b,constraints=con,options={'time_limit':tlim,'mip_rel_gap':0.0,'presolve':True})
    print('ANY status',r.message,'success',r.success,'gap',getattr(r,'mip_gap',None),'inc',r.x is not None,'sec',time.time()-st,flush=True)
    if r.x is not None:
      ex=[a for a,j in meta['eidx'].items() if r.x[j]>.5]
      qs=[(m,v) for (m,v),j in meta['qidx'].items() if r.x[j]>.5]
      xs=[(T,v,z) for (T,v,z),j in meta['xidx'].items() if r.x[j]>.5]
      print('exhausted',ex[:10],'q',qs,'x',xs,flush=True)
    return r,meta

if __name__=='__main__':
    import argparse,ast
    ap=argparse.ArgumentParser();ap.add_argument('--target',default='(0,1,3,1)');ap.add_argument('--M',default='0xff');ap.add_argument('--time',type=float,default=60)
    a=ap.parse_args(); solve(ast.literal_eval(a.target),int(a.M,0),a.time)
