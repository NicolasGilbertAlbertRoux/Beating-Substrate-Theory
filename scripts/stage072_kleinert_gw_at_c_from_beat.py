#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 72 (Kleinert / GW-at-c) - where does the speed c of the spin-2 field come from?
A transverse-traceless spin-2 field has helicity 2 at ANY speed (rotates e^{2i phi}, verified ratio 2.0000).
Its speed = sqrt(stiffness/inertia). Two substrate origins: elastic shear mu -> v=0.444<c (S57 problem) OR the
conservative BEAT -> v=1=c (S34 light cone). RESULT: GW-at-c is REACHABLE conditional on ONE named
identification - the spin-2 CURVATURE (disclination) field takes its kinetic/restoring term from the
conservative beat (S34, already derived at c), not the elastic shear. Then omega=c*k for a helicity-2 mode =
gravitational waves at c; with the trace-reversed source (S58) -> full Einstein bending (γ_PPN=1). THE POSIT,
precisely: 'the curvature field couples to the beat, not the shear' - exactly where the user's action/feedback
= beat/counter-beat belongs (the curvature field's kinetic term). Natural (beat = fundamental conservative
mode, axiom III; curvature = fundamental geometry) but a POSIT, not a derivation. Wall reduced from 'needs a
posited light-speed spin-2 field' to 'curvature kinetic term = the beat' - a single named on-theme identification.
"""
import numpy as np
print("="*76)
print("BST Stage 72 - Kleinert / GW-at-c: where does the speed c of the spin-2 field come from?")
print("="*76)
# A transverse-traceless spin-2 field h has helicity 2 (rotates e^{2i*phi}, S54) at ANY speed. Its speed is
# sqrt(stiffness/inertia). Two candidate stiffnesses in the substrate: the ELASTIC shear mu (-> c_T, sub-c,
# S57) or the CONSERVATIVE BEAT (-> c, already derived in S34). GW-at-c <=> the curvature field takes the
# BEAT stiffness, not the elastic one. This is the precise Kleinert posit, now named & on-theme.

print("\n(1) helicity of a transverse-traceless spin-2 mode is 2 regardless of speed (S54 recap):")
phi=0.7
# TT polarization tensor components (h_plus, h_cross) rotate by 2*phi
R=np.array([[np.cos(2*phi),-np.sin(2*phi)],[np.sin(2*phi),np.cos(2*phi)]])
e=np.array([1.0,0.0])  # plus-polarization
print(f"   under a spatial rotation by phi={phi}, the polarization rotates by 2*phi -> helicity 2 (exact): "
      f"angle ratio = {np.arctan2((R@e)[1],(R@e)[0])/phi:.4f}")

print("\n(2) speed of the spin-2 wave = sqrt(stiffness/inertia). Two substrate origins:")
rho=1.0; mu=0.197; beat_stiffness=1.0   # mu from S43 (vortex lattice); beat = conservative c-sector (S34, c=1)
cT=np.sqrt(mu/rho); cbeat=np.sqrt(beat_stiffness/rho)
print(f"   elastic shear  : v = sqrt(mu/rho)   = {cT:.3f}  < c   (the S57 sub-luminal problem)")
print(f"   conservative beat: v = sqrt(K_beat/rho) = {cbeat:.3f} = c   (the S34 light cone)")

print("\n(3) GW dispersion if the curvature field takes the BEAT stiffness:")
ks=np.array([0.5,1.0,2.0,4.0]); omega=cbeat*ks
print(f"   k     = {ks}")
print(f"   omega = {omega}   -> omega = c*k exactly: massless spin-2 at c = gravitational waves at c.")

print("\nVERDICT (pre-registered)")
print("  GW-AT-c IS REACHABLE, conditional on ONE named identification: the spin-2 CURVATURE (disclination)")
print("  field takes its kinetic/restoring term from the CONSERVATIVE BEAT (S34, already derived at c), not from")
print("  the elastic shear mu (S57, sub-c). Then omega=c*k for a helicity-2 mode = gravitational waves at c, and")
print("  with the trace-reversed source (S58) this gives full Einstein bending (γ_PPN=1).")
print("  THE POSIT, precisely: 'the curvature field couples to the beat, not the shear.' This is exactly where")
print("  the user's action/feedback = beat/counter-beat belongs - as the curvature field's kinetic term. It is")
print("  NATURAL (the beat is the substrate's fundamental conservative mode, axiom III; curvature is fundamental")
print("  geometry, so coupling to the fundamental beat rather than the emergent elastic shear is the natural")
print("  choice) - but it remains a POSIT, not a derivation. So GW-at-c = conditional Kleinert, now with the c")
print("  sourced from the already-derived beat. Wall reduced from 'needs a posited light-speed spin-2 field' to")
print("  'the curvature field's kinetic term is the beat' - a single, named, on-theme identification.")
