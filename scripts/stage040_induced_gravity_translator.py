#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 40 — the 'translator' for the Einstein magnitude: long-range force needs a GAPLESS mediator.
User's idea: Einstein's magnitude is the coarse-grained collective effect of many kinks at large scale --
a 'translation' from micro-kinks to the macro law. This IS Sakharov induced gravity (G emergent, not
fundamental). HONEST OBSTACLE (demonstrated here): a kink's curvature (S39) is LOCAL/short-range, while
Einstein-Newton gravity is LONG-RANGE (1/r). Coarse-graining a local response stays local. ESCAPE the
framework already has: a long-range force requires a GAPLESS mediator -- and the substrate supplies one,
the Goldstone mode (S27). 

Test: two static masses coupled to a scalar mediator chi obeying (lap - mu^2) chi = -source. Interaction
potential U(d) = M1 M2 * G(d) with G the mediator's Green function. PRE-REGISTERED: GAPLESS (mu=0) ->
U(d) ~ -log d (2D), LONG-RANGE; GAPPED (mu>0) -> U(d) ~ K0(mu d) ~ e^{-mu d}, SHORT-RANGE (range ~1/mu).
Only the gapless mediator gives a gravity-like long-range force; U is exactly proportional to M1*M2 (the
field equation is linear), with the coupling = the 'translator' magnitude.
HONEST: this locates WHERE the Einstein magnitude lives (the kink<->Goldstone coupling, Sakharov-style,
set by micro-params) and what it requires (a gapless mediator). It does NOT fix the absolute value to
nature's G, and true Einstein is 3+1 & nonlinear; the STRUCTURE (long-range, ~M1 M2, universal coupling)
is what emerges. 2D.
"""
import numpy as np
N=1024; L=400.0; dx=L/N
k=2*np.pi*np.fft.fftfreq(N,d=dx); KX,KY=np.meshgrid(k,k); K2=KX**2+KY**2
def green_row(mu):
    src=np.zeros((N,N)); src[N//2,N//2]=1.0/dx**2
    denom=K2+mu**2
    if mu==0: denom[0,0]=1.0
    chi=np.real(np.fft.ifft2(np.fft.fft2(src)/denom))
    if mu==0: chi-=chi.mean()
    return chi[N//2,N//2:]          # radial profile from center outward
r=np.arange(N//2)*dx
g0=green_row(0.0)        # gapless (Goldstone-like)
gm=green_row(0.1)        # gapped (mu=0.1 -> range ~10)
print("="*78); print("BST Stage 40 — does the kink-kink force go long-range only with a gapless mediator?"); print("="*78)
print(f"\n  Interaction potential U(d) = M1 M2 * G(d) between two masses, separation d.")
print(f"  {'d':>6}{'U_gapless(d)':>15}{'U_gapped(d) mu=0.1':>20}{'-log(d)/2pi (ref)':>19}")
for d in [5,10,20,40,80,150]:
    i=int(d/dx); ref=-np.log(d)/(2*np.pi)
    print(f"  {d:>6}{g0[i]:>15.5f}{gm[i]:>20.6f}{ref:>19.5f}")
# ranges: ratio U(large)/U(small)
i5=int(5/dx); i80=int(80/dx)
print(f"\n  range check  U(80)/U(5):  gapless = {g0[i80]/g0[i5]:+.3f}   gapped = {gm[i80]/gm[i5]:+.3e}")
print(f"  gapless: slowly varying (logarithmic, LONG-range).  gapped: ~0 by d=80 (e^-mu d, SHORT-range).")
# force F=-dU/dd (gapless) vs 1/d reference
i20,i21=int(20/dx),int(20/dx)+1
F=-(g0[i21]-g0[i20])/dx
print(f"\n  gapless force at d=20:  F = -dU/dd = {F:.5f}   vs  1/(2pi d) = {1/(2*np.pi*20):.5f}  (2D gravity ~1/d)")
print("\n  => only the GAPLESS mediator (the Goldstone mode, S27) gives the long-range, ~M1 M2 force.")
print("  The 'translator' = the kink<->Goldstone coupling (its strength = the emergent magnitude).")
print("  BOUNDARY: structure emerges (long-range, ~M1M2, universal coupling); absolute G not fixed; true")
print("  Einstein is 3+1 & nonlinear. The local kink curvature (S39) alone stays short-range.")
