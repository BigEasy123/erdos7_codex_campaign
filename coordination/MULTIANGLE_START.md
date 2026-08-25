# Multi-angle start ledger

Starting commit: `ace6ab5880982fc9248e52fe222d84156fce3bf2`

Current status summary:
- CARD9 status: `NUMERICAL_EVIDENCE`
- Exact phase certificate: absent
- Repository portability: passes (`python agents/A_card9/verify_repo_relative.py`)
- Exact checkpoint validation: passes (`python scripts/validate_checkpoint.py`)
- Raw floating SciPy dual for a saved rejection failed exact Fraction replay in `src/verify_card9_phase_certificate.py`
- The phase LP remains a pooled child-capacity + Hunter relaxation, not an exact infeasibility-Farkas object

Smallest obstruction:
- The current phase model is assembled from float-valued coefficients in `src/state2275_child_pooled_master.py` and `src/eonly_phase_benders.py`.
- The exact mathematical origin of many coefficient families has not yet been frozen into an optimizer-independent exact rational representation.
- The missing proof object is not a numerical dual failure alone; the exact LP is not yet represented in a way that can be replayed without the optimizer.

Required next proof gate:
- Build an exact rational model with coefficient families classified as integer incidence, rational reciprocal mass, exact HN constants, exact BBMST coefficients, or BLOCKED_DEPENDENCY.
- Rebuild the phase dual with documented sign conventions and a verifying routine that accepts only exact arithmetic.
- Only then may a phase rejection become a valid theorem-level certificate.

This note is intentionally conservative and stops at the current audited obstruction.
