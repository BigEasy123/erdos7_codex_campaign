# Top-Digit p-adic Collision Lemma

## Statement

Assume an odd distinct covering exists and let `N` be the numerically least possible LCM of such a cover. Let `C` be a distinct cover with LCM `N`. Write

`N=p^alpha M`, `(p,M)=1`.

If `alpha>=2`, then at least `p` distinct cofactors `d|M` occur for which both moduli

`p^{alpha-1}d` and `p^alpha d`

belong to `C`.

If `alpha=1`, then at least `p-1` distinct pairs `d,pd` occur; if modulus `p` is absent, at least `p` such pairs occur.

## Proof

For a residue `y mod N/p`, write its CRT coordinates as `(y_p,y_M)` with

`y_p mod p^{alpha-1}` and `y_M mod M`.

For each `t mod p`, define the top-digit slice map `iota_t` by taking the unique residue `x mod N` satisfying

`x == y_M (mod M)`

and

`x == y_p + t p^{alpha-1} (mod p^alpha)`.

The images of the `iota_t` partition `Z/NZ` into `p` slices.

Consider a congruence from `C` with modulus `p^e d`, where `d|M` and `p` does not divide `d`.

If `e<alpha`, its pullback under every `iota_t` is a congruence with the same modulus `p^e d`: the condition only fixes p-adic digits below the top digit and the same `d`-coordinate.

If `e=alpha`, the congruence meets exactly the slice whose top p-adic digit agrees with its residue. On that slice its pullback is a congruence with modulus `p^{alpha-1}d`.

Because `C` covers `Z/NZ`, the pullbacks cover `Z/(N/p)Z` on each slice.

Suppose first that `alpha>=2`. All pulled-back moduli are odd and greater than 1. If they were distinct on some slice, that slice would be an odd distinct covering whose LCM divides `N/p`, contradicting the numerical minimality of `N`.

Thus every slice contains a repeated modulus. Two unchanged moduli cannot collide because the original moduli were distinct. Two terminal moduli divided by `p` cannot collide for the same reason. Hence a collision must consist of an unchanged modulus `p^{alpha-1}d` and the reduction of the terminal modulus `p^alpha d`.

Every top-digit slice therefore contains at least one matched pair `p^{alpha-1}d, p^alpha d`. A given terminal congruence occurs on exactly one top-digit slice, so the `p` slices require `p` distinct terminal moduli and hence `p` distinct matched pairs.

If `alpha=1`, a pure modulus `p` reduces to modulus 1 on its unique slice, so that slice need not exhibit a duplicate. On every other slice all moduli remain greater than 1, and numerical minimality again forces a duplicate, which can only be a pair `d,pd`. There is at most one pure modulus `p`, proving the stated `p-1` bound; if it is absent, all `p` slices force pairs.

QED.

## Why this is stronger than the divisor-count inequality

The usual primitive-count argument only yields enough terminal moduli to conclude `p<=tau(M)`. The lemma above records that each required terminal modulus is accompanied by the exact adjacent lower-level modulus with the same cofactor. That matching is the additional structure intended for the next low-prime-core reduction.
