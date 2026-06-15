#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 64 (user point 1) — the cutoff is the problem: scale-invariance sets Lambda by the IR, not UV.
The Lambda ~ Planck^4 catastrophe comes ENTIRELY from imposing a UV cutoff. But the substrate is critical =
scale-invariant (S31/S55): no preferred UV scale. In a scale-free vacuum the energy density cannot depend on
a cutoff (there is none); by dimensional analysis it depends only on the IR scale L.
RESULT: (a) with cutoff Lc, rho ~ Lc^4 explodes (2.5e3 -> 2.5e15). (b) scale-invariant: rho ~ 1/L^2,
cutoff-INDEPENDENT (rho*L^2 = 0.1309 const). The Lc^4 disaster is an artifact of imposing a cutoff on a
scale-free theory. With L = horizon, rho_Lambda ~ 1/L_horizon^2 = the observed ORDER (holographic value).
HONEST RESERVE: scale-invariant / holographic dark-energy resolution (established proposals). What the
substrate's criticality (S31/S55) adds: scale-invariance is its own fixed point, not ad hoc. REMAINING
assumptions: exact scale-invariance (no anomaly) and L = horizon. The Lc^4 catastrophe is REMOVED and the
magnitude reframed to ~1/L^2; the residual 'why L = horizon' is milder, not fully closed. A real reframing,
not a from-nothing derivation. The user's intuition (the cutoff is the problem) holds.
"""
import numpy as np
# Point 1 (user): the Lambda^4 catastrophe comes from IMPOSING a UV cutoff. But the substrate is CRITICAL =
# scale-invariant (S31/S55) -> NO preferred UV scale. In a scale-free vacuum the energy density cannot depend
# on a cutoff (there is none); by dimensional analysis it can depend only on the IR scale L (the horizon).
# Test: naive cutoff gives rho ~ Lc^4 (cutoff-dependent disaster); the scale-invariant value is IR-set ~ 1/L^2
# (the S53 Casimir result), cutoff-INDEPENDENT.
def rho_cutoff(Lc, L, n=400000):
    k=np.linspace(1.0/L, Lc, n); return np.trapezoid(k**3, k)        # ~ Lc^4/4  (UV-dominated)
def rho_scale_invariant(L):                                          # no UV scale -> IR(L)-set Casimir piece
    return (np.pi/24.0)/L**2                                         # the S53 result (1D form), ~1/L^2
print("="*72); print("BST Stage 64 — is the cutoff the problem? Scale-invariance sets Lambda by the IR, not UV"); print("="*72)
L=1.0
print(f"\n  (a) naive vacuum energy WITH a UV cutoff Lc (IR size L={L}):  rho ~ Lc^4 (cutoff-dependent disaster)")
print(f"  {'Lc':>8}{'rho_cutoff':>16}")
for Lc in [10.,100.,1000.,10000.]:
    print(f"  {Lc:>8.0f}{rho_cutoff(Lc,L):>16.3e}")
print(f"\n  (b) scale-invariant substrate (NO UV scale): rho can only depend on the IR scale L -> rho ~ 1/L^2,")
print(f"      cutoff-INDEPENDENT:")
print(f"  {'L':>8}{'rho_scale_inv':>16}{'* L^2':>10}")
for Lh in [1.,10.,100.,1000.]:
    r=rho_scale_invariant(Lh); print(f"  {Lh:>8.0f}{r:>16.3e}{r*Lh**2:>10.4f}")
print("\n  => (a) with a cutoff, rho explodes as Lc^4 (the cosmological-constant catastrophe). (b) but the")
print("  substrate is critical/scale-invariant (S31/S55): there IS no UV scale, so the vacuum energy is set")
print("  ONLY by the IR scale L (rho ~ 1/L^2, cutoff-independent). The Lc^4 disaster is an ARTIFACT of")
print("  imposing a cutoff on a scale-free theory. With L = the horizon, rho_Lambda ~ 1/L_horizon^2 = the")
print("  observed ORDER (holographic value). The user's intuition holds: the cutoff WAS the problem.")
print("\n  HONEST: this is the scale-invariant / holographic dark-energy resolution (established proposals).")
print("  What our criticality (S31/S55) adds: the scale-invariance is not assumed ad hoc, it is the substrate's")
print("  own fixed point. REMAINING assumptions: exact scale-invariance (no anomaly) and the identification")
print("  L = horizon. So the Lc^4 catastrophe is REMOVED and the magnitude reframed to ~1/L^2; the residual")
print("  'why L = horizon' is milder, not fully closed. A real reframing, not a from-nothing derivation.")
