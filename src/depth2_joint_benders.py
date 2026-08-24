#!/usr/bin/env python3
import sys,time,numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import lil_matrix,vstack,hstack,csr_matrix
sys.path.insert(0,'/mnt/data/erdos2275')
import depth2_fixed_corrected as d
import state2275_hn_milp as b
from hn_oracle_prebuilt import HNOracle
from bbmst_oracle import BBMSTOracle
HCONST=b.CONST;HT=b.HRHS;HZ=HT-HCONST; FT=9.019;FCONST=.25;FZ=FT-FCONST

def avg_h(points,mu,mode):
 groups={}
 for i,(a,q) in enumerate(points):
  a0,a1,a2,a3=a
  if mode in ('c2','low','full') and a2>=3:a2=-1
  if mode in ('c3','low','full') and a3>=3:a3=-1
  qq=(q if q%3==0 else -1) if mode in ('q','full') else q
  groups.setdefault((a0,a1,a2,a3,qq),[]).append(i)
 out=np.zeros_like(mu)
 for inds in groups.values():out[inds]=mu[inds].sum()/len(inds)
 return out

def avg_f(points,mu,mode):
 groups={}
 for i,a in enumerate(points):
  a0,a1,a2,a3=a
  if mode in ('c2','low') and a2>=3:a2=-1
  if mode in ('c3','low') and a3>=3:a3=-1
  groups.setdefault((a0,a1,a2,a3),[]).append(i)
 out=np.zeros_like(mu)
 for inds in groups.values():out[inds]=mu[inds].sum()/len(inds)
 return out

def run(target=(1,0,0,0),core=(1,2,3),M1=0xf,M2=0xf,maxit=100,total_time=43,master_time=10,verbose=True):
 z,meta=d.build(target,core,M1,M2)
 if z is None:return {'status':'preinf','meta':meta}
 c0,ii0,bd0,con=z;hs=meta['h_start'];B=con.A[:hs,:];blo=con.lb[:hs];bhi=con.ub[:hs]
 lb0=bd0.lb.copy();ub0=bd0.ub.copy()
 for j,nm in enumerate(meta['names']):
  if nm[0]=='y':lb0[j]=ub0[j]=0
 HO=HNOracle(meta['deep'],2);FO=BBMSTOracle(b.R);Nh=HO.N;Nf=FO.N;n0=len(c0)
 # choice masks on H points and F leaf coverage masks
 choice_js=[];hmasks=[];leafmasks=[]
 for j,nm in enumerate(meta['names']):
  if nm[0] not in ('q','x1','x2'):continue
  hm=np.zeros(Nh,dtype=np.uint8);lm=np.zeros((Nf,9),dtype=np.uint8)
  if nm[0]=='q':
   _,m,v=nm;I=b.bits(m)
   for k,(a,q) in enumerate(HO.points):hm[k]=tuple(a[i] for i in I)==v
   for k,a in enumerate(FO.points):
    if tuple(a[i] for i in I)==v:lm[k,:]=1
  elif nm[0]=='x1':
   _,T,v,r=nm;S=b.osupp(T)
   for k,(a,q) in enumerate(HO.points):hm[k]=(q%3==r and tuple(a[i] for i in S)==v)
   for k,a in enumerate(FO.points):
    if tuple(a[i] for i in S)==v:
     for q in range(9):lm[k,q]=(q%3==r)
  else:
   _,T,v,qq=nm;S=b.osupp(T)
   for k,(a,q) in enumerate(HO.points):hm[k]=(q==qq and tuple(a[i] for i in S)==v)
   for k,a in enumerate(FO.points):
    if tuple(a[i] for i in S)==v:lm[k,qq]=1
  choice_js.append(j);hmasks.append(hm);leafmasks.append(lm)
 hmasks=np.asarray(hmasks,dtype=np.uint8);leafmasks=np.asarray(leafmasks,dtype=np.uint8);J=len(choice_js)
 # fixed core leaf coverage over shallow points
 corecov=np.zeros((Nf,9),dtype=np.uint8)
 for _,T,v,qq in meta['cores']:
  S=b.osupp(T)
  for k,a in enumerate(FO.points):
   if tuple(a[i] for i in S)==v:corecov[k,qq]=1
 # extend variables: yh exact selected-union over H base, ef shallow exhaustion
 nv=n0+Nh+Nf;c=np.zeros(nv);ii=np.r_[ii0,np.zeros(Nh+Nf,dtype=int)];lb=np.r_[lb0,np.zeros(Nh+Nf)];ub=np.r_[ub0,np.ones(Nh+Nf)]
 Bx=hstack([B,csr_matrix((B.shape[0],Nh+Nf))],format='csr');rows=[];los=[];his=[]
 # yh <= sum selected covering point
 for u in range(Nh):
  dd={n0+u:1}
  for h in np.flatnonzero(hmasks[:,u]):dd[choice_js[h]]=-1
  rows.append(dd);los.append(-np.inf);his.append(0)
 # ef <= selected coverage of every q leaf (or fixed core already covers it)
 for aidx in range(Nf):
  ej=n0+Nh+aidx
  for q in range(9):
   if corecov[aidx,q]:continue
   dd={ej:1}
   for h in np.flatnonzero(leafmasks[:,aidx,q]):dd[choice_js[h]]=-1
   rows.append(dd);los.append(-np.inf);his.append(0)
 Aextra=lil_matrix((len(rows),nv))
 for rr,dd in enumerate(rows):
  for j,v in dd.items():Aextra[rr,j]=v
 baseA=vstack([Bx,Aextra.tocsr()],format='csr');baselo=np.r_[blo,np.array(los)];basehi=np.r_[bhi,np.array(his)]
 hcuts=[];hd=[];fcuts=[];fd=[];seen=set();records=[];st0=time.time();maxjoint=(-1,None)
 if verbose:print('joint master vars',nv,'bins',ii.sum(),'rows',baseA.shape[0],'choice',J,flush=True)
 for it in range(maxit):
  if time.time()-st0>total_time:return {'status':'timeout','iters':it,'hcuts':len(hcuts),'fcuts':len(fcuts),'records':records,'elapsed':time.time()-st0}
  nr=len(hcuts)+len(fcuts)
  if nr:
   C=lil_matrix((nr,nv));clo=[];rr=0
   for mu,de in zip(hcuts,hd):C[rr,n0:n0+Nh]=mu;clo.append(de);rr+=1
   for mu,de in zip(fcuts,fd):C[rr,n0+Nh:]=mu;clo.append(de);rr+=1
   A=vstack([baseA,C.tocsr()],format='csr');lo=np.r_[baselo,np.array(clo)];hi=np.r_[basehi,np.full(nr,np.inf)]
  else:A=baseA;lo=baselo;hi=basehi
  st=time.time();r=milp(c,integrality=ii,bounds=Bounds(lb,ub),constraints=LinearConstraint(A,lo,hi),options={'time_limit':master_time,'mip_rel_gap':0,'presolve':True});mst=time.time()-st
  if verbose:print('iter',it,r.message,'inc',r.x is not None,'sec',mst,'cuts',len(hcuts),len(fcuts),flush=True)
  if r.x is None:return {'status':'closed','iters':it,'hcuts':len(hcuts),'fcuts':len(fcuts),'records':records,'elapsed':time.time()-st0}
  sel=np.array([r.x[j]>.5 for j in choice_js],dtype=bool);sig=np.packbits(sel).tobytes()
  if sig in seen:return {'status':'repeat','iters':it,'records':records}
  seen.add(sig)
  hdel=np.any(hmasks[sel].astype(bool),axis=0);leaf=np.any(leafmasks[sel].astype(bool),axis=0)|corecov.astype(bool);exh=np.all(leaf,axis=1)
  hsurv=[u for u,k in zip(HO.points,~hdel) if k];fsurv=[a for a,k in zip(FO.points,~exh) if k]
  H,hmu,hsec,_=HO.solve(hsurv,'highs-ipm');F,fmu,fsec,_=FO.solve(fsurv,'highs-ipm')
  rec={'it':it,'H':H,'F':F,'Nh':len(hsurv),'Nf':len(fsurv),'msec':mst,'hsec':hsec,'fsec':fsec};records.append(rec)
  if verbose:print(' H',H,'F',F,'Ns',len(hsurv),len(fsurv),flush=True)
  if H>=HT-1e-9 and F>=FT-1e-9:
   chosen=[meta['names'][j] for j,s in zip(choice_js,sel) if s]
   if verbose:print('FOUND JOINT BAD',chosen,flush=True)
   return {'status':'joint_bad','H':H,'F':F,'chosen':chosen,'iters':it,'records':records,'elapsed':time.time()-st0}
  addedH=[];addedF=[]
  if H<HT-1e-9:
   for mode,mu in [('raw',hmu)]+[(m,avg_h(HO.points,hmu,m)) for m in ('q','c2','c3','low','full')]:
    val=HO.score(mu)
    if val<HT-1e-10:
     de=1-(val-HCONST)/HZ;hcuts.append(mu.copy());hd.append(de+1e-9);addedH.append((mode,val,de))
  if F<FT-1e-9:
   for mode,mu in [('raw',fmu)]+[(m,avg_f(FO.points,fmu,m)) for m in ('c2','c3','low')]:
    val=FO.score(mu)
    if val<FT-1e-10:
     de=1-(val-FCONST)/FZ;fcuts.append(mu.copy());fd.append(de+1e-9);addedF.append((mode,val,de))
  rec['addH']=addedH;rec['addF']=addedF
  if verbose:print(' addH',[(x[0],round(x[2],4)) for x in addedH],'addF',[(x[0],round(x[2],4)) for x in addedF],flush=True)
 return {'status':'maxit','iters':maxit,'hcuts':len(hcuts),'fcuts':len(fcuts),'records':records,'elapsed':time.time()-st0}
if __name__=='__main__':
 import json,argparse
 ap=argparse.ArgumentParser();ap.add_argument('--time',type=float,default=43);ap.add_argument('--maxit',type=int,default=100);a=ap.parse_args();r=run(total_time=a.time,maxit=a.maxit);print('RESULT',json.dumps(r,default=str))
