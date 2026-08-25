# Failed routes

## 1. Float dual raw replay
- Route: extract the floating SciPy dual and convert coefficients via `Fraction(str(value))`.
- Result: rejected by exact verification; therefore not a proof object.
- Status: `BROKEN`

## 2. Treating a positive phase optimum as Farkas infeasibility
- Route: infer exact rejection from a positive phase optimum alone.
- Result: invalid; the project documentation explicitly distinguishes this from a dual Farkas certificate.
- Status: `BROKEN`

## 3. Blind rationalization of the final float matrix
- Route: solve a floating LP and then rationalize every coefficient in the result.
- Result: acceptable only if exact coefficient provenance is known; otherwise it produces a fake proof.
- Status: `BROKEN`

## 4. “Current solver status says infeasible” shortcut
- Route: use solver status codes as theorem-level evidence.
- Result: invalid under the project proof discipline.
- Status: `BROKEN`
