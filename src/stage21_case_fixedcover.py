import sys,time,argparse
import numpy as np
sys.path.insert(0,'/mnt/data')
from stage21_d2_downset_cases import build
from stage20_fixed_extrema_downset_agg import osupp
from scipy.optimize import milp,Bounds

def solve(ext,target,pair,fixed,tlim=20):
 built,meta=build(ext,target,pair)
 if built is None:return None,meta
 c,ii,b,con=built
 lb=b.lb.copy();ub=b.ub.copy();targeta=meta['target']
 # fixed list (t,T,z) means choose target-matching residue at node exactly
 for t,T,z in fixed:
  S=osupp(T);vals=tuple(targeta[i] for i in S)
  j=meta['xidx'].get((t,T,vals,z))
  if j is None: return 'PREINF',meta
  # force j=1; node exactly-one will kill rest
  lb[j]=ub[j]=1
 st=time.time();r=milp(c,integrality=ii,bounds=Bounds(lb,ub),constraints=con,options={'time_limit':tlim,'mip_rel_gap':0,'presolve':False})
 print('fixed',fixed,'elapsed',time.time()-st,r.message,'inc',r.x is not None,flush=True)
 return r,meta
if __name__=='__main__':
 # case5: M1 {0,1,2}, M2 {0}, fix t1 0,1,2 to z=0,1,2
 solve(1,0,5,[(1,0,0),(1,1,1),(1,2,2)],30)
