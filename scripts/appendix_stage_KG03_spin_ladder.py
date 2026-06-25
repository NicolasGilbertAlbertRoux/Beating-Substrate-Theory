# -*- coding: utf-8 -*-
"""
BST Appendix Stage KG03 — the SPIN LADDER of kinetic geometry: does the SIGN of the force follow the
STRUCTURE (spin) of the dynamic deformation?  scalar (spin-0) / vorticity (spin-1) / tensor (spin-2).
Consolidates KG01 (scalar attract, vorticity repel, simulated) with the spin-2 (graviton) case.
The interaction = source_A . [propagator numerator] . source_B / k^2.  Static sources.
Numerators (standard, documented below), then U(r) sign for LIKE sources.
"""
import numpy as np

# ---- propagator numerators for static sources, contracted explicitly (mostly-minus eta) ----
# spin-0 (scalar): coupling g*q*phi -> exchange numerator N0 = q_A q_B ; U = -N0 * G(r)  (G>0)
# spin-1 (vector): coupling J^mu A_mu, static charge J^0=q ; numerator from eta_{00} flips sign:
#                  EM result U = +q_A q_B/(4 pi r)  => N1 = -q_A q_B  (so U=-N1*G = +q_Aq_B G : repel)
# spin-2 (tensor): coupling (1/2) h_{mu nu} T^{mu nu}; massless graviton projector
#   P_{mu nu, al be} = 1/2(eta_{mu al}eta_{nu be}+eta_{mu be}eta_{nu al}-eta_{mu nu}eta_{al be})
#   static mass T^{00}=rho (else 0): T_A.P.T_B = rho_A rho_B * 1/2(1+1-1) = +1/2 rho_A rho_B
#                  => N2 = +1/2 rho_A rho_B ; U=-N2*G  (attract; rho>0 always)
def projector_spin2_static():
    eta=np.diag([1.,-1.,-1.,-1.])           # mostly-minus
    # T^{mu nu}=diag-like with only 00 = 1 (unit static mass)
    T=np.zeros((4,4)); T[0,0]=1.0
    val=0.0
    for m in range(4):
     for n in range(4):
      for a in range(4):
       for b in range(4):
        P=0.5*(eta[m,a]*eta[n,b]+eta[m,b]*eta[n,a]-eta[m,n]*eta[a,b])
        val+=T[m,n]*P*T[a,b]
    return val   # = +0.5  (with appropriate index raising for static T this is the 00-00 piece)

s2=projector_spin2_static()
print("spin-2 graviton projector contraction for static mass (T^00=1): N2 =",s2," (>0 => attractive)")

def U(r,spin,like, m=0.0):
    G=np.exp(-m*r)/(4*np.pi*r)               # Yukawa/Coulomb Green fn (3D), massless m=0 -> long-range
    qq=1.0 if like else -1.0                  # like => same sign sources
    if spin==0: N=+qq
    elif spin==1: N=-qq                        # vector: like-charge repels
    elif spin==2: N=+0.5*1.0                    # tensor: mass>0 always same sign (always attract)
    return -N*G

rs=np.array([1.,2.,3.,5.,8.])
print("\nStatic interaction U(r) (U<0 attract, U>0 repel), LIKE sources, massless (long-range 1/r):")
for spin,name in [(0,"SCALAR  (spin-0)"),(1,"VORTICITY(spin-1)"),(2,"TENSOR  (spin-2)")]:
    Ulike=[U(r,spin,True) for r in rs]
    verdict="ATTRACT" if Ulike[0]<0 else "REPEL"
    print(f"  {name}: U(like)=",["%+.4f"%u for u in Ulike]," => like sources {0}".format(verdict))
print("\nLADDER:  spin-0 attract | spin-1 REPEL (magnetism) | spin-2 attract (gravity).")
print("=> The FORCE SIGN is set by the SPIN/STRUCTURE of the dynamic deformation (kinetic geometry):")
print("   only the VECTOR/vorticity (spin-1) gives like-repulsion. Gravity (tensor/spin-2) & a scalar attract.")
print("   BST carries both: vorticity=B (S59, magnetism), spin-2 curvature (S43/S54, gravity).")
