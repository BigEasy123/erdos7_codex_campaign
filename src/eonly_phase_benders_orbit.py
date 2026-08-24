#!/usr/bin/env python3
import sys,time,json,pickle,os,itertools
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import lil_matrix
sys.path.insert(0,'/mnt/data/erdos2275')
from eonly_phase_benders import PhaseOracle
import state2275_hn_milp as s
CK='/mnt/data/erdos2275/EONLY_ORBIT_BENDERS_CK.pkl'; OUT='/mnt/data/erdos2275/EONLY_ORBIT_BENDERS.json'

def orbit_maps(points):
 idx={a:i for i,a in enumerate(points)};maps=[];u2=(3,4,5);u3=(3,4,5,6,7,8,9)
 for p2 in itertools.permutations(u2):
  mp2=dict(zip(u2,p2))
  for sh in range(7):
   mp3={u3[i]:u3[(i+sh)%7] for i in range(7)};m=np.empty(len(points),dtype=int)
   for i,a in enumerate(points):m[i]=idx[(a[0],a[1],mp2.get(a[2],a[2]),mp3.get(a[3],a[3]))]
   maps.append(m)
 return maps
MAPS=orbit_maps(s.R)

def master(cuts,mincard=9,tlim=5):
 n=331;c=np.ones(n);A=lil_matrix((1+len(cuts),n));lo=np.full(1+len(cuts),-np.inf);hi=np.empty(1+len(cuts))
 A[0,:]=1;lo[0]=mincard;hi[0]=330
 for rr,(g,rhs) in enumerate(cuts,1):
  nz=np.flatnonzero(np.abs(g)>1e-12);A[rr,nz]=g[nz];hi[rr]=rhs
 return milp(c,integrality=np.ones(n,dtype=int),bounds=Bounds(np.zeros(n),np.ones(n)),constraints=LinearConstraint(A.tocsr(),lo,hi),options={'time_limit':tlim,'mip_rel_gap':0,'presolve':True})

def add_orbits(cuts,seen,g,rhs):
 new=0
 for mp in MAPS:
  gg=np.zeros_like(g);gg[mp]=g
  key=(tuple(np.round(gg,10)),round(float(rhs),10))
  if key not in seen:seen.add(key);cuts.append((gg,float(rhs)));new+=1
 return new

def run(maxit=150):
 O=PhaseOracle();cuts=[];seen=set();records=[]
 for it in range(maxit):
  mr=master(cuts,9,5)
  print('master',it,'status',mr.status,'inc',mr.x is not None,'obj',getattr(mr,'fun',None),'cuts',len(cuts),flush=True)
  if mr.x is None:
   status='MASTER_INFEASIBLE' if mr.status==2 else 'MASTER_UNKNOWN';break
  e=(mr.x>.5).astype(float);card=int(e.sum());E=np.flatnonzero(e).tolist()
  z,rr=O.solve(e,10);phi=z.get('phi')
  print(' phase card',card,'phi',phi,'sec',z['sec'],flush=True)
  rec={'it':it,'card':card,'E':E,'phi':phi,'phase_sec':z['sec'],'cuts_before':len(cuts)}
  records.append(rec)
  if rr is None:status='PHASE_UNKNOWN';break
  if phi<=1e-8:status='FEASIBLE_E_PATTERN';break
  g=z['g'];rhs=-phi+float(g@e);nnew=add_orbits(cuts,seen,g,rhs);rec.update(orbit_new=nnew,cuts_after=len(cuts),nnz=int((abs(g)>1e-12).sum()))
  print(' orbit cuts new',nnew,'total',len(cuts),flush=True)
  pickle.dump({'cuts':cuts,'seen':seen,'records':records,'it':it+1},open(CK,'wb'))
 else:status='ITER_LIMIT'
 out={'status':status,'cuts':len(cuts),'iterations':len(records),'records':records,'orbits':len(MAPS),'oracle_build':O.buildsec}
 json.dump(out,open(OUT,'w'),indent=2);print('RESULT',status,'cuts',len(cuts),'iters',len(records),flush=True)
if __name__=='__main__':run()
