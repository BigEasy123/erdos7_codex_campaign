# Erdős #7 — Approach & Failure Ledger
**Date:** 2026-08-21  
**Purpose:** Keep every serious route, failure mode, reusable lemma, and cross-domain translation visible so failed ideas are not accidentally repeated and useful fragments can be recombined.

## Status key
- **CLOSED / RETAIN** — proved or exactly certified and safe to reuse.
- **LIVE–HIGH** — one of the strongest current finishing routes.
- **LIVE–MEDIUM** — plausible and worth testing, but less direct.
- **REUSABLE FAILURE** — route failed in its original form, but exposed a useful invariant or bound.
- **DEAD AS STATED** — mathematically false or based on an invalid inference; do not revive unchanged.
- **TOO COARSE** — logically valid but quantitatively insufficient.
- **COMPUTATION ISSUE** — formulation may be valid; failure was solver scale, not mathematics.

---

# I. Current proof frontier

The cleanest current architecture is:

1. Work in a least hypothetical odd distinct covering system when using divisor completion, comparable-modulus incompatibility, vertical pairs, exact frames, hubs, and surplus triangles.
2. Lift a measure through new p-adic digits for free as long as every old parent has a surviving child.
3. Stop at the **first exhausted parent**.
4. At that parent:
   - exact-three low-supported chain/fork frames are now finitely certified;
   - new-prime support is a support escape;
   - surplus low-supported packets are the main remaining local obstruction;
   - repeated cofactor powers enter the chain / second-prime-pivot descent.
5. Convert the resulting residual either into the BBMST low-prefix gate or a Hough–Nielsen good-fiber / multi-residue gate.
6. Use published high-prime termination once the correct interface is verified.

The strongest currently isolated local hard geometry is the surplus packet near BBMST partial state 2275, where independent cylinder-max bounds are still slightly too pessimistic but full joint correlations are favorable.

---

# II. Live finishing approaches

| ID | Route | Status | Core idea | What must be proved / computed |
|---|---|---|---|---|
| L1 | **Residue-aware surplus packet SAT/MILP at state 2275** | LIVE–HIGH | Encode actual terminal residues, pair/triple gcd blockers, comparability, coverage of the exhausted parent, and HN dual variables simultaneously. | Show the joint "surplus + HN-bad" system is infeasible; extract exact rational/integer certificate. |
| L2 | **First-exhausted-parent induction** | LIVE–HIGH | Arbitrary depth is free until a parent is exhausted; then classify the local packet. | Prove every first exhaustion is either a certified bounded-support packet or a well-founded support/exponent escape. |
| L3 | **Well-founded support-escape rank** | LIVE–HIGH | Assign a lexicographic complexity to `(deepest prime, exponent depth, cofactor support, divisor-lattice width)` and show each non-HN packet strictly decreases/increases a bounded component. | Find the correct monotone rank and prove no cycle such as repeated `p -> q -> p` survives without forcing new support. |
| L4 | **Direct Hough–Nielsen multi-residue fixed point** | LIVE–HIGH | Avoid scalar `B2` compression; retain the actual residue sets `a_{n,r}` for each high factor. | Prove support-event / fixed-point inequalities directly from triangle/blocker geometry. |
| L5 | **Faithful HN bin / good-set propagation** | LIVE–HIGH | Use Hough–Nielsen's actual nested good sets and bins instead of Markov-collapsing to one norm. | Starting from our exact low biases, certify entry into their published all-prime induction. |
| L6 | **BBMST-or-HN minimax dichotomy** | LIVE–HIGH | Treat choice of residual measure as a minimax LP: adversary chooses legal packet, prover chooses probability measure. | Prove every legal packet has either `F_BBMST <= 9.019` or exact HN linear gate `< R`. |
| L7 | **Triangle/gcd-blocker branch-and-cut** | LIVE–HIGH | Add Stage-15 triangle blockers only when a surplus triangle is selected, using lazy cuts. | Close the 2275-type packets without enumerating all blocker combinations up front. |
| L8 | **Finite-state tree automaton / transfer matrix** | LIVE–HIGH | Encode each p-adic layer by a finite state: support downset, blocker pattern, bias profile. Arbitrary depth becomes paths in a finite directed graph. | Prove every "bad" strongly connected component is impossible or has spectral radius / potential < 1. |
| L9 | **Dynamic-programming / Bellman game** | LIVE–HIGH | Two-player game: adversary chooses legal deep classes; prover chooses survivor measure. Value is worst future BBMST/HN functional. | Find a Bellman supersolution `V(state)` with `V < threshold` and prove it is invariant under every legal move. |
| L10 | **Hypergraph expansion formulation** | LIVE–HIGH | Three top 3-digits form parts; compatible transversal triangles are hyperedges; gcd blockers are forced labels/costs. | Prove enough hyperedge expansion / matching to force either support growth or bias spreading. |
| L11 | **Poset / weighted Sperner route** | LIVE–MEDIUM/HIGH | Low divisors realizing one high quotient residue form antichains. Use weighted LYM/Sperner rather than only width 3/4. | Convert antichain structure into a quantitative bound on total HN residue multiplicity across all quotient residues. |
| L12 | **Residue-sensitive KKL second moment** | LIVE–MEDIUM/HIGH | Replace KKL's crude multiplicity factor `s^2` by the actual conflict graph of low-divisor labels; incompatible pairs have zero intersection. | Derive a second-moment theorem using graph edge/nonedge counts rather than a uniform multiplicity bound. |
| L13 | **Fourier / spectral correlation bound** | LIVE–MEDIUM/HIGH | Congruence classes are subgroup cosets in a finite abelian group; joint cylinder maxima can be bounded via Fourier coefficients / Parseval. | Exploit blocker/comparability to force cancellation or spectral spreading in the 2275 residual. |
| L14 | **Entropy / Shearer support-growth theorem** | LIVE–MEDIUM/HIGH | First exhaustion forces uncertainty/spread over support arms. Pairwise-coprime arms should increase entropy in independent prime coordinates. | Show repeated support recycling violates an entropy lower bound or Shearer-type inequality. |
| L15 | **Polymatroid / submodular rank** | LIVE–MEDIUM | Associate each cofactor packet with prime-support rank; coprime arms behave like independent increments. | Find a submodular potential that increases under surplus triangles but is globally bounded. |
| L16 | **Network-flow / min-cut translation** | LIVE–MEDIUM | Children to terminal supports to blockers to outside primes form a flow network. Exhausting a parent requires enough capacity across cuts. | Identify a cut whose required capacity exceeds what bounded low support can supply. |
| L17 | **Prefix-code / Kraft inequality translation** | LIVE–MEDIUM | p-adic congruence classes are rooted-tree cylinders/codewords; compatible comparable classes violate irredundancy, producing prefix-free restrictions. | Strengthen Kraft/McMillan with cross-prime support labels and blockers. |
| L18 | **Graph coloring / comparability graph** | LIVE–MEDIUM | At a parent, top p-digits are colors; comparable divisor nodes cannot share compatible projected residues. | Strengthen the earlier B3 coloring obstruction using coverage and triangle constraints. |
| L19 | **SDP / Lovász-theta / association-scheme bound** | LIVE–MEDIUM | State 2275 has substantial symmetry. Build a graph whose independent sets are legal residue packets and use SDP to bound HN-bad configurations. | Produce a rationalized SDP or derive a human spectral inequality. |
| L20 | **Polynomial / SOS certificate** | LIVE–MEDIUM/LOW | Encode residue-choice indicators and incompatibility constraints as polynomial equations; certify the bad region empty with SOS/Nullstellensatz. | Useful if SAT/MILP leaves only a tiny finite state. |
| L21 | **Kernel-checked finite CRT certificate** | LIVE–HIGH for rigor | Once finite cases are isolated, formalize integer inequalities / CRT capacity checks in Lean. | Turn computational closure into an independently trusted certificate chain. |
| L22 | **Successive-filter IP à la Zhang–Zhang** | LIVE–HIGH | Reciprocal filter -> divisor-completed IP -> partial-cover filter -> exact solver only on survivors. | Apply this pipeline directly to surplus packet states instead of one monolithic MILP. |
| L23 | **Reverse-engineer repeated-modulus constructions** | LIVE–MEDIUM | Near-counterexamples with one repeated odd modulus show how branching succeeds when distinctness is relaxed. | Identify the exact branching move that requires repetition; prove a surplus packet would force that forbidden repeat. |
| L24 | **Pure-tower transversal optimization** | LIVE–MEDIUM | Choose one survivor in each allowed shallow branch to get excellent BBMST cylinder caps, then optimize against mixed deletions. | Replace the failed scalar `26.14%` deletion budget by packet-aware correlated transversal selection. |
| L25 | **Coordinatewise HN `K=12.5` support-event route** | LIVE–MEDIUM/HIGH | It suffices to control induced high residue sets, e.g. `|a_{n,r}| <= 12` in the sharp singleton case. | Derive residue-count caps from support escape / antichain / triangle geometry. |
| L26 | **Hybrid BBMST finite stage + HN tail** | LIVE–HIGH | Use BBMST only where its squarefree functional is strong; switch to HN exactly at packets where BBMST degrades. | Certify a universal switching rule with exact finite duals. |

---

# III. Failed / limited approaches and what they taught us

| ID | Original route | Classification | Failure / obstruction | Reusable lesson |
|---|---|---|---|---|
| F1 | BFF bound alone at `L0` | TOO COARSE | `g_BFF > 2` at the boundary. | Excellent lower-bound sieve below `L0`; not the boundary finisher. |
| F2 | Maximum-spanning-forest refinement of BFF | TOO COARSE | Improves the excess but still remains above 2. | Pair-overlap information helps; higher-order correlation is relevant. |
| F3 | Base-only heavy-fibre scalar relaxation | REUSABLE FAILURE | Explicit aligned witness satisfies the scalar excess constraints. | Must retain actual cofactor residues / simultaneous compatibility, not just base loads. |
| F4 | Scalar `|T|, H(T)` 7-coordinate bound | TOO COARSE | Gives bounds too weak to reach `14/5`. | Need interaction between local deletions and maximizing residue classes. |
| F5 | Immediate hub contradiction from repeated hub modulus | DEAD AS STATED | Two distinct residue classes with the same modulus can occur in repeated-modulus covering variants. | Hub is structural, not itself a contradiction. |
| F6 | Apply BBMST `-1/-2` cancellation at every p-adic depth | DEAD AS STATED | Deep `p^r` classes are not codimension-one hyperplanes in the full digit product. | Only genuine first-new-digit cancellation is safe. |
| F7 | Direct sequential distortion through arbitrary deep 3/5 tails | TOO COARSE | Worst budgets around `2.08` or higher, not `<1`. | Scalar moment recurrence loses too much geometry. |
| F8 | Restart after the depth-free `5/48` residual using uniform conditioning | TOO COARSE | Subsequent 11–73 budget around `4.47`. | Residual mass is not concentration control. |
| F9 | Universal one-extra-3-digit preservation of BBMST `F<=9.019` | DEAD AS STATED | LP gives `F≈9.431313 > 9.019`. | Deep structural restrictions are essential; arbitrary extension is false. |
| F10 | Generic HN two-/three-moment handoff from universal Stage-12 biases | TOO COARSE | Best generic criterion remains `>1`; no crossover before direct-removal budget exceeds 1. | Need packet-specific optimized measure or direct residue-set information. |
| F11 | Subtract comparable low-prefix pairs inside HN fibre moment | DEAD AS STATED | Incompatibility can live in the high coordinate; both low cofactors can meet the same fibre with different high residues. | Keep high residue labels; do not scalar-cancel those cross terms. |
| F12 | Local blocker/spine CRT inconsistency | DEAD AS STATED | Exact chain/fork ladder witnesses exist, even at deeper hubs. | Must encode coverage, surplus triangles, second-prime pivot, or HN loads. |
| F13 | Raw two-prime `7/8` density -> BBMST | TOO COARSE | Naive domination yields BBMST functional about `32.83`. | The `7/8` fact is structural support escape, not an analytic handoff. |
| F14 | Pure-tower transversal + arbitrary `26.1425%` mixed deletion budget | TOO COARSE as universal route | Actual squarefree extremals can delete far more under a scalar mass count. | Keep the optimized transversal idea, but make deletion packet-aware. |
| F15 | "Every legal packet stays BBMST-good" | DEAD AS STATED | Exact bad packet gives `F_min >= 9.47655`. | Necessitated the BBMST-or-HN dichotomy. |
| F16 | Scalar dichotomy `F<=9.019 OR B2<=17.5` | DEAD AS STATED | Legal relaxed state has `F≈9.4283`, `B2≈17.8118`. | Use joint `(B2,B3)` HN gate rather than one scalar. |
| F17 | Prime-power restart `eta<1` through 73 as full finish | REUSABLE FAILURE | Exact `eta≈0.9938839` is real but does not itself establish the >73 interface. | Keep as a finite noncoverage certificate / restart lemma. |
| F18 | Refined first-digit cancellation + conservative higher powers to feed BBMST tail | TOO COARSE | Bias at 73 still far above the BBMST large-prime threshold. | First-digit cancellation is valid but insufficient alone. |
| F19 | Naive sequential HN Markov update | TOO COARSE | Biases blow up after the first small-prime stage. | Must retain HN bins/good-set structure. |
| F20 | One-shot HN starting at 13/17/19 | TOO COARSE | `23+` works, but including 19 or smaller pushes the criterion above 1. | Treat 13/17/19 separately or improve the initial measure. |
| F21 | Interpret Stage-14 antichain width 3/4 as high-modulus multiplicity 3/4 | DEAD AS STATED | Width bounds realizations of the **same high quotient residue**, not all residues for that quotient modulus. | Feed antichain data into residue-sensitive moments, not scalar multiplicity. |
| F22 | Plug width 4 into KKL bounded-multiplicity theorem | DEAD AS STATED | Same mismatch as F21. | Derive a conflict-graph version of KKL instead. |
| F23 | Uniform measure on every deep residual | DEAD AS UNIVERSAL CLAIM | Some legal residuals have uniform HN value above the gate (~0.4977). | Optimized measures recover the gate; measure choice matters. |
| F24 | Reuse BBMST optimal shallow weights for HN branch | TOO COARSE / WRONG OBJECTIVE | Can give HN value around `0.5008`. | BBMST and HN optimize different geometries; use separate measures. |
| F25 | Count only number of deleted points to certify HN | TOO COARSE | Worst deletion counts can exceed reserve although actual HN cylinder profile is good. | Need which cylinders are hit, not just mass. |
| F26 | Monolithic depth-two MILP | COMPUTATION ISSUE | Tens of thousands of binary variables/constraints; solver stalls. | Decompose by divisor downsets, support cores, symmetry, lazy cuts. |
| F27 | Brute-force 303 targets | COMPUTATION ISSUE | Redundant under digit automorphisms. | 303 targets collapse to 70 rooted orbits in each extremum. |
| F28 | Independent-max surplus bound over all supports | TOO COARSE | 337/7637 partial states fail; only one is BBMST-dangerous. | Correlation between support classes is the missing saving. |
| F29 | Post-core independent-max bound at state 2275 | TOO COARSE | Still gives about `-11.1983` reserve. | Need exact joint residue correlations / blockers; this is the current local bottleneck. |
| F30 | Geometrically inflate each squarefree support to its whole prime-power tower | TOO COARSE | Destroys the HN margin. | Repeated powers require chain/downset structure, not independent union bounds. |
| F31 | Treat canonical-core domination as concentration-preserving exponent compression | DEAD AS STATED | The domination theorem leaves arbitrary tails intact and may enlarge the cover. | It is valid for monotone tail certificates, but least-counterexample structural arguments must be applied before losing leastness. |
| F32 | Base-only reciprocal-capacity / heavy-set moment bound | TOO COARSE | Feasible explicit witness; scalar ceiling roughly an order of magnitude too high. | Simultaneous divisor compatibility across cofactor residues is essential. |
| F33 | "More computation alone" without structure | REUSABLE FAILURE | Large MILPs repeatedly stall or produce weak relaxations. | Use canonicalization, orbit reduction, staged filtering, and exact small certificates. |

---

# IV. Closed results that should remain available as components

- Least-counterexample / irredundant framework with divisor completion and comparable-modulus incompatibility.
- Prime-support normalization to consecutive odd primes.
- Exact exclusion of `L0`.
- Top-p-adic vertical-pair lemma.
- Exact-frame hub geometry.
- Exact-three chain/fork classification.
- Support-poor chain second-prime pivot; tight backtrack can only return to the original prime.
- Two-prime rectangle reciprocal mass `<1`, forcing outside support.
- Surplus terminal compatibility graph and transversal triangles.
- Pair/triple-gcd blockers for surplus triangles.
- Pair-overlap arms are pairwise coprime after factoring the common gcd.
- Antichain bound for repeated realizations of one fixed high quotient congruence.
- Depth-free `3/5/7` residual mass at least `5/48`.
- Exact low-stage through-23 removal certificate under the canonical-tail setup.
- Exact BBMST squarefree extremal reconstruction.
- Exact Stage-18 restart / HN linear gate.
- Exact Stage-23 one-layer squarefree exhaustion certificate on both BBMST extrema.
- Independent reconstruction of BBMST `7637 -> 90`.
- Exact-three low-supported first-exhaustion branch closed over all 7637 canonical squarefree partial states.

---

# V. Translations into other mathematical problem types

## 1. Hypergraph problem
**Translation.**
- Vertices: terminal classes, partitioned by top p-digit.
- Hyperedges: compatible transversal triangles through an exhausted parent.
- Labels: gcd supports / blocker moduli.
- Expansion: coprime overlap arms.

**Target theorem.**
Every sufficiently covering 3-partite hypergraph with these label constraints either expands prime support or creates enough residue dispersion for HN.

**Why attractive.**
The surplus branch is already literally triangle-based.

---

## 2. Finite automaton / model checking
**Translation.**
A p-adic layer is a transition between finite packet states:
`(support downset, blockers, residue orbit, bias summary)`.

**Target theorem.**
No infinite path stays in the "BBMST-bad and HN-bad" state set. Equivalently, there is no bad strongly connected component.

**Why attractive.**
It turns arbitrary exponent depth into a finite graph-cycle problem.

---

## 3. Zero-sum game / dynamic programming
**Translation.**
- Player A chooses legal congruence classes / deep packet.
- Player B chooses the residual measure.
- Payoff = BBMST/HN functional.

**Target theorem.**
Construct a Bellman potential showing the minimax value remains below the handoff threshold.

**Why attractive.**
Our recent optimized-measure behavior is already a minimax phenomenon.

---

## 4. Prefix coding / information theory
**Translation.**
A congruence `a mod p^r` is a p-adic prefix cylinder. Comparable compatible classes behave like nested codewords, forbidden by irredundancy.

**Potential tools.**
Kraft inequality, entropy, Shearer, prefix-free codes, tree entropy.

**Target.**
Show repeated attempts to exhaust parents consume more "prefix capacity" than bounded low-prime support can supply.

---

## 5. Poset / Sperner theory
**Translation.**
Low divisor labels live in a product-of-chains divisor lattice. Same quotient residue labels form an antichain.

**Potential tools.**
LYM inequality, weighted Sperner, chain decompositions.

**Target.**
Replace crude width 3/4 by a weighted total-mass inequality compatible with HN moments.

---

## 6. Spectral / Fourier analysis on CRT groups
**Translation.**
Residue classes are cosets of subgroups in finite abelian groups; the residual indicator has a Fourier spectrum.

**Potential tools.**
Parseval, uncertainty inequalities, spectral gap, character sums.

**Target.**
Quantify the joint-correlation saving that independent cylinder maxima miss at state 2275.

---

## 7. Graph / SDP formulation
**Translation.**
Vertices are candidate residue choices; edges connect incompatible choices. A legal packet is an independent/transversal set.

**Potential tools.**
Lovász theta, semidefinite relaxations, association schemes, Hoffman bounds.

**Target.**
Show no independent set can both exhaust the parent and preserve HN-bad concentration.

---

## 8. Network flow / cut problem
**Translation.**
Flow goes from parent children -> terminal supports -> gcd blockers -> outside-prime support.

**Target.**
A min-cut inequality showing bounded low support lacks enough capacity to recycle all forced packets.

---

## 9. Polymatroid / matroid rank
**Translation.**
Prime supports are ground-set elements; coprime triangle arms give independent rank increments.

**Target.**
Find a submodular rank potential that strictly increases under every noncompressible surplus move but is bounded by the finite low-prime set.

---

## 10. Cluster expansion / polymer LLL
**Translation.**
Congruence events are polymers with overlap graph determined by shared primes/residues.

**Target.**
Use triangle packet structure to improve the local partition-function bound beyond scalar HN moments.

---

## 11. Formal proof / certificate problem
**Translation.**
After structural reduction, every remaining claim is finite CRT arithmetic.

**Potential implementation.**
Lean 4, exact SAT proof logs, rational LP duals, DRAT/LRAT, verified integer inequalities.

**Target.**
Make the final computational step independently checkable rather than solver-trusted.

---

# VI. Innovation combinations worth trying first

1. **Automaton + Bellman LP:** build the finite first-exhaustion state graph and solve for a rational potential `V` satisfying all transition inequalities. This could prove arbitrary-depth termination in one finite certificate.

2. **Hypergraph + entropy:** use transversal triangles and coprime arms to prove that each surplus step creates a minimum amount of new-prime entropy; bounded low support then cannot sustain an infinite bad descent.

3. **Poset + HN:** derive a weighted LYM inequality for low-divisor labels and plug it directly into the second/third HN bias sums. This is the mathematically cleanest repair of the invalid "width = multiplicity" shortcut.

4. **Residue-sensitive KKL:** modify the bounded-multiplicity distortion second moment so the penalty is the actual number of compatible label pairs rather than `s^2`. Stage-14 incompatibility can then delete real cross terms legally.

5. **Fourier + state 2275:** compute the spectral structure of the 2275 residual and prove a uniform upper bound on joint cylinder concentration. This directly attacks the ~11-point deficit of the independent-max relaxation.

6. **Zhang-style successive filtering on the surplus packet:** reciprocal/support filter -> divisor-downset filter -> triangle-blocker filter -> HN dual filter -> exact SAT/MILP only on survivors.

7. **Reverse-engineer repeated-modulus tree constructions:** compare the exact branching gadget that works when one modulus is allowed to repeat with our surplus packet. Try to prove that completing the packet would force precisely such a repeat, contradicting distinctness.

---

# VII. Recommended experimental order

**A. Discovery first:**  
Automaton/Bellman, hypergraph-expansion, weighted-poset/HN, and residue-sensitive KKL.

**B. Exact finite attack in parallel:**  
State-2275 triangle-blocker SAT/MILP with rational HN dual.

**C. Tail proof:**  
Faithful Hough–Nielsen bin/good-set propagation once a packet gives the required initial bias/residue data.

**D. Formalization:**  
Convert the winning finite certificate to integer/rational verification, then Lean/SAT-proof logging if practical.

---

# VIII. Important proof-ledger distinction

The library contains a **canonical shallow-core domination theorem**: any hypothetical cover can be enlarged/normalized to a canonical `3^3 5^2` pure core plus completely unrestricted tail classes. That is useful for monotone tail noncoverage certificates.

It is **not** a concentration-preserving exponent compression theorem and does not preserve every least-counterexample structural property after cover enlargement. Therefore:

- use least-counterexample surgery / blockers / incompatibility **before** passing to a super-system;
- use the canonical-core domination theorem for monotone "even this enlarged tail cannot cover" arguments.

Keeping these two proof modes separate prevents several earlier false shortcuts.
