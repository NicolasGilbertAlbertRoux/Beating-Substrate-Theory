#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 53 — does Lambda vary with the bounded size L? (the substrate's restoring tension; user lead 6a).
The substrate's restoring tension (axiom III, return-to-equilibrium) confined to a region of size L = the
finite-size (Casimir) part of the zero-point energy. Modes omega_n = n*pi/L; subtract the extensive bulk
(~L/eps^2, the cutoff vacuum); the L-dependent CASIMIR residue is the gravitating (contact) tension.
RESULT: E_Casimir * L = -pi/24 = -0.1309 constant across L=1..16 -> E_Casimir ~ 1/L, energy DENSITY ~ 1/L^2.
So Lambda decreases as 1/L^2: negligible toward large L, formidable toward small L = exactly the user's
intuition (a scale-dependent feedback tension).
HONEST RESERVE: this is Casimir / holographic dark energy (established idea, Lambda ~ 1/L^2). With L = the
horizon it gives the right ORDER of magnitude (the Lambda ~ H0^2 coincidence), but L=horizon is an INPUT,
not derived -> the magnitude is matched, not solved. The SCALING (1/L^2) is the genuine result and it
vindicates the lead; the absolute magnitude stays open.
"""
import numpy as np
# Does Lambda vary with the bounded size L? The substrate's restoring tension (axiom III) in a confined
# region = the finite-size (Casimir) part of the zero-point energy. Modes omega_n = n*pi/L (c=1). The
# bulk piece ~ L/eps^2 (extensive, the cutoff vacuum) is subtracted; the L-dependent CASIMIR residue is
# the gravitating (contact) tension. Test its scaling with L.
def casimir_1d(L, eps, N=2_000_000):
    n=np.arange(1,N+1); a=eps*np.pi/L
    E=(np.pi/(2*L))*np.sum(n*np.exp(-a*n))     # regularized zero-point energy
    bulk=L/(2*np.pi*eps**2)                      # extensive bulk (continuum) piece
    return E-bulk                                # Casimir finite part
print("="*72); print("BST Stage 53 — does Lambda vary with bounded size L? (substrate restoring tension)"); print("="*72)
eps=2e-3
print(f"\n  finite-size (Casimir) vacuum energy vs L   [exact zeta result: E_C = -pi/24L = {-np.pi/24:.5f}/L]")
print(f"  {'L':>6}{'E_Casimir':>14}{'E_C * L':>12}{'density E/L^2 ~':>18}")
for L in [1.0,2.0,4.0,8.0,16.0]:
    Ec=casimir_1d(L,eps); print(f"  {L:>6.1f}{Ec:>14.5f}{Ec*L:>12.5f}{Ec/L:>18.6f}")
print(f"\n  => E_Casimir * L = const = -pi/24  -> E_Casimir ~ 1/L, energy DENSITY ~ 1/L^2.")
print("  So the substrate's restoring tension gives a vacuum energy density that SCALES as 1/L^2:")
print("  negligible toward large L (one infinity), formidable toward small L (the other) -- exactly")
print("  the intuition. HONEST: this is Casimir / holographic dark energy (established: Lambda ~ 1/L^2);")
print("  with L = the horizon it gives the right ORDER of magnitude (the Lambda~H0^2 coincidence), but")
print("  L=horizon is an INPUT, not derived -> the magnitude is matched, not solved. The SCALING is the win.")
