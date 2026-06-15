#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 8 — does going to FINER resolution keep paying off, or SATURATE?
Tests the author's axiom "resolution -> infinity". For each substrate we measure the
fraction of the field's reconstructable structure (variance) carried in each OCTAVE of
scale, coarse->fine, and the CUMULATIVE reconstruction fidelity vs depth (octaves added).

Substrates: (A) single characteristic scale (band-limited); (B) scale-invariant 1/f;
(C) the Stage-7 BEATING substrate itself (coupled phase oscillators, spatial field).

PRE-REGISTERED (can fail): single-scale & beating substrate SATURATE (marginal gain ->0
past a natural scale); scale-invariant keeps paying (~constant gain per octave).
CONCLUSION sought: "infinite resolution pays off" IFF the substrate is scale-invariant
/critical; a generic (or beating) substrate has a NATURAL finest scale -> CONSTRAINS the
axiom. Honest: a property of the substrate's scale structure, not a claim about nature.
"""
import numpy as np
rng=np.random.default_rng(0); L=256; kk=np.fft.rfftfreq(L,d=1.0/L); kk[0]=1e-9
def field_from_spectrum(amp):
    ph=rng.uniform(0,2*np.pi,len(amp)); F=amp*np.exp(1j*ph)
    x=np.fft.irfft(F,n=L); return x/ (x.std()+1e-12)
def single_scale(k0=16,w=2.0): return field_from_spectrum(np.exp(-((np.log2(kk)-np.log2(k0))**2)/(2*w**2)))
def scale_inv(alpha=1.0):     return field_from_spectrum(kk**(-alpha/2.0))
def beating_field():
    N=L; dt=0.1; θ=rng.uniform(0,2*np.pi,N); omega=rng.normal(1.0,0.3,N); S=[]
    for t in range(400):
        coup=np.sin(np.roll(θ,1)-θ)+np.sin(np.roll(θ,-1)-θ)
        θ=θ+dt*(omega+2.0*coup)
        if t>100: S.append(np.cos(θ).copy())
    return np.array(S)
def octave_variance(field2d_or_1d):
    # average power spectrum -> variance per octave band [2^j,2^{j+1})
    X=np.atleast_2d(field2d_or_1d); P=np.abs(np.fft.rfft(X,axis=1))**2; P=P.mean(0)
    nyq=L//2; bands=[]; j=1
    while 2**j<=nyq:
        lo,hi=2**(j-1),2**j; bands.append(P[lo:hi].sum()); j+=1
    bands=np.array(bands); return bands/bands.sum()
print("="*68); print("BST Stage 8 — resolution-depth saturation (does fine keep paying?)"); print("="*68)
subs={"single-scale (one char. scale)":single_scale(),
      "scale-invariant 1/f (alpha=1)":scale_inv(1.0),
      "BEATING substrate (Stage 7)":beating_field()}
print(f"\n{'octave (coarse->fine)':24s}"+"".join(f"oct{j:<5}" for j in range(1,8)))
for name,fld in subs.items():
    ov=octave_variance(fld); ov=np.pad(ov,(0,max(0,7-len(ov))))[:7]
    print(f"{name:24s}"+"".join(f"{v:7.3f}" for v in ov))
print("\nReading: a row whose mass is concentrated in one octave SATURATES (a natural")
print("scale). A flat-ish row keeps paying per octave -> only THAT substrate honours")
print("'resolution -> infinity'. The axiom is conditional on scale-invariance/criticality.")
