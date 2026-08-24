# Track A — CARD9 exact closure status

## Verdict

Status: **BLOCKED_DEPENDENCY**

The exact CARD9 path is not yet valid as a theorem-producing implementation. The active solver code is still using stale absolute filesystem paths and imports a missing helper module that the checkpoint relies on for valid Benders-derived phase cuts. This is a repository portability and reconstruction failure, not a mathematical closure of the 9-parent layer.

## Reproduced evidence

1. The file [src/card9_sparse_exact_benders.py](src/card9_sparse_exact_benders.py) still contains absolute path assumptions of the form `/mnt/data/erdos2275`, which are not valid in this repo checkout.
2. The file [src/eonly_phase_benders.py](src/eonly_phase_benders.py) imports `eonly_card9_hybridprefix` and also assumes the same stale working directory, while the repository contains no corresponding helper file under [src](src).
3. The checkpoint files in [artifacts/current_state](artifacts/current_state) show that the exact-cardinality pass is a saved snapshot, not an independently replayed finite proof. The available records show many rejected 9-sets with positive phase margin, but no exact closure certificate and no valid helper to replay the phase oracle from the repository itself.
4. The phase-run ledger [artifacts/current_state/EONLY_PHASE_BENDERS.json](artifacts/current_state/EONLY_PHASE_BENDERS.json) only reports `ITER_LIMIT` and positive `phi` values, which is consistent with a partial numerical search, not exact infeasibility.

## Required fix before any CARD9 theorem claim

A valid theorem claim must satisfy the checklist in [agents/A_card9/BRIEF.md](agents/A_card9/BRIEF.md):

- repository-relative paths; 
- reconstruct/validate the missing helper module from the mathematical derivation;
- validate the phase oracle on saved rejected sets;
- check the 42 symmetry maps and exact nogoods;
- produce an optimizer-free exact certificate or a genuine phase-feasible 9-parent witness.

Until those are satisfied, the headline claim must remain `BLOCKED_DEPENDENCY`.

## Repository-local verifier

The script [agents/A_card9/verify_repo_relative.py](agents/A_card9/verify_repo_relative.py) checks the exact portability issue and confirms that the active code is not yet repository-relative. It is the minimal verification artifact required to prevent a false theorem claim.

## Impact on the project

This does not prove the 9-parent layer is feasible or empty. It only establishes that the current solver stack is not yet a valid witness-based proof object. The next theorem-level task is to rebuild the missing phase oracle from the derivation in [src/eonly_phase_benders.py](src/eonly_phase_benders.py) and to validate it against the saved rejected sets before any CARD9 claim is promoted.
