#!/usr/bin/env python3
import time,json
from itertools import product
from multiprocessing import Pool
import numpy as np
from scipy.optimize import linprog
from scipy.sparse import lil_matrix
DIMS=(2,4,6,10); AT=list(product(*[range(d) for d in DIMS])); N=480; NV=N+15
# fixed all-cylinder LP matrix
c=np.zeros(NV)
for m in range(1,16):c[N+m-1]=3**m.bit_count()-.75
rows=[]
for m in range(1,16):
 I=tuple(i for i in range(4) if m>>i&1);g={}
 for j,a in enumerate(AT):g.setdefault(tuple(a[i] for i in I),[]).append(j)
 for mem in g.values():rows.append((m,mem))
A=lil_matrix((len(rows),NV));b=np.zeros(len(rows))
for r,(m,mem) in enumerate(rows):
 A[r,N+m-1]=-1
 for j in mem:A[r,j]=1
A=A.tocsr(); E=np.zeros((1,NV));E[0,:N]=1

def parse(s):
 I=tuple(i for i,c in enumerate(s) if c!='*');return I,tuple(int(s[i])-1 for i in I)
def covered(line):
 pats=[parse(s) for s in line.split()];cov=np.zeros(N,dtype=bool)
 for j,a in enumerate(AT):cov[j]=any(tuple(a[i] for i in I)==v for I,v in pats)
 return cov

def solve_line(item):
 idx,line=item;cov=covered(line);bounds=[(0,0) if cov[j] else (0,None) for j in range(N)]+[(0,None)]*15
 z=linprog(c,A_ub=A,b_ub=b,A_eq=E,b_eq=[1],bounds=bounds,method='highs')
 if not z.success:return idx,line,N-int(cov.sum()),None,None,None
 F=.25+z.fun;pr=float(z.x[N+11:N+15].sum());adj=(F-.25*pr)/(1-pr)
 return idx,line,N-int(cov.sum()),F,pr,adj
if __name__=='__main__':
 lines=[x.strip() for x in open('/mnt/data/stage18_bbmst_7637_partials.txt') if x.strip()];st=time.time();out=[]
 for k,x in enumerate(lines):
  out.append(solve_line((k,x)))
  if (k+1)%500==0:print('done',k+1,'elapsed',time.time()-st,flush=True)
 json.dump([dict(index=i,line=l,n=n,F=F,omitted=pr,adjusted=a) for i,l,n,F,pr,a in out],open('/mnt/data/STAGE24_7637_LP.json','w'))
 danger=[r for r in out if r[-1] is not None and r[-1]>=9.018-1e-9]
 open('/mnt/data/STAGE24_90_PARTIALS.txt','w').write('\n'.join(r[1] for r in danger)+'\n')
 print('total',len(out),'danger',len(danger),'minmax',min(r[-1] for r in out if r[-1]),max(r[-1] for r in out if r[-1]),'elapsed',time.time()-st)
 for r in sorted(danger,key=lambda x:x[-1],reverse=True)[:10]:print(r[0],r[2],r[-1],r[1])
