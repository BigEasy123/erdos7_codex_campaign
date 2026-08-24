#!/usr/bin/env python3
import sys,json
import numpy as np
from scipy.sparse import vstack,csr_matrix
sys.path.insert(0,'/mnt/data/erdos2275')
import depth2_fullcover as f

P='/mnt/data/erdos2275/FULLCOVER_4CORES_FARKAS_EXACT.json'
data=json.load(open(P))

def rebuild(core):
 z,meta=f.build(core=tuple(core))
 assert z is not None
 c,ii,bd,con=z;hs=meta['h_start'];fc=meta['fullcover_rows']
 keep=list(range(hs))+list(range(con.A.shape[0]-fc,con.A.shape[0]))
 A=con.A[keep,:].tocsr();lo=con.lb[keep];hi=con.ub[keep]
 rows=[];ds=[]
 for rr in range(A.shape[0]):
  ar=A.getrow(rr)
  if np.isfinite(hi[rr]):rows.append(ar);ds.append(int(round(hi[rr])))
  if np.isfinite(lo[rr]):rows.append(-ar);ds.append(int(round(-lo[rr])))
 n=A.shape[1]
 I=csr_matrix((np.ones(n),(np.arange(n),np.arange(n))),shape=(n,n))
 rows.extend([I.getrow(j) for j in range(n)]);ds.extend([1]*n)
 return vstack(rows,format='csr'),ds

print('FULLCOVER 4-CORE EXACT FARKAS REPLAY')
print('target',data['target'],'M1',data['M1'],'M2',data['M2'])
weak=None
for cert in data['certificates']:
 C,d=rebuild(cert['core']);m,n=C.shape
 lam=[0]*m
 for i,v in cert['active']:
  i=int(i);v=int(v);assert 0<=i<m and v>=0;lam[i]=v
 cols=[0]*n;rhs=0
 for i,v in enumerate(lam):
  if not v:continue
  rhs+=v*d[i]
  row=C.getrow(i)
  for j,a in zip(row.indices,row.data):
   ai=int(round(float(a)));assert float(a)==ai
   cols[j]+=v*ai
 mn=min(cols);assert mn>=0;assert rhs<0
 den=int(cert['den']);score=rhs/den
 print('core',tuple(cert['core']),'PASS','active',sum(v>0 for v in lam),'mincol',mn,'rhs=',f'{rhs}/{den}','=',score)
 if weak is None or score>weak[0]:weak=(score,tuple(cert['core']),rhs,den)
print('ALL_PASS=True')
print('weakest_rhs',weak)
