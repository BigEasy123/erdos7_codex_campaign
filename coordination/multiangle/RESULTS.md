# Multi-angle results

## Verified facts
- Starting commit: `ace6ab5880982fc9248e52fe222d84156fce3bf2`
- `python scripts/validate_checkpoint.py` passes.
- `python agents/A_card9/verify_repo_relative.py` passes.
- The repo is portable and the helper recovery is valid.

## Current non-proof status
- The phase rejection is not valid as an exact certificate.
- The last saved dual failed exact `Fraction` replay.
- The phase LP is therefore still a numerical lower-bound heuristic, not a theorem object.

## Best current route
- Freeze the mathematical coefficient families of the phase LP into exact rational objects.
- Then derive a dual lower bound and verify it against a strong exact arithmetic replay.

## Most likely dependency barrier
- The exact source formulas for the pooled child-capacity rows and Hunter/BBMST row families are still not available in a canonical exact representation.
- This must be repaired before any fully exact cardinality-9 theorem can be claimed.
