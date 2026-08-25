# Multi-angle idea ledger

## Ledger state
- Starting HEAD: `ace6ab5880982fc9248e52fe222d84156fce3bf2`
- Primary status: `NUMERICAL_EVIDENCE`
- Current bottleneck: exact rational phase dual is missing; all numerical evidence remains non-proof.

## Angle 1 — Rebuild the phase LP from rational source formulas
- Hypothesis: the phase model can be rebuilt from exact integer/rational families rather than float serialization.
- Method: classify row families into exact inc/reciprocals/HN/BBMST or `BLOCKED_DEPENDENCY`.
- Result: not yet exact; current source still stores pooled row coefficients in floating arithmetic.
- Status: `BLOCKED_DEPENDENCY`

## Angle 2 — Exact dual reconstruction
- Hypothesis: the active-set or sparse dual basis over the phase LP can be recovered exactly after rationalization.
- Method: derive dual algebraically and replay with `Fraction`/exact arithmetic.
- Result: no exact certificate yet; raw dual fails verification.
- Status: `NUMERICAL_EVIDENCE`

## Angle 3 — Symbolic tail certificate
- Hypothesis: a short human-readable inequality may replace the full dual.
- Method: search for compressed weighted-child/Hunter inequality.
- Result: not yet obtained.
- Status: `OPEN`

## Angle 4 — SAT/CP exact certificate
- Hypothesis: the 9-set master can be encoded into a finite UNSAT certificate.
- Method: branch-and-bound or PB encoding with proof object.
- Result: not yet attempted beyond the current LP checkpoint.
- Status: `OPEN`

## Angle 5 — near-extremal 9-set classification
- Hypothesis: low-margin sets concentrate in a structured family that can be classified.
- Method: orbit-scan and residue-pattern clustering.
- Result: partially observed; no exact theorem yet.
- Status: `NUMERICAL_EVIDENCE`

## Angle 6 — common-U / triangle / blocker logic
- Hypothesis: repeated-power packets can be forced into a provable blocker geometry.
- Method: extend exact 284-case common-U logic to near-extremal survivors.
- Result: not yet mature.
- Status: `OPEN`

## Angle 7 — exact CRT union bounds
- Hypothesis: exact residual union structure is stronger than Hunter bounds.
- Method: exact union/inclusion-exclusion over residual LCM classes.
- Result: not yet implemented.
- Status: `OPEN`

## Angle 8 — next-3 child dispersion
- Hypothesis: exact child capacity inequalities can exclude bad 9-set patterns.
- Method: characterize the three-child capacity region for heavy classes.
- Result: not yet implemented.
- Status: `OPEN`

## Angle 9 — exact 8.764 bound
- Hypothesis: the pooled minimum-exhaustion LP can be rationalized and certified.
- Method: exact LP dual or exact finite certificate.
- Result: current bound is numerical only.
- Status: `NUMERICAL_EVIDENCE`

## Angle 10 — arbitrary-depth interface
- Hypothesis: the finite child/Hunter model exactly dominates arbitrary-depth continuations.
- Method: proof of relaxation direction and dependency audit.
- Result: not yet proved.
- Status: `OPEN`
