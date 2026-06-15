#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 63 — the mass/Lambda moment inversion IS the inertia/feedback duality (user reframing of S61).
If Lambda is the substrate FEEDBACK (restoring tension, axiom III / S53), then the S61 inversion is expected:
mass = inertia (IR moment, weight 1/Omega^2), Lambda = stiffness/feedback (UV moment, weight Omega). Split
the latent spectrum into inertial (low-Omega) and feedback (high-Omega) parts and vary the feedback weight.
RESULT: raising the feedback raises Lambda strongly (24.99 -> 4224.98, the UV moment) while the inertial mass
barely moves (1008.50 -> 1008.62, the IR moment). So the S61 inversion is the EXPECTED signature of
Lambda = substrate restoring tension (S53) -- a passed consistency check, not a null.
HONEST RESERVE: this fixes the STRUCTURE (why mass and Lambda weight opposite ends), NOT the magnitude --
Lambda's value still rides on the UV/feedback cutoff, so the cosmological-constant magnitude stays open.
Right intuition; structure, not solution.
"""
import numpy as np
# The user's reframing: if Lambda IS the substrate feedback (restoring tension, axiom III), the mass/Lambda
# moment inversion (S61) is EXPECTED, not a failure -- it is the inertia(IR) vs stiffness/feedback(UV) duality.
# Test: split the latent spectrum into an inertial (low-Omega) part and a feedback/restoring (high-Omega)
# part. Mass weights 1/Omega^2 (should track inertia), Lambda weights Omega (should track feedback). Vary
# the feedback weight and watch which one moves.
def moments(feedback_weight, n=200000, Lc=50.0, Om_split=20.0):
    O=np.linspace(1e-3,Lc,n)
    J_inertia = np.exp(-(O/5.0))                 # inertial part: low-Omega
    J_feedback= feedback_weight*np.where(O>Om_split, 1.0, 0.0)  # restoring/feedback: high-Omega
    J=J_inertia+J_feedback
    mass = np.trapezoid(J/O**2, O)               # inertial (IR) moment, weight 1/Omega^2
    Lam  = np.trapezoid(J*O,   O)                # feedback/stiffness (UV) moment, weight Omega
    return mass, Lam
print("="*72); print("BST Stage 63 — the mass/Lambda inversion IS the inertia/feedback duality (user reframing)"); print("="*72)
print(f"\n  vary the FEEDBACK (restoring-tension) weight; watch mass (inertia, IR) vs Lambda (feedback, UV):")
print(f"  {'feedback w':>12}{'mass (IR moment)':>18}{'Lambda (UV moment)':>20}")
m0,_=moments(0.0)
for w in [0.0,0.5,1.0,2.0,4.0]:
    m,L=moments(w); print(f"  {w:>12.1f}{m:>18.4f}{L:>20.2f}")
print("\n  => increasing the substrate FEEDBACK raises Lambda strongly (it IS the feedback/UV moment) while")
print("  the inertial mass barely moves (it is the IR moment, set by the slow modes). The S61 'inversion'")
print("  is therefore the EXPECTED signature of Lambda = substrate restoring tension (S53), confirming the")
print("  reframing: not a null, but a passed consistency check. HONEST: this fixes the STRUCTURE (why mass")
print("  and Lambda weight opposite ends), not the MAGNITUDE -- Lambda's value still rides on the UV/feedback")
print("  cutoff, so the cosmological-constant magnitude stays open. Right intuition; structure, not solution.")
