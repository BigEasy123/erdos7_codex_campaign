# Dependency map

## Exact-environment dependencies

- [scripts/validate_checkpoint.py](../scripts/validate_checkpoint.py) validates the immutable exact archive.
- [artifacts/exact/STATE2275_FULL_EXACT_REPLAY.txt](../artifacts/exact/STATE2275_FULL_EXACT_REPLAY.txt) is the current exact replay for the state-2275 local proof path.
- [artifacts/exact/FULLCOVER_71x4_FARKAS_EXACT_REPLAY.txt](../artifacts/exact/FULLCOVER_71x4_FARKAS_EXACT_REPLAY.txt) is the exact replay for the 284-case common-U theorem.

## Local state-2275 proof path

- A-card9 path: [agents/A_card9/BRIEF.md](../agents/A_card9/BRIEF.md)
  - Depends on a valid phase oracle and an optimizer-independent closure certificate or survivor witness.
  - Status: numerical evidence; portability and five-record phase replay checks pass, but exact phase dual certification is open.
- B-structure path: [agents/B_structure/BRIEF.md](../agents/B_structure/BRIEF.md)
  - Intended to explain slab concentration and rule out or shrink the near-extremal packet family.
  - Status: no theorem-level output yet.
- C-common-U path: [agents/C_commonU/BRIEF.md](../agents/C_commonU/BRIEF.md)
  - Intended to turn exact depth-two common-U structure into a repeated-power descent.
  - Status: no theorem-level output yet.
- D-HN/BBMST path: [agents/D_HN_BBMST/BRIEF.md](../agents/D_HN_BBMST/BRIEF.md)
  - Intended to provide the correlated analytic bridge.
  - Status: no theorem-level output yet.
- E-referee path: [agents/E_referee/BRIEF.md](../agents/E_referee/BRIEF.md)
  - Required to audit every nontrivial dependency before promotion.
  - Status: not yet produced.
- F-global path: [agents/F_global_interface/BRIEF.md](../agents/F_global_interface/BRIEF.md)
  - Intended to handle the lift from state 2275 to the full canonical family and the 13–73/>73 handoff.
  - Status: not yet produced.

## Dependency graph

```text
exact replay / Farkas certificates
        |
        v
state-2275 local obstruction (safe exact evidence only)
        |
        +--> A: CARD9 closure or survivor fidelity
        |        |
        |        +--> B: slab/concentration structural lemma
        |        +--> C: common-U / blocker descent
        |        +--> D: HN / BBMST analytic socket
        |        +--> E: independent referee
        |        \--> F: global lift / high-prime interface
        |
        +--> E must mark every dependency AUDITED_EXACT before any QED promotion
```

## Current verdict

No dependency on the final proof path is currently marked AUDITED_EXACT. Therefore the project remains OPEN and no theorem claim is promoted.
