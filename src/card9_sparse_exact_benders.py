#!/usr/bin/env python3
import sys,pickle,itertools,time,os,json
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import lil_matrix
sys.path.insert(0,'/mnt/data/erdos2275')
import state2275_hn_milp as s
import eonly_card9_hybridprefix as h
CP='/mnt/data/erdos2275/EONLY_CARD9_COMPACT30.pkl';NP='/mnt/data/erdos2275/EONLY_CARD9_NOGOODS.pkl';OP='/mnt/data/erdos2275/PHASE_ORACLE.pkl';RP='/mnt/data/erdos2275/CARD9_SPARSE_EXACT_RECORDS.json';K=9

def ap(o,p):t=p+'.tmp';pickle.dump(o,open(t,'wb'),protocol=pickle.HIGHEST_PROTOCOL);os.replace(t,p)
def aj(o,p):t=p+'.tmp';json.dump(o,open(t,'w'),indent=2);os.replace(t,p)
def maps():
 idx={a:i for i,a in enumerate(s.R)};out=[];u2=(3,4,5);u3=(3,4,5,6,7,8,9)
 for p2 in itertools.permutations(u2):
  mp2=dict(zip(u2,p2))
  for sh in range(7):
   mp3={u3[i]:u3[(i+sh)%7] for i in range(7)};m=np.empty(331,dtype=int)
   for i,a in enumerate(s.R):m[i]=idx[(a[0],a[1],mp2.get(a[2],a[2]),mp3.get(a[3],a[3]))]
   out.append(m)
 return out
MAPS=maps()
def master(C,N,tlim=10):
 D={S:c for S,c in C.items()}
 for S in N:D[tuple(S)]=min(8,D.get(tuple(S),99))
 rows=list(D.items());A=lil_matrix((1+len(rows),331));lo=np.full(1+len(rows),-np.inf);hi=np.full(1+len(rows),np.inf);A[0,:]=1;lo[0]=hi[0]=K
 for rr,(S,cap) in enumerate(rows,1):
  for j in S:A[rr,j]=1
  hi[rr]=cap
 st=time.time();r=milp(np.zeros(331),integrality=np.ones(331,dtype=int),bounds=Bounds(np.zeros(331),np.ones(331)),constraints=LinearConstraint(A.tocsr(),lo,hi),options={'time_limit':tlim,'mip_rel_gap':0,'presolve':True});return r,time.time()-st,len(rows)
def run(maxit=40):
 C=pickle.load(open(CP,'rb'));N=pickle.load(open(NP,'rb')) if os.path.exists(NP) else set();O=pickle.load(open(OP,'rb'));R=json.load(open(RP)) if os.path.exists(RP) else []
 for q in range(maxit):
  mr,ms,nr=master(C,N,10);print('MASTER',q,'st',mr.status,'inc',mr.x is not None,'sec',round(ms,3),'C',len(C),'N',len(N),flush=True)
  if mr.x is None:
   st='CARD9_INFEASIBLE' if mr.status==2 else 'MASTER_UNKNOWN';R.append({'q':q,'status':st,'master_sec':ms,'C':len(C),'N':len(N)});aj(R,RP);print('RESULT',st,flush=True);return st
  E=np.flatnonzero(mr.x>.5).tolist();e=np.zeros(331);e[E]=1;z,rr=O.solve(e,12);phi=z.get('phi');print(' PHI',phi,'E',E,flush=True)
  rec={'q':q,'E':E,'phi':phi,'master_sec':ms,'phase_sec':z['sec'],'C_before':len(C),'N_before':len(N)}
  if rr is None:rec['status']='PHASE_UNKNOWN';R.append(rec);aj(R,RP);return 'PHASE_UNKNOWN'
  if phi<=1e-8:rec['status']='PHASE_FEASIBLE';R.append(rec);aj(R,RP);print('RESULT PHASE_FEASIBLE',flush=True);return 'PHASE_FEASIBLE'
  arr=np.array(E,dtype=int);nn=0
  for mp in MAPS:
   T=tuple(sorted(map(int,mp[arr])))
   if T not in N:N.add(T);nn+=1
  g=z['g'];rhs=-phi+float(g@e);nc=0
  for mp in MAPS:
   gg=np.zeros_like(g);gg[mp]=g
   for S,cap in h.derive_compact(gg,rhs):
    old=C.get(S)
    if old is None or cap<old:C[S]=cap;nc+=1
  rec.update(status='REJECTED',nogoods_new=nn,compact_new=nc,C_after=len(C),N_after=len(N));R.append(rec);ap(C,CP);ap(N,NP);aj(R,RP);print(' ADD N',nn,'C',nc,'tot',len(N),len(C),flush=True)
 print('ITER_LIMIT');return 'ITER_LIMIT'
if __name__=='__main__':run()
