# Probe-3 reduction certificate — 2026-08-19

## Statement

For the canonical active two-branch residual family, the low-depth potential is nonnegative for **all three** possible mod-3 probe positions \(\rho_3\in\{0,1,2\}\). Thus the proof no longer needs to assume \(\rho_3=2\).

## Position \(\rho_3=0\)

The universal normalized potential bound has worst constant
\[
C_0=-14479,
\]
so
\[
\Phi_T(\rho)\ge 79|T|-14479\ge0
\]
for \(|T|\ge184\). Every canonical residual family starts at \(|T|\ge188\), so this position is automatically closed.

## Position \(\rho_3=2\)

This is the original normalized finite certificate. The finite window is certified through \(|T|=235\), and the universal normalized tail
\[
\Phi_T(\rho)\ge79|T|-18601
\]
takes over at \(|T|\ge236\).

## Position \(\rho_3=1\)

The universal normalized bound has worst constant
\[
C_1=-17629,
\]
so it automatically closes \(|T|\ge224\). Therefore only the finite range
\[
188\le |T|\le223
\]
requires a terminal certificate.

There are exactly **42,560** formal allocation/defect strata in that finite range. They partition exactly as

- 22,767 closed by the clean-defect one-sided tail;
- 9,353 exactly absent (zero legal dirty residual states);
- 6,263 closed by the complementary dirty-residual tail;
- 4,177 requiring stage-2 correlation checks.

Among the 4,177 stage-2 candidates, 2,462 close immediately. The remaining 1,715 are all closed by stronger exact/grouped checks:

- 1,186 full exact-clean closures;
- 4 non-225 exact-dirty/M3 closures;
- 155 non-225 hard closures recorded in `rho3_1/NON225_HARD_CLOSURE_AUDIT.json`;
- 175 225-containing grouped-clean closures;
- 5 225-containing exact-dirty/M3 closures;
- 90 reduced grouped-clean closures;
- 100 final low-six-depth grouped/grouped-chunk closures.

These counts sum exactly to
\[
1186+4+155+175+5+90+100=1715.
\]

The final 100-case 225 ledger is fully closed. The literal last case was stratum `s4150`, with all 1,575 reduced probe-orbits certified and
\[
B_{\min}=368>0.
\]
No completed finite check produced a negative survivor.

## Conclusion

All three mod-3 probe positions are now closed:
\[
\boxed{\rho_3=0\ \checkmark,\qquad \rho_3=1\ \checkmark,\qquad \rho_3=2\ \checkmark.}
\]
Hence **probe-3 reduction is no longer an open normal-form obligation**.

The machine-readable exhaustive audit is `PROBE3_RHO1_GLOBAL_AUDIT_2026-08-19.json`.
