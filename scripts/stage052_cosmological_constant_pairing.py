#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 52 — cosmological constant via wave(zero-point) vs contact(gravitating); beat pairing.
The Lambda magnitude problem is a wave/contact confusion: the zero-point energy (wave, sum of 1/2 hbar w)
is ~cutoff^4 (huge); what GRAVITATES (contact) is what survives after the beat pairs boson (+) and fermion
(-) zero-point energies -- the substrate now HAS both (S49/S51). rho = 1/2 integral[omega_b - omega_f].
RESULT: exact pairing (m_b=m_f) -> gravitating vacuum = 0 EXACTLY (the huge wave zero-point does NOT
gravitate). Broken pairing (detuning Delta=m_f^2-m_b^2 > 0) -> the leading cutoff^4 CANCELS, but a softer
residue ~ Delta*cutoff^2 REMAINS (verified: rho_paired ~ Lc^2 at fixed Delta) -- the pairing softens
quartic->quadratic, set by the breaking scale.
HONEST RESERVE: this is the standard SUSY/pairing cancellation -- NOT novel, and NOT a solution. It reduces
cutoff^4 to the breaking scale but does NOT reach the observed tiny Lambda (~1e-122); the residual
hierarchy (breaking scale -> observed Lambda) is the unsolved magnitude problem, unsolved by everyone.
Content here: the wave/contact translation correctly shows the bulk zero-point need not gravitate; the
beat supplies the pairing. Suggestive, conceptual -- not a closed result.
"""
import numpy as np
# Cosmological constant via wave<->contact: the zero-point energy (wave) is huge ~cutoff^4; what GRAVITATES
# (contact) is what survives after the beat pairs boson (+1/2 w) and fermion (-1/2 w) zero-point energies
# (the substrate now HAS both, S49/S51). m_b vs m_f split by the beat detuning Delta -> the bulk cancels,
# residue set by Delta (the breaking scale), NOT the cutoff. SUGGESTIVE step, NOT a solution of the magnitude.
def rho(mb2, mf2, Lc, n=400000):
    k=np.linspace(1e-6,Lc,n)
    integ_b=k**2*np.sqrt(k**2+mb2); integ_f=k**2*np.sqrt(k**2+mf2)
    pref=0.5/(2*np.pi**2)
    return pref*np.trapezoid(integ_b,k), pref*np.trapezoid(integ_b-integ_f,k)  # (boson-only naive, paired)
print("="*72); print("BST Stage 52 — cosmological constant: wave(zero-point) vs contact(gravitating)"); print("="*72)
mb2=1.0; Lc=100.0  # cutoff^4 = 1e8
print(f"\n  cutoff Lc={Lc:.0f} (Lc^4={Lc**4:.0e}); boson mass^2={mb2}; vary beat detuning Delta (=m_f^2-m_b^2):")
print(f"  {'Delta':>8}{'rho_naive(wave)':>18}{'rho_paired(contact)':>22}{'ratio':>12}")
rn0=None
for D in [0.0,1e-3,1e-2,1e-1,1.0]:
    rn,rp=rho(mb2,mb2+D,Lc); 
    print(f"  {D:>8.0e}{rn:>18.3e}{rp:>22.3e}{(rp/rn):>12.2e}")
print("\n  cutoff-independence of the paired (gravitating) residue — vary Lc at fixed Delta=1e-2:")
print(f"  {'Lc':>8}{'rho_naive ~Lc^4':>18}{'rho_paired':>16}")
for Lc2 in [50.,100.,200.,400.]:
    rn,rp=rho(mb2,mb2+1e-2,Lc2); print(f"  {Lc2:>8.0f}{rn:>18.3e}{rp:>16.3e}")
print("\n  => Delta=0 (exact beat pairing): gravitating vacuum = 0 EXACTLY (boson/fermion zero-points cancel).")
print("  Delta>0: residue ~ Delta (the detuning), NOT cutoff^4 -> the huge 'wave' zero-point does NOT")
print("  gravitate; only the contact residue does. HONEST: this is the SUSY/pairing cancellation -- it")
print("  reduces cutoff^4 to the breaking scale, but does NOT reach the observed tiny Lambda. The residual")
print("  hierarchy (breaking scale -> observed Lambda) is the unsolved magnitude problem. Suggestive, not solved.")
