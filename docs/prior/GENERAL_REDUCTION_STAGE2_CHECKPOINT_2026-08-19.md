# Erdős–Selfridge General Reduction — Stage 2 Checkpoint

Date: 2026-08-19
Status: structural checkpoint on exponent depth and the high-rank tail.

## Objective
Continue the post-`L0` route

`least primitive odd cover -> exponent-depth control -> finite low-prime prefix -> published high-prime sieve -> contradiction`.

This checkpoint does **not** claim the general odd-cover theorem. It records three rigorous reductions that substantially narrow the remaining problem.

## 1. Exponent-depth p-frame / hub structure

Let `N=p^alpha M`, `(p,M)=1`, be the numerically least hypothetical odd distinct-covering LCM.

Using the p-adic digit model, fixing the highest p-adic digit gives p covers on the period `N/p`. Since `N` is least, no slice may retain distinct moduli. This forces a terminal/nonterminal vertical collision in each top digit. Thus there are at least p matched modulus pairs

`p^(alpha-1)d, p^alpha d`.

If the number of terminal `p^alpha` classes is exactly p, there is exactly one terminal class in every top digit. In a minimal subcover each vertical pair is residue-nested **only if the terminal class is redundant**, so all p pairs are nonnested.

Now write the p terminal moduli as

`p^alpha m_1,...,p^alpha m_p`.

Krukenberg's reduction lemma (Dalton--Jones, Lemma 2.3) replaces these p classes by one class of modulus

`h = p^(alpha-1) lcm(m_1,...,m_p)`

and preserves covering. If h were not already an original nonterminal modulus, this would yield a smaller odd DCS with LCM dividing `N/p`, contradicting leastness. Hence an exact-p terminal frame forces a pre-existing **hub modulus** h.

This gives the exponent-depth dichotomy:

`>p terminal classes` OR `rigid exact-p nonnested frame + forced hub`.

Important limitation: the hub does not yet lower alpha automatically, because Krukenberg compression may create two different residue classes with the same hub modulus. Recent repeated-modulus odd-cover constructions show that such covers are not intrinsically impossible.

Detailed proof: `EXPONENT_DEPTH_FRAME_AND_HUB_LEMMA_2026-08-19.md`.

## 2. Arbitrary 3/5/7 depth has a uniform residual

Harrington--Klein--Lowrance--Trifonov Theorem 1.9 (arXiv:2605.18644) gives a three-prime inclusion-exclusion density bound; the authors explicitly state that the proof works for any three distinct primes.

Applying it to arbitrary distinct congruences with moduli dividing

`3^alpha 5^beta 7^gamma`

and optimizing exactly over the seven possible nonempty prime-support groups yields

`covered density <= 43/48`.

Therefore

`uncovered density >= 5/48`

uniformly in alpha,beta,gamma.

The proof is depth-free: the reciprocal masses are bounded by the infinite geometric sums 1/2, 1/4, and 1/6. An exact rational verifier checks all derivative inequalities and the final identity.

Files:
- `DEPTH_FREE_357_RESIDUAL_LEMMA_2026-08-19.md`
- `verify_depth_free_357.py`
- `DEPTH_FREE_357_VERIFICATION.txt` (PASS)

This means arbitrary extra powers of 3,5,7 cannot by themselves remove the entire residual. Mixed classes involving primes >=11 are essential.

## 3. The arbitrary high-prime tail is already a published theorem once the low prefix is controlled

Balister--Bollobás--Morris--Sahasrabudhe--Tiba (arXiv:1901.11465), at the end of their square-free odd-cover proof, explicitly state that the large-prime results they use do not require square-freeness. Their argument actually proves nonexistence if every prime `p<=73` appears with exponent at most 1; arbitrary prime powers above 73 are allowed.

Thus we do **not** need a new infinite-prime theorem. The remaining non-squarefree obstruction is confined to the finite 73-smooth prefix

`3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73`.

Their handoff from the low prefix into the 13--73 and >73 sieve is controlled by an optimized probability measure; in their square-free setting a sufficient low-prefix condition is

`c_5(3) - (3/4)c_5(1) <= 9.019`.

The new depth-free 3/5/7 residual has mass at least 5/48, providing a uniform nonempty reservoir for a low-prefix measure. But **total residual density is not directly comparable to the BBMST 9.019 moment threshold**: the latter sums worst hyperplane masses over many fixed-coordinate sets. A direct handoff therefore needs geometric control of those moments, plausibly from the p-adic frame/nonnesting constraints or the stronger `Phi` certificate, not density alone.

Detailed handoff: `HIGH_RANK_TAIL_HANDOFF_2026-08-19.md`.

## 4. Current proof map

Established:

1. `L0` excluded by the project potential certificate.
2. Least hypothetical odd covering LCM is primitive and may be equipped with a minimal DCS.
3. Published prime replacement normalizes support to consecutive odd primes.
4. Exact BFF boundary gives `N>L0`.
5. Top p-adic slices force vertical pairs.
6. Exact-p terminal case forces a rigid nonnested p-frame plus hub.
7. Arbitrary 3/5/7 exponent depth alone leaves at least 5/48 residual density.
8. Published high-prime sieve already tolerates arbitrary prime powers above 73.

Still open:

### A. Low-prefix repeated-power control
Prove one of the following:
- a genuine exponent-compression lemma reducing repeated powers among primes <=73 to the canonical low-depth core; or
- a uniform low-prefix probability-measure theorem that feeds the non-squarefree residual directly into the BBMST moment condition.

### B. Integration with the L0/Phi certificate
The existing `Phi` theorem gives very strong control on the canonical `3^3 5^2` residual and a monotonic next-prime theorem (`p=7` is worst for all p>=7). The next objective is to translate that potential control into either:
- a low-prefix moment bound suitable for the BBMST sieve, or
- a compression invariant that survives deeper p-adic towers.

## 5. Best immediate next target

The most promising target is now a **Low-Prefix Measure Handoff Lemma**:

> For the residual of a least primitive odd cover after processing the repeated 3/5/7 towers (and then the finite repeated-power coordinates up to 73), construct a probability measure whose BBMST low-prefix moment is at most 9.019.

The 5/48 residual theorem supplies guaranteed support for such a measure, but the required moment bound is a separate geometric inequality. The next task is to translate nonnesting/frame constraints or the stronger `Phi` information into bounds on the BBMST hyperplane moments.

If this succeeds, the arbitrary high-rank tail is discharged by the existing published sieve and no infinite computation is required.
