import pathlib,sys,json,time,os,argparse
import numpy as np
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import state2275_hunter_benders_v2 as hb
CURRENT = ROOT / 'artifacts' / 'current_state'
CUTLOG = str(CURRENT / 'HUNTER_V2_CUTLOG.json')
STATE = str(CURRENT / 'HUNTER_V2_STATE.json')
WIT = str(CURRENT / 'TOWER_HEAVY_BBMST_V3_002_WITNESS.json')

def ctx0():
 ctx=hb.build_context(.02,False);ctx[0][:]=0;return ctx

def cut_from_sig(sig,ctx):
 c,ii,bd,A0,lo0,hi0,meta,cand,tailvars=ctx
 aset=set(sig['active'])
 active=[q for q in cand[sig['aidx']] if q[0] in aset]
 d,rhs,_=hb.make_cut(sig['aidx'],active,cand[sig['aidx']],tailvars[sig['aidx']],meta)
 return d,rhs

def init():
 ctx=ctx0(); c,ii,bd,A0,lo0,hi0,meta,cand,tailvars=ctx
 w=json.load(open(WIT));sel={(int(z['m']),int(z['h']),tuple(z['v'])) for z in w['heavy_selected']}
 tload={(int(z['m']),tuple(z['v'])):float(z['load']) for z in w['tail']};jid_tail={j:tload.get((m,tuple(v)),0.0) for (m,v),j in meta['tidx'].items()}
 logs=[];seen=set()
 for aidx in w['exhausted']:
  active=[q for q in cand[aidx] if (q[3],q[4],tuple(meta['names'][q[0]][-1])) in sel]
  cap,_=hb.hunter_cap(active,sum(jid_tail.get(j,0.0) for j in tailvars[aidx]))
  if float(cap)<1-1e-10:
   sig={'aidx':aidx,'active':sorted(q[0] for q in active)};key=(aidx,tuple(sig['active']))
   if key not in seen:seen.add(key);logs.append(sig)
 json.dump(logs,open(CUTLOG,'w'));json.dump({'iter':0,'records':[],'status':'READY','cuts':len(logs)},open(STATE,'w'),indent=2)
 print('initialized',len(logs))

def step(tlim=22):
 ctx=ctx0(); c,ii,bd,A0,lo0,hi0,meta,cand,tailvars=ctx
 logs=json.load(open(CUTLOG));cuts=[cut_from_sig(x,ctx) for x in logs]
 stt=json.load(open(STATE));it=stt['iter']
 st=time.time();r=hb.solve_with_cuts(ctx,cuts,tlim);sec=time.time()-st
 print('iter',it,'status',r.status,r.message,'inc',r.x is not None,'sec',sec,'cuts',len(cuts),flush=True)
 if r.x is None:
  stt['status']='INFEASIBLE' if r.status==2 else 'UNKNOWN';stt['solver_status']=int(r.status);stt['message']=r.message;json.dump(stt,open(STATE,'w'),indent=2);return
 ex=[a for a,j in meta['eidx'].items() if r.x[j]>.5];invalid=[];pot=[];new=[];seen={(z['aidx'],tuple(z['active'])) for z in logs}
 for aidx in ex:
  active=[q for q in cand[aidx] if r.x[q[0]]>.5];tailmass=sum(r.x[j] for j in tailvars[aidx]);cap,forest=hb.hunter_cap(active,tailmass)
  if float(cap)>=1-1e-10:pot.append((aidx,float(cap),len(active),len(forest)))
  else:
   invalid.append((aidx,float(cap),len(active),len(forest)))
   sig={'aidx':aidx,'active':sorted(q[0] for q in active)};key=(aidx,tuple(sig['active']))
   if key not in seen:seen.add(key);new.append(sig)
 rec={'it':it,'exhausted':len(ex),'potential':len(pot),'invalid':len(invalid),'newcuts':len(new),'cuts_before':len(logs),'cuts_after':len(logs)+len(new),'sec':sec,
      'min_invalid_cap':min([x[1] for x in invalid],default=1.0),'max_invalid_cap':max([x[1] for x in invalid],default=1.0)}
 stt['records'].append(rec);stt['iter']=it+1;logs.extend(new);stt['cuts']=len(logs);stt['status']='READY'
 if not invalid:
  stt['status']='HUNTER_FEASIBLE_BBMST_BAD';stt['exhausted']=ex;stt['potential']=pot
  hs=[]
  for (m,h,v),j in meta['xidx'].items():
   if r.x[j]>.5:hs.append({'m':m,'h':h,'v':list(v),'es':list(meta['hv'][m][h][0]),'weight':float(meta['hv'][m][h][1]),'j':j})
  tails=[]
  for (m,v),j in meta['tidx'].items():
   if r.x[j]>1e-9:tails.append({'m':m,'v':list(v),'load':float(r.x[j]),'j':j})
  stt['heavy_selected']=hs;stt['tail']=tails
 json.dump(logs,open(CUTLOG,'w'));json.dump(stt,open(STATE,'w'),indent=2)
 print(rec,flush=True)

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--init',action='store_true');ap.add_argument('--time',type=float,default=22);a=ap.parse_args()
 if a.init:init()
 else:step(a.time)
