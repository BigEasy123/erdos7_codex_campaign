# Aggressive Finish Attack Ledger

Date: 2026-08-25
Starting HEAD: `bd8fac2a7cca0ff9dbc82001982bfdce181dd8d`
Ending HEAD: `bd8fac2a7cca0ff9dbc82001982bfdce181dd8d`

All statuses below are conservative. Numerical solver output is not promoted to a theorem.

| Attack | Hypothesis / decisive test | Result | Status | Derivative idea |
|---|---|---|---|---|
| 1. Phase threshold Farkas | Test `t <= 1/100, 1/200, 1/500, 1/1000` using rational-system rows and a replayable ray | All four exact checks false | `BLOCKED_DEPENDENCY` | Recover exact pooled coefficients before ray reconstruction |
| 2. Minimum exhaustion threshold | Add `sum(e) <= 8` to an exact safe pooled model | Exact safe model is not serialized; pooled builder is float-dependent | `OPEN` | Build a smaller exact relaxation from source formulas |
| 3. Model safety | Prove genuine continuation maps into every pooled inequality | No domination proof; unresolved deep-3/tail groups remain | `BROKEN` | Prove each row direction before any dual use |
| 4. Rational basis recovery | Reconstruct a HiGHS basis over Q | No exact basis object or exact matrix serialization available | `OPEN` | Serialize deterministic rational matrix and active basis |
| 5. Dual repair LP | Repair 756 negative reduced-cost entries from the float dual | Residual diagnostic found `756` negative exact reduced costs; no repair certificate | `OPEN` | Support-preserving exact feasibility LP after source recovery |
| 6. Short symbolic phase lemma | Compress phase contradiction to child/Hunter/tail inequalities | No symbolic derivation completed | `OPEN` | Inspect exact source rows only after model safety closes |
| 7. Exact CRT union | Replace Hunter with exact pair/triple/higher CRT union | No complete normalized signature computation in this run | `OPEN` | Target low-margin packets after exact source serialization |
| 8. Three-child convex hull | Enumerate all normalized terminal order types | `90` orbits classified; `23` squarefree | `NUMERICAL_EVIDENCE` | Derive facets for repeated-power types 85--90 |
| 9. Low-margin classification | Cluster rejected CARD9 packets by slab/support/triangle type | Existing records show concentration, not a finite proof family | `NUMERICAL_EVIDENCE` | Canonicalize all saved packets and prove coverage of clusters |
| 10. Common-U expansion | Extend the audited 284-case theorem to dangerous packets | Existing verifier blocked by missing `depth2_fixed_corrected` module | `BROKEN` | Restore exact historical dependency or rederive the finite model |
| 11. Repeated-power descent | Close types 85--90 by q-frame/blocker/pivot descent | Structural ingredients exist, but no closed theorem/replay | `OPEN` | Produce a per-type exact counterexample search and proof obligations |
| 12. Least-counterexample descent | Compress a feasible CARD9 packet to lower LCM/support | No preservation proof for a proposed compression | `OPEN` | Freeze candidate packets and check oddness/distinctness explicitly |
| 13. SAT/PB master | Encode exact `sum(e)=9` constraints and certify UNSAT | No complete exact constraint set; no proof object | `OPEN` | Use only independently validated exact cuts |
| 14. Certified branch tree | Close every parent-bit leaf by exact reason | No exact leaf partition exists | `OPEN` | Start after threshold or structural leaf certificates exist |
| 15. Smaller exhaustion relaxation | Discard unnecessary variables while preserving continuation inclusion | No exact safe reduced model identified | `OPEN` | Target only child capacity and integer exhaustion |
| 16. Direct HN restart | Bypass CARD9 with branchwise state-2275 HN | Stage-18 exact HN gate passes, but arbitrary-depth correlation is absent | `NUMERICAL_EVIDENCE` | Preserve child/support masks branchwise |
| 17. Localized BBMST distortion | Use actual residue geometry instead of tower inflation | No proof-level margin obtained | `OPEN` | Couple distortion to exact CRT signatures |
| 18. Shearer/cluster expansion | Test sharper dependency criterion | No validated dependency graph/criterion output | `OPEN` | Kill unless a strict exact margin appears |
| 19. All 7,637 invariants | Recompute all canonical states | Script blocked by missing `/mnt/data/stage18_bbmst_7637_partials.txt` | `BLOCKED_DEPENDENCY` | Make input path repository-relative and restore source data |
| 20. Statewise exact certificates | Certify each canonical state independently | No state bundle or exact all-state verifier | `OPEN` | First obtain canonical input and exact invariant schema |
| 21. Prime 13--73 handoff | Produce exact stagewise interface | No complete exact artifact or verifier | `PLAUSIBLE_UNAUDITED` | Specify incoming/outgoing invariant per prime |
| 22. >73 theorem mapping | Map published termination theorem hypotheses | No theorem citation/mapping package in repository | `PLAUSIBLE_UNAUDITED` | Write a hypothesis-by-hypothesis imported theorem record |
| 23. Front-end reduction audit | Recheck leastness, support, compression, pivot | Referee classifies it `PLAUSIBLE_UNAUDITED` | `PLAUSIBLE_UNAUDITED` | Build preservation ledger for every descent |
| 24. Literature bypass | Replace CARD9 with a published structural route | No imported theorem with checked hypotheses found in repository | `OPEN` | Search only after notation and hypotheses are explicit |
| 25. Weakest local handoff | Determine what the high-prime stage actually needs | Not established; current project target remains stronger than documented handoff | `OPEN` | Formalize the outgoing statistic before local overproof |

## Fresh executable evidence

- `python src/verify_phase_threshold_farkas.py`: `PHASE_THRESHOLD_EXACT_REPLAY=BLOCKED` at all four deltas.
- `python src/verify_exact_phase_dual_replay.py`: `FLOAT_DUAL_FAILED_EXACT_RATIONAL_VERIFICATION`.
- `python src/verify_stage18_restart_hn_gate.py`: exact Stage-18 gate passes.
- `python src/state2275_tower_heavy_bbmst_exact.py`: exact model dimensions/support match.
- `python src/state2275_hunter_exact.py`: `HUNTER_EXACT_REPLAY=PASS 1308 records`.
- `python src/classify_triangle_all_order_types.py`: all 90 order types enumerated; 23 squarefree.
- `python src/stage24_recompute_7637_fast.py`: blocked by missing `/mnt/data` input.
- `python src/state2275_child_pooled_exact.py`: blocked by missing `build` API in `state2275_hunter_benders_v2`.
- `python src/verify_full_state2275_exact.py`: `STATE2275_FULL_EXACT_REPLAY=PASS`.

## Promotion rule

No attack in this ledger closes a QED gate. The strongest exact results remain the pre-existing low-prime and Hunter replays.
