# Exact Phase Bridge: Four-Loop Log

Date: 2026-08-25
Repository HEAD: `a6eb306f3a06355e2a8f1bf3ce936c96ac4fdf64`

This log records exactly four loops, as requested. It does not promote numerical output to an exact theorem.

## Loop 1: Structural Replay

Command: `python src/verify_exact_phase_dual_replay.py`

Result:

- `PHASE_DUAL_CERTIFICATE_STATUS=BLOCKED`
- `REASON=FLOAT_DUAL_FAILED_EXACT_RATIONAL_VERIFICATION`
- primal objective: `0.05402950069357493`
- multiplier count: `44149` after the attempted upper-bound append

Finding: `rational_system()` already emits explicit finite upper-bound rows. Appending `result.upper.marginals` therefore double-counted rows and was removed.

## Loop 2: Residual Diagnosis

Command: one-off exact residual diagnostic for the saved rejected 9-set.

Result:

- rational-system rows: `29980`
- multipliers after double-counting attempt: `44149`
- `min_lhs=-459039415855125603/5000000000000000000`
- negative reduced-cost entries: `756`
- exact check: `False`

Finding: the failure is not caused by missing upper-bound multipliers. The floating dual values do not satisfy the exact rational reduced-cost inequalities.

## Loop 3: Guarded Replay

Command: `python src/verify_exact_phase_dual_replay.py`

Result:

- row-count guard passed implicitly: `29980` rows and `29980` inequality multipliers
- `PHASE_DUAL_CERTIFICATE_STATUS=BLOCKED`
- `REASON=FLOAT_DUAL_FAILED_EXACT_RATIONAL_VERIFICATION`
- primal objective: `0.05402950069357493`

Finding: the dual-row accounting is consistent, but no optimizer-free rational certificate exists yet.

## Loop 4: Final Validation Stack

Command: `python scripts/validate_checkpoint.py; python agents/A_card9/verify_repo_relative.py; python src/verify_exact_phase_dual_replay.py; python src/verify_state2275_lift_exact.py`

Result:

- `CHECKPOINT_VALIDATION=PASS`
- `CARD9_REPO_RELATIVE_CHECK=PASS`
- `PHASE_DUAL_CERTIFICATE_STATUS=BLOCKED`
- phase reason: `FLOAT_DUAL_FAILED_EXACT_RATIONAL_VERIFICATION`
- `STATE2275_LIFT_STATUS=BLOCKED`
- lift reason: `STAGE24_RECOMPUTE_IS_NUMERICAL_NOT_EXACT`

## Code Change

[src/verify_exact_phase_dual_replay.py](../src/verify_exact_phase_dual_replay.py) now contains a fail-closed row-count guard for the exact-system/solver-dual mapping.

## Final Status

The four-loop task is complete. The exact CARD9 phase dual and the exact 7,637-state lift remain open. No QED claim is made.
