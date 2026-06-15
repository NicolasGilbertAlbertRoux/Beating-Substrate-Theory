#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 61 (lead 1) — latent origin of mass and Lambda: linked, but opposite spectral moments.
Both the particle mass (latent dressing / self-energy) and Lambda (latent gravitating vacuum) come from the
SAME latent spectral density J(Omega). Pre-registered test of whether the link FIXES the Lambda magnitude.
RESULT: mass shift dm^2 = integral J/Omega^2 ~ log(Lc) (IR-dominated, set by LOW latent modes); vacuum energy
~ integral J*Omega ~ Lc^3 (UV-dominated, set by HIGH latent modes). They are OPPOSITE spectral moments. So
mass and Lambda DO share one latent origin (a genuine conceptual unification: two faces of the latent zero-
point energy), but knowing the mass scale (IR) does NOT fix Lambda (UV) -> the magnitude is not transferred.
PRE-REGISTERED RESULT: NULL on "solving the Lambda magnitude". The link is real in ORIGIN, but opposite
moments -> the cosmological-constant magnitude stays open (as for everyone). HONEST: mass renormalization
and vacuum energy being the same vacuum fluctuations is standard QFT; the substrate adds the unified latent
picture, NOT a solution. The user's idea was right about the unification, not about a magnitude solution.
"""
import numpy as np
# Lead 1: are the mass (latent dressing/self-energy) and Lambda (latent gravitating vacuum) linked enough to
# fix Lambda's magnitude? Both come from the SAME latent spectral density J(Omega). Pre-registered test:
# compute how each weights J. Mass dressing weights 1/Omega^2 (IR, low modes); vacuum energy weights Omega
# (UV, high modes). If they weight OPPOSITE ends, the link is real in ORIGIN but does NOT transfer the scale.
def latent(Lc, n=200000, s=1.0):
    O=np.linspace(1e-3,Lc,n); J=O**s                       # latent spectral density J(Omega)=Omega^s (ohmic s=1)
    dm2=np.trapezoid(J/O**2,O)                              # mass dressing (self-energy), IR-weighted (1/O^2)
    rho_unpaired=0.5*np.trapezoid(J*O,O)                    # vacuum energy, UV-weighted (O)
    # boson/fermion pairing (S52) with detuning Delta cancels the bulk:
    Of=np.sqrt(O**2+ (0.05*Lc)**2); Jf=Of**s
    rho_paired=0.5*np.trapezoid(J*O - Jf*Of,O)
    return dm2,rho_unpaired,rho_paired
print("="*72); print("BST Stage 61 — latent origin of mass & Lambda: linked, but opposite spectral moments"); print("="*72)
print(f"\n  both mass-dressing and Lambda come from the SAME latent spectrum J(Omega). How do they scale with")
print(f"  the latent cutoff Lc?")
print(f"  {'Lc':>8}{'mass shift dm^2':>18}{'Lambda (unpaired)':>20}{'Lambda (paired)':>18}")
for Lc in [10.,20.,40.,80.]:
    dm2,ru,rp=latent(Lc); print(f"  {Lc:>8.0f}{dm2:>18.4f}{ru:>20.3e}{rp:>18.3e}")
print("\n  => mass shift dm^2 ~ log(Lc) (almost FLAT: IR-dominated, set by LOW latent modes).")
print("     Lambda ~ Lc^3 (steeply UV-dominated, set by HIGH latent modes). They probe OPPOSITE ends of")
print("     the latent spectrum. So mass and Lambda DO share a single latent origin (a real conceptual")
print("     unification: two faces of the latent zero-point energy), but knowing the mass scale (IR) does")
print("     NOT fix Lambda (UV). The magnitude is NOT transferred.")
print("\n  PRE-REGISTERED RESULT: NULL on 'solving the Lambda magnitude'. The latent link is genuine in ORIGIN")
print("  but the two phenomena are opposite spectral moments -> the cosmological-constant magnitude stays")
print("  open (as it does for everyone). HONEST: mass renormalization and vacuum energy being the same")
print("  vacuum fluctuations is standard QFT; the substrate adds the unified 'latent' picture, not a solution.")
