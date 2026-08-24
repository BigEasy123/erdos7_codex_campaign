# Erdős Problem #7 — state 2275 exact-certificate checkpoint

Date: 2026-08-22  
Status: **exact finite state-2275 depth-one surplus closure; not a QED**

## 1. What is now exact

The focal canonical partial is state `2275`,

```text
11**  1*1*  *22*  123*  1**1  *3*2  13*3
```

on the reduced shallow box `2 x 4 x 6 x 10`.  It leaves 331 shallow atoms before the four remaining square-free supports `12,13,14,15` are chosen.

For a depth-one terminal 3-adic packet with square-free cofactor dividing `5*7*11`, the divisor-closed **surplus** support downsets are

```text
0x0f 0x17 0x1f 0x33 0x37 0x3f
0x55 0x57 0x5f 0x77 0x7f 0xff
```

The finite feasibility model simultaneously includes:

- the seven fixed state-2275 square-free residue classes;
- one legal residue class on each of the four remaining square-free supports;
- comparable-modulus incompatibility among the square-free completions;
- one terminal class for each support in the chosen downset;
- deep/deep and deep/square-free divisibility incompatibility;
- freely chosen exhausted shallow parent(s);
- coverage of all three second-3-adic children of every selected exhausted parent; and
- the joint Hough--Nielsen `(B2,B3)` bad-gate dual.

For **each of the 12 surplus downsets**, the continuous nonnegative-variable relaxation has an exact Farkas contradiction. Consequently the integer model is infeasible a fortiori.

## 2. Exact Stage-18 Hough--Nielsen gate

The exact replay uses

```text
alpha = 51603567726348558328760981369659084133279683367
        /4373107200000000000000000000000000000000000000000

beta  = 14493601981951/13781250000000000

R     = 1985876874482391730913463316715795569734245382761
        /4115865600000000000000000000000000000000000000000
```

with

```text
ZH = R - alpha - beta
   = 5111658741313791476105513439461730119454397244699
     /10884177920000000000000000000000000000000000000000.
```

`verify_stage18_restart_hn_gate.py` rebuilds these coefficients from exact finite-prime sums using `Fraction` arithmetic and upward rational rounding of square/cube roots. Its saved output is reproduced byte-for-byte by the full replay driver.

## 3. Farkas certificate format

Each model is rewritten as

```text
C x <= d,    x >= 0.
```

For each downset, the certificate stores a rational multiplier vector `lambda` satisfying exactly

```text
lambda >= 0,
C^T lambda >= 0,
d^T lambda < 0.
```

These three conditions imply infeasibility immediately.  The stored multipliers have denominator `10^13`, but replay of the certificate is entirely exact rational arithmetic; the rounding is part of the certified witness, not a numerical tolerance.

The weakest contradiction among the twelve has

```text
d^T lambda =
-2433681111230126869193043081158315253930424823075084666112361
/1224470016000000000000000000000000000000000000000000000000000000
≈ -0.001987538346737375.
```

The smallest exact nonnegative column margin is

```text
13128293077609733460321214587660089230601886468501972381
/15548825600000000000000000000000000000000000000000000000000000
≈ 8.443269874742009e-7 > 0.
```

Thus the certificates have genuine sign margin after substitution of the full exact Stage-18 coefficients.

## 4. Exact conclusion of this checkpoint

**Lemma (finite state-2275 depth-one surplus certificate).**  In the state-2275 residue-aware model described above, no legal depth-one surplus first-exhaustion packet can be simultaneously compatible with the four legal square-free completions and remain on the Hough--Nielsen-bad side of the exact Stage-18 joint `(B2,B3)` gate.

Equivalently, every legal packet in this finite model is forced to the HN-good side.

This conclusion no longer depends on a MIP solver returning `infeasible`; the final verifier calls no optimizer.

## 5. Exact replay

Run

```bash
python verify_full_state2275_exact.py
```

The final lines must be

```text
STATE2275_FULL_EXACT_REPLAY=PASS
optimizer_calls=0
```

The driver also requires the Stage-18 arithmetic to byte-match the saved exact output and requires all twelve Farkas witnesses to pass.

## 6. What this closes

This removes the computational uncertainty at the **depth-one 2275 spike**.  Solver timeouts in the larger Hall/tower models are no longer needed to justify this finite local lemma.

It also validates the exact Stage-18 tangent/gate coefficients used by the state-2275 model rather than treating the displayed decimals as axioms.

## 7. What it does **not** close

This checkpoint does **not** prove arbitrary-depth reduction to the depth-one model. In particular:

1. first deep exhaustion may involve several shallow parents simultaneously;
2. mixed fixed-cofactor chains at different p-adic depths can interact;
3. a monotone tail-noncoverage domination theorem does not automatically preserve the BBMST/HN concentration statistics;
4. the exact finite restart through the primes up to 73 is not by itself an infinite-tail theorem.

Therefore no QED is claimed here.

## 8. Revised shortest route to QED

The remaining bridge should be formulated as a **correlated arbitrary-depth packet projection / survivor-dispersion lemma**:

> Starting from any legal arbitrary-depth continuation of a canonical low-four partial, either its surviving shallow projection is BBMST-good, or the first genuinely obstructive mixed-chain packet projects to an HN configuration dominated by one of the exact finite packet certificates (including state 2275), with the joint `(B2,B3)` gate preserved.

The proof must use actual residue incompatibility / first-exhaustion geometry. It must **not** assume an unproved concentration-preserving canonical compression.

Once that bridge is established, the preferred high-prime branch is Hough--Nielsen rather than forcing prime powers into the square-free BBMST model: Hough--Nielsen group congruences by square-free support but their local-lemma theorem and staged fibers allow arbitrary prime powers in the moduli. The remaining audit is to align the project joint gate with the nested good-fiber/support-event hypotheses needed for their iteration.

The square-free BBMST `>73` machinery remains an alternative on genuinely square-free / BBMST-good branches, but it should not be used as if it automatically covered repeated prime powers.

## 9. Files in this checkpoint

- `state2275_hn_milp.py` — source model whose coefficient alphabet is reconstructed exactly in replay.
- `STATE2275_FARKAS_CERTIFICATES_STAGE18_EXACT.json` — all twelve rational Farkas witnesses with exact Stage-18 coefficients.
- `verify_state2275_farkas_stage18_exact.py` — optimizer-free exact Farkas verifier.
- `verify_stage18_restart_hn_gate.py` — exact Stage-18 HN arithmetic verifier.
- `STAGE18_RESTART_HN_EXACT_OUTPUT.txt` — saved exact Stage-18 output.
- `verify_full_state2275_exact.py` — one-command complete replay.
- `STATE2275_FULL_EXACT_REPLAY.txt` — complete replay transcript.
- `SHA256SUMS.txt` — hashes of packaged files.
