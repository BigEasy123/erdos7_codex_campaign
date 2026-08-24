from itertools import product
import sys
sys.path.insert(0,'/mnt/data')
from stage20_fixed_extrema_downset_agg import ALPHA,BETA,bits

def uniform_H(de,D):
 n=len(de)
 if n==0:return 10**9
 l3=lambda e:(e+1)**3-e**3
 s=ALPHA+BETA
 for e in range(D+2):
  for b5,b7,b11 in product(range(2),repeat=3):
   if e==b5==b7==b11==0:continue
   wt=ALPHA*(2*e+1)*(3 if b5 else 1)*(3 if b7 else 1)*(3 if b11 else 1)+BETA*l3(e)*l3(b5)*l3(b7)*l3(b11)
   counts={}
   for a,z in de:
    key=()
    if e>=1:key+=(a[0],)
    if e>=2:key+=(z%(3**(e-1)),)
    if b5:key+=(a[1],)
    if b7:key+=(a[2],)
    if b11:key+=(a[3],)
    counts[key]=counts.get(key,0)+1
   s += wt*max(counts.values())/n
 return s
