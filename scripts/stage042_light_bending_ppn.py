#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 42 — light bending pinpoints the Newton->Einstein gap (γ_PPN).
S41 reached Newton via a SCALAR mediator; full Einstein needs the SPIN-2 (tensor) structure. The clean
discriminator (historically THE one) is LIGHT BENDING. In the weak field ds^2 = -(1+2Phi)dt^2 +
(1-2 γ_PPN Phi)dx^2, the photon deflection ~ (1+γ_PPN): SCALAR gravity curves only time (γ_PPN=0) ->
HALF; EINSTEIN curves space too (γ_PPN=1) -> the famous FACTOR 2. (Cassini: γ_PPN=1.000 +/- 2e-5.)

We ray-trace a null ray (Fermat/eikonal, index n=1+(1+γ_PPN)GM/r) past a mass for γ_PPN=0, 1/3, 1 and
read the deflection. PRE-REGISTERED: alpha ~ (1+γ_PPN), so alpha(1)/alpha(0)=2, alpha(1/3)/alpha(0)=4/3.
KEY HONEST POINT: the substrate's SCALAR Goldstone (S40/41) gives γ_PPN=0; and its ACOUSTIC metric (S35),
though tensorial, is conformal to -c^2 dt^2 + dx^2 and null geodesics are conformally invariant, so light
sees only c(x) (a refractive index) -> γ_PPN=0 TOO. So the substrate sits at γ_PPN=0 = HALF the Einstein
bending. The FACTOR 2 (spatial curvature, γ_PPN=1) is exactly what it LACKS -- and is observationally
ruled in for GR. That is the precise, named gap: it requires the genuine spin-2 Einstein field equations,
the 40-year-open boundary of emergent/analog gravity. The chain reaches Newton + equivalence + a refractive
(γ_PPN=0) light bending; Einstein's γ_PPN=1 is beyond it.
"""
import numpy as np
def deflection_deg(γ_PPN, GM=0.02, b=1.0, soft=0.04, Lhalf=60.0, ds=0.0015):
    pos=np.array([-Lhalf,b]); d=np.array([1.0,0.0])
    def gradn(p):
        r=np.sqrt(p[0]**2+p[1]**2+soft**2); return -(1+γ_PPN)*GM*p/r**3
    def n_at(p):
        r=np.sqrt(p[0]**2+p[1]**2+soft**2); return 1.0+(1+γ_PPN)*GM/r
    for _ in range(int(2*Lhalf/ds)):
        g=gradn(pos); n=n_at(pos); perp=g-np.dot(d,g)*d
        d=d+ds*perp/n; d=d/np.linalg.norm(d); pos=pos+ds*d
        if pos[0]>=Lhalf: break
    return -np.degrees(np.arctan2(d[1],d[0]))     # magnitude of downward bend toward the mass
print("="*72); print("BST Stage 42 — light bending: where does the substrate sit (γ_PPN)?"); print("="*72)
a0=deflection_deg(0.0); a13=deflection_deg(1/3); a1=deflection_deg(1.0)
print(f"\n  null-ray deflection (GM=0.02, b=1):")
print(f"  {'γ_PPN':>8}{'who':>34}{'alpha (deg)':>13}{'alpha/alpha(0)':>16}")
print(f"  {0.0:>8.2f}{'scalar Goldstone (S40/41) & acoustic':>34}{a0:>13.4f}{a0/a0:>16.3f}")
print(f"  {1/3:>8.2f}{'(intermediate reference)':>34}{a13:>13.4f}{a13/a0:>16.3f}")
print(f"  {1.0:>8.2f}{'EINSTEIN (GR, Cassini-confirmed)':>34}{a1:>13.4f}{a1/a0:>16.3f}")
print(f"\n  alpha ~ (1+γ_PPN):  alpha(1)/alpha(0) = {a1/a0:.3f} (pred 2.00);  alpha(1/3)/alpha(0) = {a13/a0:.3f} (pred 1.33)")
print("\n  => the substrate (scalar Goldstone + acoustic metric) sits at γ_PPN=0 -> HALF the Einstein bending.")
print("  The factor-2 (spatial curvature, γ_PPN=1) is the precise GAP: it needs the spin-2 Einstein")
print("  field equations -- the chain reaches Newton + equivalence + refractive (γ_PPN=0) bending, not GR.")
