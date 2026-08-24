#!/usr/bin/env python3
from fractions import Fraction as F
from math import factorial
from decimal import Decimal, getcontext, ROUND_CEILING
getcontext().prec=100

P=[13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73]
D=[F(143,500),F(37,125),F(8,25),F(333,1000),F(337,1000),F(357,1000),
   F(91,250),F(377,1000),F(197,500),F(409,1000),F(421,1000),F(433,1000),
   F(9,20),F(58,125),F(481,1000),F(1,2)]

def eta(B2):
    f=B2; z=F(0)
    for p,d in zip(P,D):
        z += f/(4*d*(1-d)*(p-1)**2)
        f *= 1+F(3*p-1,1)/((1-d)*(p-1)**2)
    return z

B2=F(939021643,52631552)
z=eta(B2)
assert z == F(1214388808040855518079148965756252301981495818444068623716815930503680225933604795037019,
              1221861827844653704754536256580447630858302854437611063874022271435564927301158342492160)
assert z<1
zclean=eta(F(35,2))
assert zclean == F(63369201378462711733129136536905532002837228644962512927003941904542801971122017,
                   65003082522913828824821687158783639258885012405207260064215137718522566015975424)
assert zclean<1

# HN linear gate, rebuilt from exact finite-prime sums.
PH=[23,29,31,37,41,43,47,53,59,61,67,71,73]
M=F(261,100)
prod2=F(1);prod3=F(1)
for p in PH:
    prod2*=F(p,p-1)**2
    prod3*=F(p,p-1)**3
K2=prod2*sum((F(1,(p-1)**2) for p in PH),F(0))
K3=prod3*sum((F(1,(p-1)**3) for p in PH),F(0))

def de(x):return Decimal(x.numerator)/Decimal(x.denominator)
def rup(x,k,places=15):
    xd=de(x); scale=10**places
    if k==2:y=xd.sqrt()
    else:
        y=xd**(Decimal(1)/Decimal(3))
        for _ in range(20):y=(2*y+xd/(y*y))/3
    n=int((y*scale).to_integral_value(rounding=ROUND_CEILING))
    q=F(n,scale)
    assert q**k>=x
    return q

a=[F(1,p*p) for p in PH]
e=[F(0)]*(len(PH)+2);e[0]=F(1)
for v in a:
    for j in range(len(PH),0,-1):e[j]+=e[j-1]*v
DD={1:prod2*2*e[2]}
for k in range(2,len(PH)+1):
    DD[k]=prod2*factorial(k)*(k*e[k]+((k+1)*e[k+1] if k<len(PH) else 0))
A=rup(K2,2)/M+rup(DD[1],2)
for k in range(2,len(PH)+1):A+=M**(k-1)*rup(DD[k],2)/factorial(k-1)
B=rup(K3,3)
t=F(17,4);s=F(21,4)
alpha=A/(2*t); beta=B/(3*s*s); C=A*t/2+B*2*s/3; R=1-C
assert R>0
assert alpha*18+beta*145 < R  # equivalent to Q_HN<1
print("PASS")
print("eta_joint =", z, float(z))
print("margin_joint =", 1-z, float(1-z))
print("eta_B2_17.5 =", zclean, float(zclean))
print("margin_B2_17.5 =",1-zclean,float(1-zclean))
print("A =",A,float(A))
print("B =",B,float(B))
print("alpha =",alpha,float(alpha))
print("beta =",beta,float(beta))
print("R =",R,float(R))
print("HN linear LHS at (18,145) =",alpha*18+beta*145,float(alpha*18+beta*145))
print("HN criterion upper =",alpha*18+beta*145+C,float(alpha*18+beta*145+C))
