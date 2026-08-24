#!/usr/bin/env python3
from fractions import Fraction as F
from itertools import product
import math,time,argparse,json,sys
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import lil_matrix
sys.path.insert(0,'/mnt/data/erdos2275')
import state2275_hn_milp as s
R=s.R; N=len(R); FIX=set(s.FIX); MIXED={m for m in range(1,16) if m.bit_count()>=2}; FUT=MIXED-FIX
PR=((1,3),(2,5),(4,7),(8,11)); ZF=9.019-0.25

def bits(m): return tuple(i for i in range(4) if m>>i&1)
def Gall(m):
 z=F(1)
 for bit,p in PR:
  if m&bit:z*=F(p,p-1)
 return z
f={m:(Gall(m) if m in FUT else Gall(m)-1) for m in range(1,16)}
# Only residue cylinders intersecting R matter; omitted residues are an extra harmless option.
cyl={}; atom_cyl={j:[] for j in range(N)}
for m in range(1,16):
 I=bits(m); groups={}
 for j,a in enumerate(R):groups.setdefault(tuple(a[i] for i in I),[]).append(j)
 for v,mem in groups.items():
  k=(m,v);cyl[k]=mem
  for j in mem:atom_cyl[j].append(k)
keys=list(cyl)

def heavy_vectors(m,cut):
 ps=[p for bit,p in PR if m&bit]
 # weight prod p^(1-e); enumerate all >=cut
 maxes=[1+int(math.floor(math.log(1/cut,p)))+1 for p in ps]
 arr=[]
 for es in product(*[range(1,M+1) for M in maxes]):
  w=F(1)
  for p,e in zip(ps,es):w*=F(1,p**(e-1))
  if float(w)+1e-15 < cut:continue
  if m not in FUT and all(e==1 for e in es):continue
  arr.append((es,w))
 return arr

def build(cut=.05):
 hv={m:heavy_vectors(m,cut) for m in range(1,16)}
 hsum={m:sum((w for _,w in hv[m]),F(0)) for m in range(1,16)}
 tail={m:max(F(0),f[m]-hsum[m]) for m in range(1,16)}
 names=[];lb=[];ub=[];integ=[]
 def add(n,lo=0,hi=np.inf,integer=False):
  j=len(names);names.append(n);lb.append(lo);ub.append(hi);integ.append(1 if integer else 0);return j
 # each heavy exponent vector chooses at most one relevant shallow residue; can choose outside R/omit
 xidx={}
 for m in range(1,16):
  mkeys=[k for k in keys if k[0]==m]
  for h,(es,w) in enumerate(hv[m]):
   # Future squarefree base class must use one of the legal Q[m] residues.
   allowed={tuple(v) for v in s.Q[m]} if (m in FUT and all(e==1 for e in es)) else None
   for k in mkeys:
    if allowed is not None and tuple(k[1]) not in allowed: continue
    xidx[m,h,k[1]]=add(('x',m,h,es,k[1]),0,1,True)
 # fractional remainder tail by residue
 tidx={k:add(('tail',)+k,0,float(tail[k[0]])) for k in keys if tail[k[0]]>0}
 eidx={j:add(('e',j),0,1,True) for j in range(N)}
 yidx={k:add(('y',)+k,0,np.inf) for k in keys}
 rows=[];los=[];his=[]
 def row(d,lo=-np.inf,hi=np.inf):rows.append(d);los.append(lo);his.append(hi)
 # heavy modulus: at most one residue intersecting R; future squarefree bases exactly one.
 for m in range(1,16):
  for h,(es,w) in enumerate(hv[m]):
   ids=[j for (mm,hh,v),j in xidx.items() if mm==m and hh==h]
   if m in FUT and all(e==1 for e in es):
    if not ids: return None
    row({j:1 for j in ids},lo=1,hi=1)
   else:
    row({j:1 for j in ids},hi=1)
 # Future squarefree bases are comparable when supports nest: compatible residues are forbidden.
 baseh={}
 for m in FUT:
  for h,(es,w) in enumerate(hv[m]):
   if all(e==1 for e in es): baseh[m]=h; break
 for m in FUT:
  Im=bits(m); hm=baseh[m]
  for n in FUT:
   if m>=n or (m & ~n): continue
   In=bits(n); hn=baseh[n]
   for (mm,hh,mv),jm in list(xidx.items()):
    if mm!=m or hh!=hm: continue
    js=[]
    for (nn,h2,nv),jn in xidx.items():
     if nn==n and h2==hn and s.restrict(nv,In,Im)==mv: js.append(jn)
    if js: row({jm:1,**{j:1 for j in js}},hi=1)
 # Every future squarefree base divides every higher modulus whose radical contains it.
 # Therefore compatible projected shallow residues would make the higher class redundant.
 for m in FUT:
  Im=bits(m); hm=baseh[m]
  for U in range(1,16):
   if m & ~U: continue
   IU=bits(U)
   for hu,(es,w) in enumerate(hv[U]):
    if U==m and all(e==1 for e in es): continue
    for (mm,hh,mv),jm in list(xidx.items()):
     if mm!=m or hh!=hm: continue
     js=[]
     for (uu,h2,uv),ju in xidx.items():
      if uu==U and h2==hu and s.restrict(uv,IU,Im)==mv: js.append(ju)
     if js: row({jm:1,**{j:1 for j in js}},hi=1)
 # Divisor completion inside each represented exponent lattice: if an exact heavy
 # modulus is present, every immediate lower exponent-vector modulus is present.
 # The squarefree parent on an already-fixed support is already in the canonical core.
 for m in range(1,16):
  es_to_h={tuple(es):h for h,(es,w) in enumerate(hv[m])}
  for h,(es,w) in enumerate(hv[m]):
   for i,e in enumerate(es):
    if e<=1: continue
    par=list(es);par[i]-=1;par=tuple(par)
    hp=es_to_h.get(par)
    if hp is None:
     # only possible squarefree parent omitted from strict-tail list on fixed supports
     continue
    child=[j for (mm,hh,v),j in xidx.items() if mm==m and hh==h]
    parent=[j for (mm,hh,v),j in xidx.items() if mm==m and hh==hp]
    if child:
     d={j:1 for j in child}
     for j in parent:d[j]=d.get(j,0)-1
     row(d,hi=0)
 # fractional leftover support budget
 for m in range(1,16):
  ids=[tidx[k] for k in keys if k[0]==m and k in tidx]
  if ids:row({j:1 for j in ids},hi=float(tail[m]))
 # e => total allocated incident load >=1
 # load includes weights of heavy vector selections and fractional tail
 for aidx in range(N):
  d={eidx[aidx]:-1}
  for m in range(1,16):
   I=bits(m);v=tuple(R[aidx][i] for i in I)
   for h,(_,w) in enumerate(hv[m]):
    j=xidx.get((m,h,v))
    if j is not None:d[j]=d.get(j,0)+float(w)
   j=tidx.get((m,v))
   if j is not None:d[j]=d.get(j,0)+1
  row(d,lo=0)
 # BBMST bad dual
 for m in range(1,16):row({yidx[k]:1 for k in keys if k[0]==m},hi=3**m.bit_count()-0.75)
 for aidx in range(N):
  d={eidx[aidx]:ZF}
  for k in atom_cyl[aidx]:d[yidx[k]]=1
  row(d,lo=ZF)
 row({eidx[j]:1 for j in range(N)},hi=N-1)
 n=len(names);A=lil_matrix((len(rows),n))
 for r,d in enumerate(rows):
  for j,v in d.items():A[r,j]=v
 meta=dict(names=names,eidx=eidx,xidx=xidx,tidx=tidx,hv=hv,tail=tail,nvars=n,nbin=sum(integ),nrows=len(rows))
 return np.zeros(n),np.array(integ),Bounds(np.array(lb),np.array(ub)),LinearConstraint(A.tocsr(),np.array(los),np.array(his)),meta

def run(cut=.05,tlim=60,out=None):
 z=build(cut)
 if z is None:
  print('PREINF build'); return None,None,{'cut':cut,'status':'preinf'}
 c,ii,b,con,meta=z
 print('cut',cut,'vars',len(c),'binary',ii.sum(),'rows',con.A.shape[0], 'heavy',sum(len(v) for v in meta['hv'].values()),flush=True)
 print('tail total',float(sum(meta['tail'].values(),F(0))), 'max',max(float(x) for x in meta['tail'].values()),flush=True)
 st=time.time();r=milp(c,integrality=ii,bounds=b,constraints=con,options={'time_limit':tlim,'mip_rel_gap':0,'presolve':True});sec=time.time()-st
 print('status',r.status,r.message,'success',r.success,'inc',r.x is not None,'gap',getattr(r,'mip_gap',None),'sec',sec,flush=True)
 rec={'cut':cut,'status':int(r.status),'message':r.message,'success':bool(r.success),'incumbent':r.x is not None,'gap':getattr(r,'mip_gap',None),'sec':sec,'vars':len(c),'binary':int(ii.sum()),'rows':con.A.shape[0],'heavy':sum(len(v) for v in meta['hv'].values())}
 if r.x is not None:
  ex=sum(r.x[j]>.5 for j in meta['eidx'].values());rec['exhausted']=ex;rec['survive']=N-ex
  print('exhausted',ex,'survive',N-ex,flush=True)
 if out:open(out,'w').write(json.dumps(rec,indent=2,default=str))
 return r,meta,rec
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--cut',type=float,default=.05);ap.add_argument('--time',type=float,default=60);ap.add_argument('--out');a=ap.parse_args();run(a.cut,a.time,a.out)
