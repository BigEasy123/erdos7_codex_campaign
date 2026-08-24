from itertools import product,permutations

def norm_coord(vals):
 u=sorted(set(vals));mp={x:i for i,x in enumerate(u)};return tuple(mp[x] for x in vals)
def normalize(tri):
 out=[[0]*3 for _ in range(3)]
 for j in range(3):
  vals=[tri[i][j] for i in range(3)]; nv=norm_coord(vals)
  for i in range(3):out[i][j]=nv[i]
 return tuple(tuple(r) for r in out)
def canon(tri):
 tri=normalize(tri);reps=[]
 for bp in permutations(range(3)):
  for cp in permutations(range(3)):
   reps.append(tuple(tuple(tri[bp[i]][cp[j]] for j in range(3)) for i in range(3)))
 return min(reps)
coords=[]
for x in product(range(3),repeat=3):
 u=sorted(set(x))
 if u and u[0]==0 and u==list(range(len(u))):coords.append(x)
orbits={}
for c0,c1,c2 in product(coords,repeat=3):
 tri=tuple((c0[i],c1[i],c2[i]) for i in range(3))
 C=canon(tri);orbits[C]=orbits.get(C,0)+1
print('coord patterns',len(coords),'all orbits',len(orbits))
# classify by number active coords, squarefree, comparable pair count, divisor downset size normalized
def le(a,b):return all(x<=y for x,y in zip(a,b))
def divs(v):
 import itertools
 return itertools.product(*[range(x+1) for x in v])
from itertools import combinations
out=[]
for i,C in enumerate(sorted(orbits),1):
 active=sum(any(v[j] for v in C) for j in range(3))
 comp=sum(le(C[a],C[b]) or le(C[b],C[a]) for a,b in combinations(range(3),2))
 sq=all(x<=1 for v in C for x in v)
 D=set()
 for v in C:D.update(divs(v))
 out.append((i,C,active,comp,sq,len(D)))
print('counts active', {k:sum(r[2]==k for r in out) for k in range(4)})
print('counts comp', {k:sum(r[3]==k for r in out) for k in range(4)})
print('squarefree',sum(r[4] for r in out))
with open('TRIANGLE_ALL_ORDER_TYPES.txt','w') as f:
 for r in out:f.write(f"{r[0]} {r[1]} active={r[2]} comparable_pairs={r[3]} squarefree={r[4]} closure={r[5]}\n")
