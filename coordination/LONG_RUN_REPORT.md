# Long-run integration report

Date: 2026-08-24

## Repository baseline

Starting commit: `0b547d0a5b3afbf14a73ffa0c4655125a28fb2ce`
Ending commit: the integration checkpoint commit created below; retrieve its immutable SHA with `git rev-parse HEAD`.

## Commands run

- `python scripts/validate_checkpoint.py`
- `python agents/A_card9/verify_repo_relative.py`
- `python -m py_compile src/eonly_card9_hybridprefix.py src/eonly_phase_benders.py src/card9_sparse_exact_benders.py src/hunter_v2_step.py src/state2275_child_pooled_master.py`
- Repository-relative phase replay on the first five records in `artifacts/current_state/CARD9_SPARSE_EXACT_RECORDS.json`
- One bounded sparse CARD9 iteration via `card9_sparse_exact_benders.run(1)`
- 42-map permutation/preservation and rejected-margin checks
- Pylance diagnostics on the repaired CARD9 files

## Results obtained

Exact/replayable checks:

- Immutable exact checkpoint validation: PASS.
- CARD9 repository-relative verifier: PASS.
- Five saved phase margins replayed with maximum absolute difference `0.0`.
- All 42 symmetry maps passed permutation and shallow-index preservation checks.
- All 32 currently recorded rejected candidates have positive phase margins; minimum `phi = 0.08225417337323754`.

These are validation milestones, not a CARD9 closure theorem. The phase values are floating LP outputs.

## Numerical-only results

- Fresh sparse iteration: rejected a 9-set with `phi = 0.10147076397503477`.
- Added 42 symmetry nogoods; persisted 3,192 total nogoods.
- Iteration ended at `ITER_LIMIT`; no infeasibility conclusion was drawn.
- Stored pooled LP objective remains `8.76416923252369...`, but its JSON record contains no constraint matrix or dual multipliers.

## Blockers and killed approaches

- The original missing-helper and stale-path blocker is repaired.
- Exactification of the `8.764...` bound is currently blocked by missing matrix/dual certificate data, not by a solver result.
- The reconstructed compact helper yields only conservative threshold consequences. It does not retroactively certify the historical compact database or reproduce an exact closure certificate.

## Smallest obstruction to QED

The smallest hard obstruction is still arbitrary-depth CARD9/state-2275 closure: there is neither an optimizer-independent exact infeasibility certificate nor a genuine phase-feasible survivor. The global 7,637-state lift and repeated-power high-prime interfaces remain open as well.

## Remaining theorem gates

All six QED gates remain open at project level. Local Stage-18, K2, and 284-case replay artifacts are exact, but they do not imply arbitrary-depth closure, the global lift, or the repeated-power interfaces.

## Independent referee commands

- `python scripts/validate_checkpoint.py`
- `python agents/A_card9/verify_repo_relative.py`
- Re-run the five-record phase replay described above.
- Re-run the 42-map and positive-margin checks.
- Inspect `agents/A_card9/RESULT.md` and `proof/MASTER_PROOF_SKELETON.md`.

## Highest-value next step

Rebuild the pooled LP with a restartable repository-local builder that saves the full rationalizable matrix, row bounds, variable ordering, and solver dual output. Then construct an optimizer-free rational dual verifier for `sum(e) > 8`, without treating the floating optimum as exact.

## Exact-certificate run update

The deterministic CARD9 phase builder was serialized into [artifacts/card9_exact/CARD9_MODEL_SCHEMA.json](../artifacts/card9_exact/CARD9_MODEL_SCHEMA.json): 14,500 variables and 17,898 rows. Rational-dual tooling was added in [src/card9_exact_phase.py](../src/card9_exact_phase.py) and [src/verify_card9_phase_certificate.py](../src/verify_card9_phase_certificate.py). On the first saved rejection, the raw floating SciPy dual failed exact Fraction verification, so no certificate was created. This confirms the remaining blocker is certificate reconstruction, not missing execution plumbing.

This update was checkpointed in the exact-certificate tooling commit; retrieve the ending SHA with `git rev-parse HEAD`.
