# Depth-free 3-5-7 residual lemma

## Statement
Let \(\mathcal C\) be any distinct collection of congruence classes whose moduli are divisors greater than 1 of
\[
3^\alpha5^\beta7^\gamma,
\]
where \(\alpha,\beta,\gamma\ge 0\). Then the upper density of the union of the classes in \(\mathcal C\) is at most
\[
\boxed{\frac{43}{48}}.
\]
Consequently at least \(5/48\) of the CRT box remains uncovered, uniformly in all three exponent depths.

## Published input
Harrington--Klein--Lowrance--Trifonov, Theorem 1.9 (arXiv:2605.18644), gives for a distinct system supported on three prime powers an upper bound
\[
\sum_i\frac1{m_i}
-\sum_{(m_i,m_j)=1}\frac1{m_im_j}
+\sum_{m_i,m_j,m_k\ \mathrm{pairwise\ coprime}}\frac1{m_im_jm_k}.
\]
The authors explicitly state that the proof works after replacing \(2,3,5\) by any three distinct primes.

## Support-group reduction
Group the selected moduli according to exact nonempty prime support. Let their reciprocal masses be
\[
A,B,C,D,E,F,G
\]
for supports
\[
\{3\},\{5\},\{7\},\{3,5\},\{3,7\},\{5,7\},\{3,5,7\}.
\]
The published upper bound becomes
\[
U=A+B+C+D+E+F+G-AB-AC-BC-AF-BE-CD+ABC.
\]
The available reciprocal masses satisfy
\[
A\le\frac12,\quad B\le\frac14,\quad C\le\frac16,\quad
D\le\frac18,\quad E\le\frac1{12},\quad F\le\frac1{24},\quad G\le\frac1{48}.
\]

Every partial derivative of \(U\) is positive throughout this box. Explicitly,
\[
\partial_GU=1,
\quad \partial_DU=1-C\ge\frac56,
\quad \partial_EU=1-B\ge\frac34,
\quad \partial_FU=1-A\ge\frac12,
\]
\[
\partial_AU=1-B-C-F+BC\ge\frac7{12},
\]
\[
\partial_BU=1-A-C-E+AC\ge\frac13,
\]
\[
\partial_CU=1-A-B-D+AB\ge\frac14.
\]
Thus the maximum occurs when every support group has its full available reciprocal mass.

Let
\[
X=\sum_{i\ge1}3^{-i}=\frac12,\qquad
Y=\sum_{j\ge1}5^{-j}=\frac14,\qquad
Z=\sum_{k\ge1}7^{-k}=\frac16.
\]
At full support the expression simplifies exactly to
\[
U=X+Y+Z-XYZ,
\]
so
\[
U\le\frac12+\frac14+\frac16-\frac1{48}=\boxed{\frac{43}{48}}.
\]

For finite \(\alpha,\beta,\gamma\), the reciprocal masses are smaller, so the same bound holds a fortiori.

## Significance
Arbitrary extra powers of 3, 5, and 7 cannot by themselves cover the CRT space. They always leave a uniform residual of density at least \(5/48\). Therefore unbounded 3/5/7-adic depth is not, by itself, a source of arbitrary covering power; any hypothetical cover must use mixed classes carrying primes \(\ge 11\) to repair this residual.
