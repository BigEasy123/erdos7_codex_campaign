#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]

def sha256(p: pathlib.Path) -> str:
    h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(1<<20), b''):
            h.update(chunk)
    return h.hexdigest()

def check_hashes() -> bool:
    ok=True
    manifest=ROOT/'artifacts'/'EXACT_SHA256SUMS.txt'
    for line in manifest.read_text().splitlines():
        if not line.strip(): continue
        digest, rel=line.split(None,1)
        rel=rel.lstrip('* ')
        p=ROOT/rel
        got=sha256(p)
        if got != digest:
            print('HASH_FAIL',rel,digest,got); ok=False
        else:
            print('HASH_OK',rel)
    return ok

def check_status_json() -> bool:
    ok=True
    allowed={'PROVED_EXACT','PROVED_SYMBOLIC','NUMERICAL_EVIDENCE','COUNTEREXAMPLE','HEURISTIC','UNKNOWN_TIMEOUT','BLOCKED_DEPENDENCY'}
    for p in sorted((ROOT/'agents').glob('*/status.json')):
        try: d=json.loads(p.read_text())
        except Exception as e:
            print('STATUS_JSON_FAIL',p,e);ok=False;continue
        missing=[k for k in ('track','status','headline','dependencies','artifacts','next_action') if k not in d]
        if missing or d.get('status') not in allowed:
            print('STATUS_SCHEMA_FAIL',p,'missing',missing,'status',d.get('status'));ok=False
        else: print('STATUS_OK',p.relative_to(ROOT))
    return ok

if __name__=='__main__':
    a=check_hashes();b=check_status_json()
    print('CHECKPOINT_VALIDATION=' + ('PASS' if a and b else 'FAIL'))
    sys.exit(0 if a and b else 1)
