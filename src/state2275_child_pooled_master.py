#!/usr/bin/env python3
import sys,time,json,argparse
import numpy as np
from scipy.optimize import milp,Bounds,LinearConstraint
from scipy.sparse import lil_matrix,vstack,hstack,csr_matrix
sys.path.insert(0,'/mnt/data/erdos2275')
import state2275_hunter_benders_v2 as hb
import hunter_v2_step as hs
import state2275_hn_milp as s

# Safe partially-resolved next-3-digit relaxation.
# Large deep-3 heavy classes get explicit global next-digit choice.
# Smaller deep-3 heavy classes + subcutoff tail are pooled by shallow (support,residue)
# and may split fractionally among next digits, but that split is shared by all parents in the cylinder.

def build(cut=.02,digit_cut=.2,with_hunter=True):
    ctx=hb.build_context(cut,False); c0,ii0,bd0,A0,lo0,hi0,meta,cand,tailvars=ctx
    n0=len(c0);names=list(meta['names']);lb=list(bd0.lb);ub=list(bd0.ub);integ=list(ii0)
    def add(n,lo=0,hi=np.inf,integer=False):
        j=len(names);names.append(n);lb.append(lo);ub.append(hi);integ.append(1 if integer else 0);return j
    # explicit digit vars for resolved deep3 x options
    dz={}; resolved=set(); unresolved_groups={}
    for (m,h,v),jx in meta['xidx'].items():
        es,w=meta['hv'][m][h]
        if not ((m&1) and es[0]>=2): continue
        if float(w)+1e-15>=digit_cut:
            resolved.add(jx)
            for q in range(3): dz[jx,q]=add(('dz',jx,q,m,h,v),0,1,True)
        else:
            unresolved_groups.setdefault((m,v),[]).append((jx,float(w)))
    # pooled child conditional capacity for each shallow cylinder with unresolved deep3 mass or deep3 tail
    pool={}
    groupkeys=set(unresolved_groups)
    for (m,v),jt in meta['tidx'].items():
        if m&1:groupkeys.add((m,v))
    for g in sorted(groupkeys,key=str):
        for q in range(3):pool[g,q]=add(('pool',g,q),0,np.inf,False)
    n=len(names);A0e=hstack([A0,csr_matrix((A0.shape[0],n-n0))],format='csr')
    rows=[];los=[];his=[]
    def row(d,lo=-np.inf,hi=np.inf):rows.append(d);los.append(lo);his.append(hi)
    # resolved digit link
    for jx in resolved:
        d={dz[jx,q]:1 for q in range(3)};d[jx]=-1;row(d,0,0)
    # pooled total conditional mass <=3*(unresolved parent mass + tail allocation)
    for g in groupkeys:
        m,v=g;d={pool[g,q]:1 for q in range(3)}
        for jx,w in unresolved_groups.get(g,[]):d[jx]=d.get(jx,0)-3*w
        jt=meta['tidx'].get(g)
        if jt is not None:d[jt]=d.get(jt,0)-3
        row(d,hi=0)
    # every exhausted parent needs all three next children capacity >=1
    for aidx,a in enumerate(s.R):
        je=meta['eidx'][aidx]
        for q in range(3):
            d={je:-1.0}
            for m in range(1,16):
                I=s.bits(m);v=tuple(a[i] for i in I)
                # heavy exact classes
                for h,(es,w) in enumerate(meta['hv'][m]):
                    jx=meta['xidx'].get((m,h,v))
                    if jx is None:continue
                    fw=float(w)
                    if (m&1) and es[0]>=2:
                        if jx in resolved:d[dz[jx,q]]=d.get(dz[jx,q],0)+3*fw
                        # unresolved is represented once through pooled variable below
                    else:d[jx]=d.get(jx,0)+fw
                # tail without extra-3 support is common in all children
                jt=meta['tidx'].get((m,v))
                if jt is not None and not (m&1):d[jt]=d.get(jt,0)+1
                # pooled unresolved/tail deep3 group
                if (m,v) in groupkeys:d[pool[(m,v),q]]=d.get(pool[(m,v),q],0)+1
            row(d,lo=0)
    # historical globally-valid Hunter rows
    hcuts=[]
    if with_hunter:
        logs=json.load(open(hs.CUTLOG));hcuts=[hs.cut_from_sig(x,ctx) for x in logs]
        for d0,rhs in hcuts:row(d0,hi=rhs)
    E=lil_matrix((len(rows),n))
    for rr,d in enumerate(rows):
        for j,v in d.items():E[rr,j]=v
    A=vstack([A0e,E.tocsr()],format='csr');lo=np.r_[lo0,np.asarray(los)];hi=np.r_[hi0,np.asarray(his)]
    mm=dict(meta);mm.update(names=names,dz=dz,pool=pool,resolved=resolved,unresolved_groups=unresolved_groups,nvars=n,nbin=int(sum(integ)),child_rows=len(rows)-len(hcuts),hunter_rows=len(hcuts),digit_cut=digit_cut)
    return np.zeros(n),np.asarray(integ),Bounds(np.asarray(lb),np.asarray(ub)),LinearConstraint(A,lo,hi),mm

def run(digit_cut=.2,tlim=20,relax=False,out=None):
    st=time.time();z=build(.02,digit_cut,True);c,ii,b,con,m=z;buildsec=time.time()-st
    jj=np.zeros_like(ii) if relax else ii
    print('pooled digit_cut',digit_cut,'build',buildsec,'vars',len(c),'bin',int(jj.sum()),'rows',con.A.shape[0],'resolved_x',len(m['resolved']),'poolvars',len(m['pool']),'hunter',m['hunter_rows'],flush=True)
    st=time.time();r=milp(c,integrality=jj,bounds=b,constraints=con,options={'time_limit':tlim,'mip_rel_gap':0,'presolve':True});sec=time.time()-st
    rec={'digit_cut':digit_cut,'relax':relax,'status':int(r.status),'message':str(r.message),'inc':r.x is not None,'sec':sec,'buildsec':buildsec,'gap':getattr(r,'mip_gap',None),'vars':len(c),'binary':int(jj.sum()),'rows':con.A.shape[0],'resolved_x':len(m['resolved']),'poolvars':len(m['pool']),'hunter':m['hunter_rows']}
    if r.x is not None:
        E=np.array([r.x[j] for j in m['eidx'].values()]);rec.update(sum_e=float(E.sum()),max_e=float(E.max()),exhausted_gt_half=int((E>.5).sum()))
        print(' sumE',rec['sum_e'],'maxE',rec['max_e'],'gt.5',rec['exhausted_gt_half'],flush=True)
    print(rec,flush=True)
    if out:json.dump(rec,open(out,'w'),indent=2)
    return rec
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--digit-cut',type=float,default=.2);ap.add_argument('--time',type=float,default=20);ap.add_argument('--relax',action='store_true');ap.add_argument('--out');a=ap.parse_args();run(a.digit_cut,a.time,a.relax,a.out)
