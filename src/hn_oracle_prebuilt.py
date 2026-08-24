#!/usr/bin/env python3
import sys,time,numpy as np
from itertools import product
from scipy.optimize import linprog
from scipy.sparse import lil_matrix, csr_matrix
sys.path.insert(0,'/mnt/data/erdos2275')
import state2275_hn_milp as b

class HNOracle:
    def __init__(self, points, depth=2):
        self.points=list(points); self.depth=depth; self.N=len(points)
        self.index={u:i for i,u in enumerate(self.points)}
        ALPHA=b.ALPHA;BETA=b.BETA
        pats=[]; l3=lambda e:(e+1)**3-e**3
        for e in range(depth+2):
            for b5,b7,b11 in product(range(2),repeat=3):
                if e==b5==b7==b11==0: continue
                ell2=(2*e+1)*(3 if b5 else 1)*(3 if b7 else 1)*(3 if b11 else 1)
                ell3=l3(e)*l3(b5)*l3(b7)*l3(b11)
                wt=ALPHA*ell2+BETA*ell3
                groups={}
                for j,(a,q) in enumerate(self.points):
                    key=()
                    if e>=1:key+=(a[0],)
                    if e>=2:key+=(q%(3**(e-1)),)
                    if b5:key+=(a[1],)
                    if b7:key+=(a[2],)
                    if b11:key+=(a[3],)
                    groups.setdefault(key,[]).append(j)
                pats.append((wt,list(groups.values())))
        self.pats=pats
        self.P=len(pats); nv=self.N+self.P
        self.obj=np.zeros(nv)
        for k,(wt,_) in enumerate(pats): self.obj[self.N+k]=wt
        rows=sum(len(gs) for _,gs in pats)
        A=lil_matrix((rows,nv)); rr=0
        for k,(_,gs) in enumerate(pats):
            for mem in gs:
                A[rr,mem]=1.0; A[rr,self.N+k]=-1.0; rr+=1
        self.A=A.tocsr(); self.b=np.zeros(rows)
        self.E=np.zeros((1,nv)); self.E[0,:self.N]=1.0
        self.be=np.array([1.0])
        self.bounds_base=[(0,None)]*nv
        print('HNOracle built points',self.N,'patterns',self.P,'rows',rows,'nnz',self.A.nnz,flush=True)

    def score(self,mu):
        val=b.CONST
        for wt,gs in self.pats:
            mx=max(float(np.sum(mu[mem])) for mem in gs)
            val += wt*mx
        return val

    def solve(self,survivors,method='highs'):
        keep=np.zeros(self.N,dtype=bool)
        for u in survivors:
            j=self.index.get(u)
            if j is not None: keep[j]=True
        bounds=[(0,None) if keep[j] else (0,0) for j in range(self.N)] + [(0,None)]*self.P
        st=time.time()
        z=linprog(self.obj,A_ub=self.A,b_ub=self.b,A_eq=self.E,b_eq=self.be,bounds=bounds,method=method,
                  options={'presolve':True})
        sec=time.time()-st
        if not z.success: return float('inf'),None,sec,z
        return b.CONST+z.fun,z.x[:self.N],sec,z
