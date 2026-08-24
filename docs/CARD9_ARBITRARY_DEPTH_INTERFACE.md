# CARD9 arbitrary-depth interface

This document records the required implication and its current proof status. It is not a closure proof.

## Required implication

```text
arbitrary-depth bad continuation
    => at least 9 exhausted shallow parents
    => an exact CARD9 configuration represented by the certified master
    => contradiction
```

## Audit

- `arbitrary-depth bad continuation => at least 9 exhausted shallow parents` **[OPEN]**. The numerical pooled model reports a fractional lower bound near 8.764, but no exact dual certificate was preserved. The exact integer implication has not been independently proved here.
- `at least 9 exhausted shallow parents => exact CARD9 configuration represented by the certified master` **[OPEN]**. The phase model includes 331 shallow exhaustion variables and a `sum(e)=9` master, but the arbitrary-depth-to-pooled-relaxation domination and repeated-power coverage semantics still require a formal proof.
- `exact CARD9 configuration represented by the certified master => contradiction` **[OPEN]**. Every checked phase rejection is a floating LP lower bound. No optimizer-independent phase certificates, exact Benders cuts, or UNSAT branch certificate currently exists.

## Semantic hazards

The model must retain arbitrary prime powers, including exponent/depth information. Future squarefree variables, unresolved tails, pooled next-3-digit capacity, and Hunter cuts are relaxations with separate validity obligations. A squarefree support result cannot be silently promoted to the repeated-power statement.

## Current conclusion

CARD9 is not closed. The interface remains open until the three implications above are proved with exact certificates or symbolic arguments and independently audited by Track E.
