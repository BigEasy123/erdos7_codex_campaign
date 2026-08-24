# Track F — global lift and 13–73 / >73 interface

## Mission

Work ahead of the local state-2275 attack. Determine exactly what remains after state 2275 is closed, and prove/audit as much of it as possible now so a local victory cannot be followed by a hidden global gap.

## Two independent targets

### F1. Lift from state 2275 to the other 7,636 canonical partials

The known fact that state 2275 is worst for low-four tower reserve is not automatically enough. Seek a theorem of one of these forms:

- a monotone domination of the relevant survivor-dispersion functional;
- a finite classification showing all other states are easier under the same bridge;
- a small set of extremal states rather than all 7,637;
- an exact stagewise certificate for all canonical states.

Use `src/stage24_recompute_7637_fast.py` as a starting point, but independently define the quantity that must be dominated.

### F2. High-prime interface

Audit the finite-prime restart through 13,17,...,73 and the transition to the published high-prime theorem.

You must answer precisely:

1. Which branches are BBMST-squarefree and which may retain repeated powers?
2. Which HN theorem allows the repeated powers actually present?
3. What are the exact good-fiber/support-event hypotheses at the restart?
4. Does the project distorted measure satisfy them after the low-prime deletions?
5. Which constants require exact rational certification?

If literature access is available, retrieve the papers and cite theorem/lemma numbers. Do not paraphrase an interface from memory.

## Deliverable

A dependency diagram from “state 2275 closed” to QED, with every edge classified `PROVED`, `FINITE_CERT_REQUIRED`, `LITERATURE_INTERFACE`, or `OPEN`. Any newly closed edge should include proof or verifier.
