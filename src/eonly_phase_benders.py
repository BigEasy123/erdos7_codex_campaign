#!/usr/bin/env python3
import pathlib,sys,time,json,math
import numpy as np
from scipy.optimize import linprog,milp,Bounds,LinearConstraint
from scipy.sparse import csr_matrix,lil_matrix,vstack,hstack
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import state2275_child_pooled_master as p

class PhaseOracle:
 def __init__(self):
  st=time.time();c,ii,b,con,m=p.build(.02,.2,True);self.buildsec=time.time()-st
  self.meta=m; self.n=len(c); self.eids=np.array(list(m['eidx'].values()),dtype=int); self.ne=len(self.eids)
  eset=set(self.eids.tolist());self.xids=np.array([j for j in range(self.n) if j not in eset],dtype=int)
  self.A=con.A.tocsr();self.lo=np.asarray(con.lb);self.hi=np.asarray(con.ub)
  # construct finite upper/lower inequality copies and record sign / source row
  rows=[];rhs0=[];db=[]
  # db per inequality stored sparse as list (e-position, coefficient)
  epos={j:k for k,j in enumerate(self.eids)}
  for r in range(self.A.shape[0]):
   ar=self.A.getrow(r)
   eco=[]
   for j,v in zip(ar.indices,ar.data):
    if j in epos:eco.append((epos[j],float(v)))
   if np.isfinite(self.hi[r]):
    rows.append((r,1));rhs0.append(float(self.hi[r]));db.append([(k,-v) for k,v in eco])
   if np.isfinite(self.lo[r]):
    rows.append((r,-1));rhs0.append(float(-self.lo[r]));db.append([(k,+v) for k,v in eco])
  # Matrix in x-cont vars + t. Build by selecting original rows and signs.
  B=lil_matrix((len(rows),len(self.xids)+1))
  oldnew={j:k for k,j in enumerate(self.xids)}
  for rr,(r,sgn) in enumerate(rows):
   ar=self.A.getrow(r)
   for j,v in zip(ar.indices,ar.data):
    k=oldnew.get(j)
    if k is not None:B[rr,k]=sgn*v
   B[rr,-1]=-1.0
  self.B=B.tocsr();self.rhs0=np.asarray(rhs0);self.db=db
  self.obj=np.zeros(len(self.xids)+1);self.obj[-1]=1.0
  self.bounds=[(float(b.lb[j]),float(b.ub[j]) if np.isfinite(b.ub[j]) else None) for j in self.xids]+[(0,None)]
  print('oracle build',self.buildsec,'orig vars',self.n,'cont',len(self.xids),'e',self.ne,'phase rows',len(rows),flush=True)
 def rhs(self,e):
  out=self.rhs0.copy()
  for rr,lst in enumerate(self.db):
   if lst:out[rr]+=sum(v*e[k] for k,v in lst)
  return out
 def solve(self,e,tlim=12):
  b=self.rhs(e);st=time.time();r=linprog(self.obj,A_ub=self.B,b_ub=b,bounds=self.bounds,method='highs',options={'time_limit':tlim,'presolve':True});sec=time.time()-st
  if r.x is None:return {'status':r.status,'msg':r.message,'sec':sec},None
  phi=float(r.fun); y=np.asarray(r.ineqlin.marginals)
  g=np.zeros(self.ne)
  for rr,lst in enumerate(self.db):
   yy=y[rr]
   if yy:
    for k,v in lst:g[k]+=yy*v
  return {'status':r.status,'msg':r.message,'sec':sec,'phi':phi,'g':g},r

def master(cuts,mincard=9,tlim=5):
 n=331;c=np.ones(n);rows=[];lo=[];hi=[]
 # sum e >= mincard; <=330 inherited from base but irrelevant here
 rows.append({i:1 for i in range(n)});lo.append(mincard);hi.append(330)
 for g,rhs in cuts:
  rows.append({i:float(v) for i,v in enumerate(g) if abs(v)>1e-12});lo.append(-np.inf);hi.append(float(rhs))
 A=lil_matrix((len(rows),n))
 for rr,d in enumerate(rows):
  for j,v in d.items():A[rr,j]=v
 r=milp(c,integrality=np.ones(n,dtype=int),bounds=Bounds(np.zeros(n),np.ones(n)),constraints=LinearConstraint(A.tocsr(),np.array(lo),np.array(hi)),options={'time_limit':tlim,'mip_rel_gap':0,'presolve':True})
 return r

def run(maxit=50):
 O=PhaseOracle();cuts=[];records=[]
 for it in range(maxit):
  mr=master(cuts,9,5)
  print('master',it,mr.status,mr.message,'inc',mr.x is not None,'obj',getattr(mr,'fun',None),'cuts',len(cuts),flush=True)
  if mr.x is None:
   status='MASTER_INFEASIBLE' if mr.status==2 else 'MASTER_UNKNOWN';break
  e=(mr.x>.5).astype(float);E=np.flatnonzero(e).tolist()
  z,rr=O.solve(e,12)
  print(' phase phi',z.get('phi'),'sec',z['sec'],'card',len(E),flush=True)
  rec={'it':it,'card':len(E),'E':E,'phase_status':z['status'],'phase_sec':z['sec'],'phi':z.get('phi')}
  records.append(rec)
  if rr is None:
   status='PHASE_UNKNOWN';break
  if z['phi']<=1e-8:
   status='FEASIBLE_E_PATTERN';
   # save continuous witness values for inspection
   rec['phase_feasible']=True;break
  g=z['g'];rhs=-z['phi']+float(g@e)
  # validate subgradient cut at current e: lhs-rhs=phi
  gap=float(g@e-rhs)
  rec.update(cut_nnz=int((abs(g)>1e-12).sum()),cut_gap=gap,gmin=float(g.min()),gmax=float(g.max()))
  print(' cut nnz',rec['cut_nnz'],'gap',gap,'g range',g.min(),g.max(),flush=True)
  cuts.append((g,rhs))
 else: status='ITER_LIMIT'
 out={'status':status,'cuts':len(cuts),'records':records,'oracle_build':O.buildsec}
 output = ROOT / 'artifacts' / 'current_state' / 'EONLY_PHASE_BENDERS.json'
 json.dump(out,open(output,'w'),indent=2)
 print('RESULT',status,'cuts',len(cuts),flush=True)
 return out
if __name__=='__main__':run(50)
