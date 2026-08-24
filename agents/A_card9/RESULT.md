# Track A — CARD9 exact closure status

## Verdict

Status: **NUMERICAL_EVIDENCE**

The CARD9 path is now repository-portable and the missing helper has been restored. The phase oracle exactly replays five saved rejected 9-parent sets, and a fresh sparse iteration rejects another 9-set. This is numerical evidence only, not a closure of the 9-parent layer.

## Reproduced evidence

1. The repository-relative verifier now passes, including core import and helper existence.
2. The restored [src/eonly_card9_hybridprefix.py](src/eonly_card9_hybridprefix.py) derives only conservative threshold subset caps from the dual inequality.
3. Five saved rejected sets replayed with exact matching floating values; maximum absolute difference was `0.0`.
4. A fresh sparse iteration produced `phi = 0.10147076397503477`, added 42 symmetry nogoods, and ended at `ITER_LIMIT`; no infeasibility was inferred.
5. The 42 symmetry maps pass permutation and parent-index preservation checks; 32 recorded rejected candidates all have positive phase margins, with minimum `phi = 0.08225417337323754`.

## Required fix before any CARD9 theorem claim

A valid theorem claim must satisfy the checklist in [agents/A_card9/BRIEF.md](agents/A_card9/BRIEF.md):

- repository-relative paths; 
- reconstruct/validate the missing helper module from the mathematical derivation;
- validate the phase oracle on saved rejected sets;
- check the 42 symmetry maps and exact nogoods;
- produce an optimizer-free exact certificate or a genuine phase-feasible 9-parent witness.

The headline claim must remain `NUMERICAL_EVIDENCE` until an optimizer-free exact certificate or a genuine phase-feasible witness is produced and Track E audits it.

## Repository-local verifier

The script [agents/A_card9/verify_repo_relative.py](agents/A_card9/verify_repo_relative.py) now passes. The phase replay and symmetry checks were run as focused executable validations from the repository root.

## Impact on the project

This does not prove the 9-parent layer is feasible or empty. The next theorem-level task is to continue the sparse search, retain a standalone exact certificate if the master closes, and have Track E audit the helper derivation, symmetry handling, and every generated nogood.
