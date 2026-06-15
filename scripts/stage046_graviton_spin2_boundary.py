#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 46 — 3+1 graviton: γ_PPN is fixed by the mediator SPIN; the precise boundary.
The 3+1 Einstein test reduces to one fact: the PPN γ_PPN is set by the mediator's SPIN. spin-0 (sound)
-> γ_PPN=0; spin-2 (graviton), via its TRACE-REVERSED source, sources h_ij exactly as much as h_00 ->
γ_PPN=1 (the factor-2 light bending), automatically. We compute h_00, h_ij from a static mass for each
spin and the resulting deflection.

RESULT: spin-0 -> h_00=0.5, h_ii=0, γ_PPN=0, deflection 2.32deg; spin-2 -> h_00=0.5, h_ii=0.5, γ_PPN=1,
deflection 4.72deg (ratio 2.03 = Einstein factor 2). So γ_PPN=1 REQUIRES a spin-2 mediator. The
substrate's generic propagating modes are spin-0 (sound) + spin-1 (shear, S43); in ordinary elasticity
the strain is partial-u (slaved to the vector displacement), NOT an independent propagating spin-2 field.
=> the 3+1 graviton is NOT present generically; it needs the independent spin-2 CURVATURE/DEFECT sector
(Kleinert second-gradient elasticity), a POSITED ingredient the beating substrate does not force.

HONEST BOUNDARY (the gravity arc's floor, mapped not masked): we know EXACTLY what is missing (a
propagating spin-2 graviton), WHY (the trace-reversed coupling), and WHAT would supply it (the Kleinert
curvature sector). The substrate delivers up to spin-1 and EXACT conical/2+1 Einstein (S45); 3+1
localized-mass Einstein with a propagating graviton remains a posited extension, not a forced link.
"""
import numpy as np
rho=1.0; eta=np.array([1.0,-1.0,-1.0,-1.0]); T=np.zeros((4,4)); T[0,0]=rho; trT=rho
def γ_PPN_from_source(spin):
    if spin==2:   S00=T[0,0]-0.5*eta[0]*trT; Sii=-0.5*eta[1]*trT
    elif spin==0: S00=0.5*trT; Sii=0.0
    Phi=S00/2.0; γ_PPN=(Sii/2.0)/Phi if Phi!=0 else 0.0
    return S00,Sii,γ_PPN
def deflect(gs,GM=0.02,b=1.0,soft=0.04,Lh=60.0,ds=0.0015):
    pos=np.array([-Lh,b]); d=np.array([1.0,0.0])
    for _ in range(int(2*Lh/ds)):
        r=np.sqrt(pos[0]**2+pos[1]**2+soft**2)
        g=-(1+gs)*GM*pos/r**3; perp=g-np.dot(d,g)*d
        d=d+ds*perp/(1+(1+gs)*GM/r); d/=np.linalg.norm(d); pos=pos+ds*d
        if pos[0]>=Lh: break
    return -np.degrees(np.arctan2(d[1],d[0]))
print("="*72); print("BST Stage 46 — 3+1 graviton: γ_PPN is fixed by mediator SPIN"); print("="*72)
print(f"\n  {'mediator':>18}{'h_00':>8}{'h_ii':>8}{'γ_PPN':>8}{'deflection(deg)':>17}")
a0=deflect(0.0)
for spin,name in [(0,'spin-0 (sound)'),(2,'spin-2 (graviton)')]:
    h00,hii,g=γ_PPN_from_source(spin)
    print(f"  {name:>18}{h00:>8.2f}{hii:>8.2f}{g:>8.2f}{deflect(g):>17.4f}")
print(f"\n  spin-2 / spin-0 deflection ratio = {deflect(1.0)/a0:.3f}  (= 2: the Einstein factor 2)")
print("\n  => γ_PPN=1 REQUIRES a spin-2 mediator. Substrate modes: spin-0 (sound) + spin-1 (shear, S43),")
print("  NO independent propagating spin-2. 3+1 Einstein needs the spin-2 curvature/defect field")
print("  (Kleinert second-gradient) -- posited, not forced. The precise, mapped boundary of the arc.")
