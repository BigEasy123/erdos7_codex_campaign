# CARD9 phase dual: exact sign convention

## 1. Statement of the primal phase model

The phase model is a minimization problem of the form

```text
min  t
subject to  A z <= b,
            0 <= z <= u,
            t >= 0,
```

where the objective is the scalar exhaustion slack `t` and the residual phase variables encode the continuity of child capacity / support / Hunter constraints. The crucial fact is that the solver output is not itself a proof object: the linear program is built from float coefficients, and an output dual must be checked against an exact rational model before it may be called a certificate.

## 2. Exact dual derivation

For a generic linear program

```text
min c^T x
subject to A x <= b,
            x >= 0,
```

the dual is

```text
max b^T y
subject to A^T y <= c,
            y >= 0.
```

The sign convention is the one used in standard `linprog` minimization with `A_ub * x <= b_ub` and the objective `c^T x`. In this repository, the phase oracle records the dual multipliers from the solver as a vector attached to the inequality side, and the project script then checks a lower bound by translating the sign to the exact scalar value

```text
lower_bound = -sum_i y_i * b_i
```

if the rows are expressed as `A_i x <= b_i` and the multipliers are all nonnegative.

The exact mapping is:

- if the phase inequality is written as `A_i x <= b_i`, then the dual multiplier `y_i` is nonnegative;
- if the row is written as `-A_i x >= -b_i`, the transposed sign flips accordingly;
- if the primal constraint is a nonnegativity upper bound `x_j <= u_j`, we add an explicit row and track the sign in the exact verifier.

In the current repository implementation, the raw floating dual is only useful as a support vector. It is not a valid exact certificate until each coefficient and each row sign is replayed over the rational field.

## 3. Why the current phase rejection is not a valid proof object

The project has established the following facts:

- the phase LP is repository-portable and the checkpoint scripts pass;
- the current objective value is positive for several saved 9-parent rejections;
- the raw floating dual fails exact `Fraction` verification;
- therefore the dual is not an optimizer-independent exact proof.

This means the current status remains `NUMERICAL_EVIDENCE`, not `PROVED_EXACT`.

## 4. Correct next step

The next mathematically sound route is not to rationalize the final floating dual. The correct route is to rebuild the phase LP from exact rational source formulas and then derive the exact dual for that exact rational model. Only after the exact dual passes an optimizer-free replay should a subset rejection be promoted to a certified theorem.
