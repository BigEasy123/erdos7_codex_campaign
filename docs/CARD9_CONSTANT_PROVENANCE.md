# CARD9 constant provenance

This memo classifies the constants currently appearing in the CARD9 / state-2275 model pipeline and records their exact mathematical source.

## Summary

| Constant | Value | Classification | Provenance |
|---|---:|---|---|
| cut | 1/50 | EXACT_RATIONAL_SOURCE | algorithmic threshold in the heavy-vector cutoff; exact representation of .02 |
| digit_cut | 1/5 | EXACT_RATIONAL_SOURCE | algorithmic threshold in the next-digit pooling; exact representation of .2 |
| ZF | 8769/1000 | NUMERICAL_APPROXIMATION | derived from the safe threshold `9.019 - 0.25`, not a theorem constant |
| Gall(m) | product p/(p-1) | EXACT_RATIONAL_SOURCE | exact upstream tower weight source |
| qres(m, es) | product p^(e-1) in denominator | EXACT_RATIONAL_SOURCE | exact residual modulus weight |
| heavy vector weights | 1 / product p^(e-1) | EXACT_RATIONAL_SOURCE | exact upstream BBMST tower weights |
| f[m] = Gall(m) - 1 or Gall(m) | EXACT_RATIONAL_SOURCE | exact residual budget in heavy vectors |

## `cut = .02`

The code path in `state2275_tower_heavy_bbmst_v3.py` and `state2275_hunter_benders_v2.py` uses the threshold `.02` as a scalar cutoff for heavy-vector inclusion. In the exact source reconstruction this is replaced by the exact rational value:

$$
.02 = \frac{1}{50}.
$$

This is an algorithmic cutoff, not a theorem-derived constant. The exact code uses the rational cutoff everywhere once the provenance is reconstructed.

## `digit_cut = .2`

The child-pooling model uses `.2` in the family split between `resolved` and `unresolved` deep-3 loads. The exact replacement is:

$$
.2 = \frac{1}{5}.
$$

This is also an algorithmic threshold, not a theorem constant.

## `ZF = 9.019 - .25`

The file `src/state2275_tower_heavy_bbmst_v3.py` defines the local protection margin as

$$
ZF = 9.019 - 0.25.
$$

This is a numeric safety threshold, not a published theorem constant. In exact arithmetic this is:

$$
\frac{9019}{1000} - \frac{1}{4} = \frac{8769}{1000} = 8.769.
$$

Therefore the exact rationalized constant is `8769/1000` and it is classified as `NUMERICAL_APPROXIMATION` unless a later theorem derives it as a justified exact lower bound. At present no such derivation is present in the repository; it is a model safety margin rather than an exact theorem constant.

## Upstream exact families that are recovered

The following families are already exact upstream and do not require guesswork:

- `Gall(m)`
- `f[m]`
- `heavy_vectors(m, cut)` weights
- `hsum[m]`
- `tail[m]`
- `qres(m, es)` in `hunter_v2_step.py`
- `maxforest` edge weights in exact rationals
- Hunter cut support from active signatures

## Conclusion

All relevant cut thresholds in the active pipeline admit exact rational representations. The rounded safety constant `ZF = 8769/1000` is not a theorem constant and must remain flagged as a numerical approximation until the underlying derivation is supplied.

No exact phase-model promotion should proceed while any model constant relevant to the lower-bound argument remains in `UNKNOWN_PROVENANCE` status. As of this audit, the checked constants are either exact rational sources or explicit numerical approximations with a documented provenance.
