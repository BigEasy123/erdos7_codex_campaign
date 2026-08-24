#!/usr/bin/env python3
from fractions import Fraction as F
from pathlib import Path
import json,sys,argparse,time
HERE=Path('/mnt/data/erdos2275');sys.path.insert(0,str(HERE));import k2_farkas_unknowns as k
D=json.load(open(HERE/'STATE2275_K2_DEPTH1_FARKAS_228.json'))['certificates']
ap=argparse.ArgumentParser();ap.add_argument('cases',nargs='+',type=int);a=ap.parse_args();sel=[z for z in D if z['case'] in set(a.cases)]
worst=None;mnall=None;maxsup=0;st=time.time()
for z in sel:
 rows,n,meta=k.build_rows(z['case'],int(z['M'],16));den=int(z['den']);col=[F(0)]*n;rhs=F(0)
 for i,num in z['active']:
  lam=F(int(num),den);co,b,_=rows[int(i)];rhs+=lam*b
  for j,q in co.items():col[j]+=lam*q
 mn=min(col);assert rhs==F(int(z['rhs_num']),int(z['rhs_den']));assert mn==F(int(z['min_num']),int(z['min_den']));assert rhs<0 and mn>=0
 worst=rhs if worst is None or rhs>worst else worst;mnall=mn if mnall is None or mn<mnall else mnall;maxsup=max(maxsup,len(z['active']))
print('CASES',a.cases,'N',len(sel),'PASS','worst_rhs',float(worst),'mincol',float(mnall),'maxsup',maxsup,'sec',time.time()-st)
