#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 45 — disclination = cone = 2+1 Einstein point mass: EXACT conical lensing.
S44 left the Einstein coupling undetermined. Here we take the correct long-range source -- a DISCLINATION
(a defect makeable in the S43 crystal) -- which turns an elastic sheet into a CONE (deficit angle delta).
EXACT correspondence (Deser-Jackiw-'t Hooft): a point mass in 2+1 GR produces exactly a conical spacetime,
deficit delta = 8 pi G M. So disclination = cone = 2+1 Einstein point mass, NO approximation, NO tunable
coupling.

We integrate geodesics on the cone metric ds^2 = dr^2 + alpha^2 r^2 dphi^2 (alpha = 1 - delta/2pi), using
r = rp sec(theta) to smooth the perihelion (b kept explicit). RESULT: deflection = pi(1-alpha)/alpha,
matched to 3-4 digits, and INDEPENDENT of impact parameter b (16.36 deg at b=1,5,20 for delta=30; 36.0 for
60; 60.0 for 90) -- the conical / 2+1 / cosmic-string signature. This IS exact Einstein gravitational
lensing in the conical case; delta = 8 pi G M fixes the magnitude.

HONEST BOUND: exact Einstein in the CONICAL case (2+1 gravity, or cosmic strings in 3+1). 2+1 gravity has
NO propagating graviton; its lensing (impact-parameter-independent deficit) is a DIFFERENT structure from
the 3+1 Schwarzschild factor-2 (gamma=1) bending of a LOCALIZED mass. So this closes the conical Einstein
exactly; 3+1 localized-mass Einstein with propagating gravitons remains the open frontier. A first first-
principles EXACT Einstein from the substrate, honestly bounded.
"""
import numpy as np
def deflection_numeric(delta_deg, b, n=200000):
    alpha=1-delta_deg/360.0; L=b; rp=L/alpha
    th=np.linspace(1e-9, np.pi/2-1e-9, n)
    r=rp/np.cos(th); drdth=rp*np.sin(th)/np.cos(th)**2
    val=np.clip(1-L**2/(alpha**2*r**2),1e-15,None)
    integrand=(L/(alpha**2*r**2))/np.sqrt(val)
    return np.degrees(2*np.trapezoid(integrand*drdth, th)-np.pi)
print("="*72); print("BST Stage 45 — disclination = cone = 2+1 Einstein mass: exact conical lensing"); print("="*72)
print("\n  geodesic deflection past a conical deficit delta (disclination):")
print(f"  {'delta(deg)':>11}{'b=1':>10}{'b=5':>10}{'b=20':>10}{'pi(1-a)/a':>12}")
for dd in [30.0,60.0,90.0]:
    a=1-dd/360.0; exact=np.degrees(np.pi*(1-a)/a)
    print(f"  {dd:>11.0f}{deflection_numeric(dd,1.0):>10.3f}{deflection_numeric(dd,5.0):>10.3f}{deflection_numeric(dd,20.0):>10.3f}{exact:>12.3f}")
print("\n  => deflection INDEPENDENT of impact parameter b (conical / 2+1 / cosmic-string signature),")
print("  matching pi(1-alpha)/alpha exactly. EXACT Einstein in the conical case:")
print("  disclination = cone = 2+1 point mass, delta = 8 pi G M. (3+1 propagating graviton: still open.)")
