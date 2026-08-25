# Gate-1 aggressive report

Starting HEAD: `c3f0b43c5e5b1949c056be1e2dcd4e26681336cb`
Ending HEAD: `c3f0b43c5e5b1949c056be1e2dcd4e26681336cb`

## Status

Gate 1 remains OPEN.

## What was tested

- `scripts/validate_checkpoint.py`
- `src/verify_exact_phase_dual_replay.py`
- `src/verify_state2275_lift_exact.py`
- `src/verify_phase_threshold_farkas.py`

## Fresh exact evidence

```text
CHECKPOINT_VALIDATION=PASS
PHASE_DUAL_CERTIFICATE_STATUS=BLOCKED
REASON=FLOAT_DUAL_FAILED_EXACT_RATIONAL_VERIFICATION
STATE2275_LIFT_STATUS=BLOCKED
REASON=STAGE24_RECOMPUTE_IS_NUMERICAL_NOT_EXACT
```

The repo retains exact finite local artifacts, but no exact Gate-1 closure has been produced.

## Model-domination status

The exact domination theorem required by Gate 1 is not proved. The child-pooled model is still not a theorem object because unresolved deep-3 / tail / pooled coefficients remain tied to numerical assembly and there is no exact proof that every genuine arbitrary-depth continuation is represented in the model.

## >=9 exhausted-parent status

The numerical lower bound is approximately 8.764..., but the exact rational relaxation is still missing. There is no valid exact Farkas certificate showing `sum(e) > 8`.

## Exact phase rejection status

The threshold replay is blocked at tested deltas `1/100`, `1/200`, `1/500`, and `1/1000` because the floating dual fails exact rational verification.

## Strongest structural bypass

No alternative exact/symbolic Gate-1 bypass was proved. The remaining route must be: exact safe-relaxation domination, then exact `sum(e) > 8`, then exact 9-parent contradiction.

## Smallest remaining obstruction

The smallest decisive blocker is an exact, model-safe, rationalized child-pooled relaxation that proves `sum(e) <= 8` infeasible, followed by an exact 9-parent phase contradiction or a valid symbolic bypass.

## QED gate count

`0/6` gates are closed at the current repository state.

## Final conclusion

Gate 1 is not closed. The project remains OPEN until a safe exact relaxation and a mathematically valid exact obstruction are produced and independently replayed.
