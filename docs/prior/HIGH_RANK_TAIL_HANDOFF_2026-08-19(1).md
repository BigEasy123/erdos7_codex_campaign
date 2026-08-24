# High-rank tail handoff

## Published large-prime theorem already tolerates prime powers above 73
Balister--Bollobas--Morris--Sahasrabudhe--Tiba (arXiv:1901.11465), after proving the odd square-free theorem, explicitly note that the large-prime results used in their Section 5 do **not** require square-freeness. Their proof actually rules out a distinct odd covering whenever every prime \(p\le73\) occurs to exponent at most one; prime powers above 73 are allowed.

Therefore the arbitrary high-rank tail is not an independent infinite-prime problem. Any hypothetical odd distinct cover must have repeated prime-power structure in the finite low-prime set
\[
\boxed{3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73.}
\]
Once the non-squarefree behavior in this 73-smooth prefix is controlled, the published distortion/termination sieve handles all larger primes, even with arbitrary powers.

## BBMST handoff functional
In the square-free proof, the large-prime stage is fed by an optimized probability distribution on the low coordinates. Their Lemma 5.3 reduces the 13--73 stage to the low-prefix condition
\[
c_5(3)-\frac34c_5(1)\le 9.019,
\]
and Corollary 5.2 then feeds the >73 termination theorem.

This is important for the present project because it suggests a route that may avoid literal exponent-by-exponent compression: construct a probability measure on the residual left by the repeated low-prime towers, and prove a uniform moment bound strong enough to satisfy the same handoff inequality.

## New project input
The depth-free 3-5-7 lemma proves that classes supported solely on arbitrary powers of 3,5,7 leave residual density at least
\[
\frac5{48}.
\]
Conditioning the uniform measure on such a residual has the crude density-distortion factor
\[
\frac{48}{5}=9.6,
\]
which is close to BBMST's 9.019 low-prefix threshold. Density alone is not sufficient to identify their moment functional, but the numerical proximity shows that only a modest structural improvement beyond a raw mass estimate could make a direct measure handoff viable.

## Current reduction of the high-rank problem
The remaining global task can therefore be stated as:

1. control repeated powers in the finite 73-smooth prefix, either by p-adic frame/hub compression or by a direct low-prefix probability measure;
2. once the BBMST low-prefix moment threshold is met, invoke their published 13--73 and >73 distortion/termination machinery.

No new infinite enumeration over high primes should be necessary.

## Honest status
This handoff is a reduction, not yet a proof of the full high-rank tail. The missing theorem is a uniform low-prefix control statement for non-squarefree p-adic towers among primes \(\le73\).
