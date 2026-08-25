# Exact source reconstruction report

## Executive judgment

The reported exact-rational blocker is narrower than earlier claimed. The upstream source families that feed the card-9 model are already exact in their native forms:

- `Gall(m)` is exact rational;
- `f[m]` is exact rational;
- `heavy_vectors(m, cut)` are exact rational weights;
- `maxforest` edge weights are exact rational;
- root cut thresholds `.02` and `.2` are exact rationals `1/50` and `1/5` once the model is rebuilt without float conversion;
- Hunter cut signatures in `HUNTER_V2_CUTLOG.json` can be regenerated exactly from active support and exact tower weights.

What remains genuinely numerical is the model safety threshold `ZF = 9.019 - 0.25 = 8769/1000`, which is a model margin, not a theorem constant, and therefore still needs its provenance to be traced or justified.

## Recovered exact families

### 1. Tower-heavy BBMST source families

Recovered from `src/state2275_tower_heavy_bbmst_v3.py` and its upstream exact definitions:

- `Gall(m)`; exact rational product over primes in the support;
- `f[m]` = exact heavy budget;
- `heavy_vectors(m, cut)` = exact rational tower weights;
- `hsum[m]` and `tail[m]` = exact rational totals;
- all resolution and divisor-completion coefficients in the exact model are deterministically reconstructible from these families.

### 2. Hunter exact family

Recovered from `src/hunter_v2_step.py` and the historical cut log:

- `qres(m, es)` is exact integer/rational from the exact tower source;
- `maxforest` uses exact rational edge weights `1 / (qa * qb)`;
- `make_cut` can reconstruct the same support as the historical float cut once the active node set is fixed;
- the exact replay produced 1308 historical cut records successfully from the saved log.

### 3. Child-pooling exact family

The model in `src/state2275_child_pooled_master.py` still loses exactness when it performs float casts in the unresolved group / child-capacity rows. That exactness can be rebuilt from the upstream fraction-valued weights, but the current numerical file is not itself the exact source.

## Remaining unresolved items

These items remain either numerical approximations or unresolved provenance, and should not be silently promoted as exact theorem constants:

- `ZF = 9.019 - 0.25 = 8769/1000` — numerical safety threshold; provenance is documented but not theorem-derived;
- any float-cast matrix rows in the numerical `state2275_child_pooled_master.py` builder that do not trace back to exact upstream source values;
- exact dual certificates are not yet available for a saved rejected 9-parent set.

## Exact matrix dimensions

The exact tower-heavy BBMST comparison script reported:

- variable count: 11050
- row count: 14447
- binary variable count: 9168

This matches the numerical model’s variable ordering and count in the source audit.

## Rational-model replay status

The following exact provenance scripts were run successfully:

- `src/state2275_tower_heavy_bbmst_exact.py`
- `src/state2275_hunter_exact.py`
- `src/verify_hunter_cuts_exact.py`

Fresh evidence:

- exact model support matches the numerical matrix within the check tolerance;
- Hunter exact cut replay succeeded on the saved log; `CUT_RECORDS 1308` was produced;
- the exact rational provenance is now reconstructed at the coefficient-source level.

## Exact phase dual status

No exact phase dual certificate for a rejected 9-parent set was obtained in this pass. This remains a downstream task beyond the source-reconstruction milestone.

## Next smallest obstruction

The next smallest obstruction is not a missing coefficient family; it is the exact dual certificate itself. The exact source families are recoverable, but the project still lacks:

1. a rationalized primal exact phase model serialized in a deterministic format,
2. the exact dual derivation with correct `<= / >= / =` conventions,
3. a positive rational lower bound `delta > 0` on a saved rejected 9-parent witness.

No claim of CARD9 closure or ERDOS 7 proof should be made from this reconstruction alone.
