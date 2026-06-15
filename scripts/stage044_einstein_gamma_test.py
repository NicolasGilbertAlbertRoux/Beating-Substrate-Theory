#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 44 — does coupling mass to the shear (spin-2) sector give γ_PPN=1 (true Einstein)?
S43 found the transverse/shear modes. For TRUE Einstein the mass must curve space as much as time
(h_ij=h_00, γ_PPN=1) AND with the SAME range as the potential. Two known pitfalls (Kleinert world
crystal): (a) a point source (center of dilation) has a 1/r^2 short-range elastic field -- wrong range;
the long-range mass-like source is a DISCLINATION (~log r in 2D); (b) even then, ORDINARY elasticity
does not give exactly γ_PPN=1 -- a special (second-gradient) elasticity is needed.

RESULTS (no fit): (1) the shear sector makes γ_PPN=1 REACHABLE -- ray-traced deflection alpha ~ (1+γ_PPN):
γ_PPN=0 -> 2.32deg (x1.00, scalar), 0.5 -> 3.51 (x1.51), 1.0 -> 4.72 (x2.03 = Einstein factor 2).
(2) our crystal's moduli (S43: mu=0.197, lambda=1.269, 2D Poisson nu=0.763), under the SIMPLEST strain-
as-metric identification, give γ_PPN ~ 0.89 -- close to 1 but IDENTIFICATION-DEPENDENT (not a derivation).
VERDICT: γ_PPN=1 (Einstein) is REACHABLE and the substrate is in the right ballpark, but γ_PPN=1 EXACT is
NOT generically forced -- it needs a long-range (disclination) source AND a special (Kleinert) elasticity.
The generic crystal gives γ_PPN>0 (tensor gravity, light bends) -- far past the scalar γ_PPN=0 -- but not
guaranteed Einstein. So likely NOT the final link, but the one bringing Einstein within reach and naming
the last condition (the Einstein/Kleinert coupling). 2D.
"""
import numpy as np
def deflect(gs, GM=0.02, b=1.0, soft=0.04, Lh=60.0, ds=0.0015):
    pos=np.array([-Lh,b]); d=np.array([1.0,0.0])
    for _ in range(int(2*Lh/ds)):
        r=np.sqrt(pos[0]**2+pos[1]**2+soft**2)
        g=-(1+gs)*GM*pos/r**3; perp=g-np.dot(d,g)*d
        d=d+ds*perp/(1+(1+gs)*GM/r); d/=np.linalg.norm(d); pos=pos+ds*d
        if pos[0]>=Lh: break
    return -np.degrees(np.arctan2(d[1],d[0]))
a0=deflect(0.0)
print("="*72); print("BST Stage 44 — is γ_PPN=1 (true Einstein) reachable from the shear sector?"); print("="*72)
print("\n  (1) deflection vs spatial-curvature coupling γ_PPN (alpha ~ 1+γ_PPN):")
print(f"  {'γ_PPN':>9}{'alpha(deg)':>12}{'alpha/alpha0':>14}")
for gs in [0.0,0.5,1.0]:
    a=deflect(gs); tag="  <- Einstein (factor 2)" if abs(gs-1)<1e-9 else ""
    print(f"  {gs:>9.2f}{a:>12.4f}{a/a0:>14.3f}{tag}")
mu=0.197; rho=0.8019; cL=1.44; lam=rho*cL**2-2*mu
nu2D=lam/(lam+2*mu); γ_PPN_est=(1/mu)/((1/mu)+1/(lam+2*mu))
print(f"\n  (2) our crystal (S43): mu={mu}, lambda={lam:.3f}, 2D Poisson nu={nu2D:.3f}")
print(f"      simplest strain-as-metric estimate -> γ_PPN ~ {γ_PPN_est:.2f}  (identification-dependent!)")
print("\n  VERDICT: shear/spin-2 modes (S43) make γ_PPN=1 REACHABLE (advance over scalar γ_PPN=0), but")
print("  γ_PPN=1 is NOT generically forced -- needs a long-range (disclination) source AND a special")
print("  (Kleinert second-gradient) elasticity. Generic crystal: γ_PPN>0 (tensor gravity) but not Einstein.")
