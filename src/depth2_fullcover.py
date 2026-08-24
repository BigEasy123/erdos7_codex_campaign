#!/usr/bin/env python3
import sys,time,json,numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import lil_matrix,vstack
sys.path.insert(0,'/mnt/data/erdos2275')
import depth2_fixed_corrected as d
import state2275_hn_milp as b

def build(target=(1,0,0,0),core=(0,1,2),M1=0xf,M2=0xf):
 z,meta=d.build(target,core,M1,M2)
 if z is None:return None,meta
 c,ii,bd,con=z; A=con.A;lo=con.lb;hi=con.ub;rows=[];los=[];his=[]
 # Common projected residual U coverage: for every residual lower point (a,r),
 # either a lower-depth class covers it, or terminal projections in EACH top digit cover it.
 for a in b.R:
  for rr in range(3):
   qids=[]
   for m in b.FUT:
    I=b.bits(m);j=meta['qidx'].get((m,tuple(a[i] for i in I)))
    if j is not None:qids.append(j)
   x1ids=[]
   for T in range(8):
    if M1>>T&1:
     v=tuple(a[i] for i in b.osupp(T));j=meta['x1'].get((T,v,rr))
     if j is not None:x1ids.append(j)
   for dig in range(3):
    corehit=False
    for _,T,v,q in meta['cores']:
     if q%3==rr and q//3==dig and tuple(a[i] for i in b.osupp(T))==v:
      corehit=True;break
    if corehit:continue
    ids=list(qids)+list(x1ids)
    for T in range(8):
     if M2>>T&1 and T not in core:
      v=tuple(a[i] for i in b.osupp(T))
      q=rr+3*dig;j=meta['x2'].get((T,v,q))
      if j is not None:ids.append(j)
    if not ids:return None,{'reason':('uncoverable_U',a,rr,dig),'meta':meta}
    rows.append({j:1 for j in ids});los.append(1);his.append(np.inf)
 E=lil_matrix((len(rows),len(c)))
 for k,dd in enumerate(rows):
  for j,v in dd.items():E[k,j]=v
 A2=vstack([A,E.tocsr()],format='csr');lo2=np.r_[lo,np.array(los)];hi2=np.r_[hi,np.array(his)]
 meta=dict(meta);meta['fullcover_rows']=len(rows)
 return (c,ii,bd,LinearConstraint(A2,lo2,hi2)),meta

def solve_legal(core=(0,1,2),tlim=20):
 z,meta=build(core=core)
 if z is None:return {'status':'preinf','reason':meta.get('reason')}
 c,ii,bd,con=z
 # disable H dual objective/constraints only by zero objective; all original constraints include H-bad condition, so take only rows before h_start plus fullcover rows.
 hs=meta['h_start']; fc=meta['fullcover_rows']; keep_rows=list(range(hs))+list(range(con.A.shape[0]-fc,con.A.shape[0]))
 A=con.A[keep_rows,:];lo=con.lb[keep_rows];hi=con.ub[keep_rows]
 st=time.time();r=milp(np.zeros_like(c),integrality=ii,bounds=bd,constraints=LinearConstraint(A,lo,hi),options={'time_limit':tlim,'mip_rel_gap':0,'presolve':True});sec=time.time()-st
 return {'status_msg':str(r.message),'incumbent':r.x is not None,'seconds':sec,'vars':len(c),'bins':int(ii.sum()),'rows':A.shape[0],'fullcover_rows':fc}

if __name__=='__main__':
 out={}
 for core in [(0,1,2),(0,1,3),(0,2,3),(1,2,3)]:
  z=solve_legal(core,30);out[str(core)]=z;print(core,z,flush=True)
 json.dump(out,open('/mnt/data/erdos2275/FULLCOVER_LEGAL_4CORES.json','w'),indent=2)
