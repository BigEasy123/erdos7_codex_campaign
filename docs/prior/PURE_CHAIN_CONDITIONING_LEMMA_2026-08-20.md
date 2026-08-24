# Pure-chain conditioning lemma — corrected replacement for repeated codimension-one cancellation

Date: 2026-08-20

## Setting
Assume a lexicographically least hypothetical odd distinct covering system: first minimize the LCM `N`, and among those minimize the sum of the moduli.  By divisor completion, if `p^alpha d` is used and `r<=alpha`, then every divisor `p^r d` (when greater than 1) is also used.  By irredundancy/incompatibility, whenever `p^r d | p^s d` with `r<s`, the two corresponding residue classes are disjoint.

## Lemma 1 — a fixed-cofactor p-chain is disjoint
Fix `(p,d)=1`.  If the moduli

\[
p^{r_0}d,p^{r_0+1}d,\ldots,p^\alpha d
\]

all occur, then their residue classes are pairwise disjoint.

**Proof.** For `r<s`, `p^r d | p^s d`.  Compatibility modulo `p^r d` would make the finer class modulo `p^s d` a subset of the coarser class and hence redundant.  Therefore the classes are incompatible.  QED.

Consequently the union of the strict tail of the chain has ordinary density

\[
\sum_{r=r_0+1}^{\alpha}\frac1{p^r d}
<\frac{1}{d p^{r_0}(p-1)}.
\]

This is an exact disjoint-union statement, not a second-moment estimate.

## Lemma 2 — the forced pure p-tower causes only constant concentration inflation
If `p^alpha || N`, divisor completion forces the pure moduli

\[
p,p^2,\ldots,p^\alpha.
\]

Their residue classes are pairwise disjoint, so under uniform measure on `Z/p^alpha Z` their union has mass

\[
S_\alpha=\sum_{r=1}^{\alpha}p^{-r}
=\frac{1-p^{-\alpha}}{p-1}.
\]

Let `nu` be uniform measure conditioned on avoiding this entire pure tower.  For every p-adic cylinder `C` of depth `t`,

\[
\nu(C)
=\frac{\Pr(C\setminus U)}{1-S_\alpha}
\le \frac{p^{-t}}{1-S_\alpha}
=\frac{p-1}{p-2+p^{-\alpha}}p^{-t}
<\frac{p-1}{p-2}p^{-t}.
\]

Thus removing **all** forced pure powers produces only a depth-independent inflation factor

\[
\boxed{\frac{p-1}{p-2}},
\]

not an exponential `(p/(p-1))^t` or `(p-1)^{-t}` loss.

For example:

- `p=3`: inflation `<2`;
- `p=5`: inflation `<4/3`;
- `p=7`: inflation `<6/5`.

## Why this matters
The earlier `ALL_PURE_POWER_CANCELLATION_CHECKPOINT_2026-08-20.md` incorrectly treated every deep pure class as if it deleted a new global codimension-one coordinate hyperplane.  A class modulo `p^r`, `r>=2`, already fixes the preceding digits, so that argument was invalid.

The present lemma is the correct replacement: deep pure powers form a **disjoint p-adic comb**, and the whole comb may be conditioned away at once with only constant concentration inflation.  It does not yet control mixed chains with different cofactors, so by itself it is not the missing QED step.  It is, however, a rigorous structural input for the next old-prime-depth optimization.

## Tail after an already exposed shallow pure prefix
If the pure tower has already been removed through depth `r_0`, then the absolute density of all later pure powers is bounded by

\[
\sum_{r=r_0+1}^{\infty}p^{-r}=\frac{1}{p^{r_0}(p-1)}.
\]

For the two main shallow coordinates this gives

\[
p=3,r_0=3:\quad \frac1{54},
\qquad
p=5,r_0=2:\quad \frac1{100}.
\]

So the genuinely difficult old-prime tail is not the forced pure tower itself; it is the family of **mixed fixed-cofactor chains and their cross-chain intersections**.
