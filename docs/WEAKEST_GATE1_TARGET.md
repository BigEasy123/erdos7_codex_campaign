# Weakest Gate-1 target

Status: OPEN.

The current model is trying to prove more than the final argument needs. The strongest available exact target is not the exact optimum of the numerical phase LP, but the weakest exact statement that still forces the arbitrary-depth contradiction.

## Candidate exact target

Show that every genuine arbitrary-depth continuation satisfies:

```text
sum_a e_a > 8.
```

Equivalently, in integer terms:

```text
at least 9 exhausted shallow parents.
```

This is sufficient to drive the finite 9-parent obstruction logic, and it can be proved by an exact infeasibility certificate for the safe rational relaxation with the extra inequality:

```text
sum_a e_a <= 8.
```

## Why this is the relevant target

The entry-point numerical fact is:

```text
min sum_a e_a approx 8.764169...
```

but the repository currently lacks a safe exact domination theorem for the pooled model, so the exact step from this numerical value to a theorem is not available. The exact target must therefore be formulated on the exact safe relaxation, not on the raw floating LP.

## Current obstruction

The safe rational relaxation and its exact Farkas certificate are not yet available. The code and artifacts currently record that the threshold route is blocked, and the exact pooled child model is not proven to dominate the genuine continuation family.

## Therefore

The weakest useful Gate-1 target is still open. The project must first serialize the exact safe relaxation and prove `sum(e) <= 8` infeasible before claiming any exact Gate-1 closure.
