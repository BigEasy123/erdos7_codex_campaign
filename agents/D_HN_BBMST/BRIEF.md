# Track D — correlated HN / BBMST analytic bridge

## Mission

Find a rigorous analytic survivor-dispersion inequality that handles repeated powers without the known overcounting failures.

Your work should be able to stand even if Track A never finishes enumerating CARD9.

## Inputs

- `docs/CURRENT_FRONTIER.md`
- `docs/DEAD_ENDS.md`
- `src/hn_oracle_prebuilt.py`
- `src/state2275_hn_milp.py`
- `src/state2275_tower_heavy_bbmst_v3.py`
- `src/state2275_child_pooled_master.py`
- `artifacts/exact/STAGE18_RESTART_HN_EXACT_OUTPUT.txt`

## Known numerical/structural landmarks

- Exact project HN threshold `R_HN` is in `CURRENT_FRONTIER.md`.
- Naive first-moment HN averaging fails.
- Uniform geometric inflation of squarefree supports to whole prime-power towers fails badly.
- Further 3-adic depth alone looked much less damaging than repeated 5/7/11 cofactor powers.
- If a suitable low fiber has every high factor count `<=12`, a saved `K=12.5` stagewise HN envelope had positive least margin at p=29; this needs re-audit before theorem use.

## Attack directions

### D1. Condition before inflating

Derive HN moment bounds conditional on actual low residue cylinders / next-3 digit choices, rather than summing independent tower tails. Quantify how incompatibility reduces simultaneous contribution to `B2` and `B3`.

### D2. Packetwise HN inequality

Use transversal triangle / pairwise-coprime arm structure to bound the HN contribution of a whole packet jointly. Aim for an inequality whose extremizer can be enumerated exactly.

### D3. BBMST/HN dichotomy

Prove a local dichotomy: if survivor deletion is concentrated enough to threaten BBMST, the same concentration forces an HN-good fiber/event. This is the conceptual bridge the project currently lacks.

### D4. Repeat-power exact tail

For a fixed radical support and residue packet, sum the 5/7/11 exponent tail **with collision constraints**, not independently. Look for a rational generating-function or dynamic-programming bound that can be certified.

### D5. Published theorem interface

Identify exactly which Hough–Nielsen hypotheses allow arbitrary prime powers and how the project’s staged fiber quantities map into them. Preserve citation/theorem numbers in `RESULT.md`; do not rely on memory alone if literature access is available.

## Deliverable

A proved analytic inequality/dichotomy with exact constants if possible. Numerical optimization alone is `NUMERICAL_EVIDENCE`, not closure.
