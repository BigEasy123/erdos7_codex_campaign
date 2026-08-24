#!/usr/bin/env python3
import sys,time,numpy as np,json,itertools
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import lil_matrix,vstack,hstack,csr_matrix
sys.path.insert(0,'/mnt/data/erdos2275')
import depth2_fixed_corrected as d
import state2275_hn_milp as b
from bbmst_oracle import BBMSTOracle
FT=9.019;FC=.25;FZ=FT-FC

def orbit_maps(points):
 idx={a:i for i,a in enumerate(points)};maps=[];u2=(3,4,5);u3=(3,4,5,6,7,8,9)
 for p2 in itertools.permutations(u2):
  mp2=dict(zip(u2,p2))
  for sh in range(7):
   mp3={u3[i]:u3[(i+sh)%7] for i in range(7)};m=np.empty(len(points),dtype=int)
   for i,a in enumerate(points):m[i]=idx[(a[0],a[1],mp2.get(a[2],a[2]),mp3.get(a[3],a[3]))]
   maps.append(m)
 return maps

def build_master(target,core,M1=0xf,M2=0xf):
 z,meta=d.build(target,core,M1,M2)
 if z is None:return None,meta
 c0,ii0,bd0,con=z;hs=meta['h_start'];keep=[j for j,nm in enumerate(meta['names']) if nm[0]!='y'];oldnew={j:k for k,j in enumerate(keep)}
 names=[meta['names'][j] for j in keep];B=con.A[:hs,keep];blo=con.lb[:hs];bhi=con.ub[:hs]
 lb0=bd0.lb[keep];ub0=bd0.ub[keep];ii0=ii0[keep];n0=len(keep)
 # remap choice indices
 choice=[]
 for old,nm in enumerate(meta['names']):
  if nm[0] in ('q','x1','x2') and old in oldnew:choice.append((oldnew[old],nm))
 O=BBMSTOracle(b.R);N=O.N;leafm=[];choice_js=[]
 for j,nm in choice:
  lm=np.zeros((N,9),dtype=np.uint8)
  if nm[0]=='q':
   _,m,v=nm;I=b.bits(m)
   for k,a in enumerate(O.points):
    if tuple(a[i] for i in I)==v:lm[k,:]=1
  elif nm[0]=='x1':
   _,T,v,r=nm;S=b.osupp(T)
   for k,a in enumerate(O.points):
    if tuple(a[i] for i in S)==v:
     for q in range(9):lm[k,q]=(q%3==r)
  else:
   _,T,v,qq=nm;S=b.osupp(T)
   for k,a in enumerate(O.points):
    if tuple(a[i] for i in S)==v:lm[k,qq]=1
  choice_js.append(j);leafm.append(lm)
 leafm=np.asarray(leafm,dtype=np.uint8);corecov=np.zeros((N,9),dtype=np.uint8)
 for _,T,v,qq in meta['cores']:
  S=b.osupp(T)
  for k,a in enumerate(O.points):
   if tuple(a[i] for i in S)==v:corecov[k,qq]=1
 nv=n0+N;c=np.zeros(nv);ii=np.r_[ii0,np.zeros(N,dtype=int)];lb=np.r_[lb0,np.zeros(N)];ub=np.r_[ub0,np.ones(N)]
 Bx=hstack([B,csr_matrix((B.shape[0],N))],format='csr');rows=[]
 for ai in range(N):
  ej=n0+ai
  for q in range(9):
   if corecov[ai,q]:continue
   dd={ej:1}
   for h in np.flatnonzero(leafm[:,ai,q]):dd[choice_js[h]]=-1
   rows.append(dd)
 E=lil_matrix((len(rows),nv))
 for rr,dd in enumerate(rows):
  for j,v in dd.items():E[rr,j]=v
 A=vstack([Bx,E.tocsr()],format='csr');lo=np.r_[blo,np.full(len(rows),-np.inf)];hi=np.r_[bhi,np.zeros(len(rows))]
 return dict(c=c,ii=ii,lb=lb,ub=ub,A=A,lo=lo,hi=hi,O=O,choice_js=choice_js,leafm=leafm,corecov=corecov,n0=n0,names=names,meta=meta)

def run(target=(1,0,0,0),core=(1,2,3),M1=0xf,M2=0xf,maxit=100,total_time=60,master_time=30,verbose=True):
 X=build_master(target,core,M1,M2)
 if isinstance(X,tuple):return {'status':'preinf'}
 c,ii,lb,ub,baseA,baselo,basehi=X['c'],X['ii'],X['lb'],X['ub'],X['A'],X['lo'],X['hi'];O=X['O'];N=O.N;n0=X['n0'];choice_js=X['choice_js'];leafm=X['leafm'];corecov=X['corecov'];names=X['names']
 maps=orbit_maps(O.points);cuts=[];deltas=[];seen=set();records=[];maxF=(-1,None);st0=time.time()
 if verbose:print('COMPACT vars',len(c),'bins',ii.sum(),'base rows',baseA.shape[0],'n0',n0,flush=True)
 for it in range(maxit):
  if time.time()-st0>total_time:return {'status':'timeout','iters':it,'cuts':len(cuts),'maxF':maxF[0],'records':records,'elapsed':time.time()-st0}
  if cuts:
   C=lil_matrix((len(cuts),len(c)))
   for rr,mu in enumerate(cuts):C[rr,n0:]=mu
   A=vstack([baseA,C.tocsr()],format='csr');lo=np.r_[baselo,np.array(deltas)];hi=np.r_[basehi,np.full(len(cuts),np.inf)]
  else:A=baseA;lo=baselo;hi=basehi
  st=time.time();r=milp(c,integrality=ii,bounds=Bounds(lb,ub),constraints=LinearConstraint(A,lo,hi),options={'time_limit':master_time,'mip_rel_gap':0,'presolve':True});ms=time.time()-st
  if verbose:print('iter',it,r.message,'inc',r.x is not None,'sec',ms,'cuts',len(cuts),flush=True)
  if r.x is None:
   if 'infeasible' in str(r.message).lower():return {'status':'closed','iters':it,'cuts':len(cuts),'maxF':maxF[0],'records':records,'elapsed':time.time()-st0}
   return {'status':'master_timeout','iters':it,'cuts':len(cuts),'maxF':maxF[0],'records':records,'elapsed':time.time()-st0}
  sel=np.array([r.x[j]>.5 for j in choice_js],dtype=bool);sig=np.packbits(sel).tobytes()
  if sig in seen:return {'status':'repeat','iters':it,'cuts':len(cuts),'maxF':maxF[0]}
  seen.add(sig);leaf=np.any(leafm[sel].astype(bool),axis=0)|corecov.astype(bool);exh=np.all(leaf,axis=1);surv=[a for a,k in zip(O.points,~exh) if k]
  F,mu,sec,_=O.solve(surv);chosen=[names[j] for j,s in zip(choice_js,sel) if s]
  if F>maxF[0]:maxF=(F,chosen)
  rec={'it':it,'F':F,'N':len(surv),'msec':ms,'lpsec':sec};records.append(rec)
  if verbose:print(' F',F,'N',len(surv),'max',maxF[0],flush=True)
  if F>=FT-1e-9:return {'status':'Fbad','F':F,'chosen':chosen,'iters':it,'cuts':len(cuts),'records':records,'elapsed':time.time()-st0}
  de=1-(F-FC)/FZ;local=set();added=0
  for mp in maps:
   mm=np.zeros_like(mu);mm[mp]=mu;key=np.round(mm,12).tobytes()
   if key in local:continue
   local.add(key);cuts.append(mm);deltas.append(de+1e-9);added+=1
  rec['delta']=de;rec['added']=added
 return {'status':'maxit','iters':maxit,'cuts':len(cuts),'maxF':maxF[0],'records':records,'elapsed':time.time()-st0}
if __name__=='__main__':
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('--time',type=float,default=60);ap.add_argument('--master',type=float,default=30);ap.add_argument('--maxit',type=int,default=100);a=ap.parse_args();r=run(total_time=a.time,master_time=a.master,maxit=a.maxit);print('RESULT',json.dumps(r,default=str))
