# Gate 1: state-2275 correlated arbitrary-depth closure

Status: OPEN, not proved.

## Required implication

The required proof chain is:

```text
genuine arbitrary-depth bad continuation
    => safe exact low-prime/child representation
    => at least 9 exhausted shallow parents
    => no legal exact 9-parent obstruction
    => contradiction.
```

This chain is not yet proved in the current repository state.

## Fresh evidence

At current HEAD `c3f0b43c5e5b1949c056be1e2dcd4e26681336cb`:

- `scripts/validate_checkpoint.py` reports `CHECKPOINT_VALIDATION=PASS`.
- `src/verify_exact_phase_dual_replay.py` reports:
  - `PHASE_DUAL_CERTIFICATE_STATUS=BLOCKED`
  - `REASON=FLOAT_DUAL_FAILED_EXACT_RATIONAL_VERIFICATION`
- `src/verify_state2275_lift_exact.py` reports:
  - `STATE2275_LIFT_STATUS=BLOCKED`
  - `REASON=STAGE24_RECOMPUTE_IS_NUMERICAL_NOT_EXACT`

Thus the exact Gate-1 closure has not been established.

## What is proved

The repository contains real exact finite evidence for the local low-prime layer, including exact Stage-18 and state-2275 replay artifacts, and an exact Hunter replay. Those are genuine local finite exact results, but they do not yet establish the arbitrary-depth state-2275 closure required by Gate 1.

## What remains open

The critical missing steps are:

1. Exact domination of the child-pooled model over the genuine arbitrary-depth continuation family.
2. Exact proof that `sum(e) <= 8` is impossible in the safe rational relaxation.
3. Exact 9-parent phase threshold infeasibility or exact finite obstruction.
4. Exact certificate for the 9-set family that kills the remaining phase-limited obstruction.

## Current conclusion

Gate 1 is not closed. The exact finite low-prime certificate chain is valid, but the arbitrary-depth/child-pooling domination and the exact 9-parent obstruction are still missing. Without that, the project remains OPEN.
