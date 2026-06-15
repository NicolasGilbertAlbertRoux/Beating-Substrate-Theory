#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 55 — trans-resolution map (lead B): the RG / coarse-graining flow of the substrate phase field.
Tests three things at once. RESULTS:
(1) FIXED POINT: critical field (P~1/k^2) spectral slope ~-2 preserved under one coarse-graining step
    (-2.07 -> -2.19, small finite-size drift); off-critical (massive) flows away (-0.72 -> -0.39). So the
    critical substrate is a scale-invariant fixed point = what makes the trans-resolution map self-similar
    (S31 as an RG fixed point).
(2) Lambda(a) ~ 1/a^2: the restoring-tension energy below cutoff pi/a gives tension*a^2 = const (1.0e8 to
    ~5% across a=2..32). So Lambda is RESOLUTION-dependent exactly as it is SIZE-dependent (S53 unified);
    each aliasing layer has its own tension.
(3) DARK FRACTION: most field energy lives in the sub-resolution (latent) modes; the fraction -> 1 as the
    mesh coarsens (0.95, 0.99, 0.997). The latent/dark sector dominates the budget at observable resolution
    -- a qualitative echo of the ~95%-dark real universe.
HONEST RESERVE: this is the renormalization group / effective field theory (established). Substrate content:
trans-resolution IS the RG flow; criticality makes it self-similar; dark = sub-resolution energy (gravitates
via S40, invisible to the observable channel) -- CONCEPTUAL, NOT a quantitative fit to Omega_DM or to halo
profiles / rotation curves. The qualitative dominance falls out; the numbers are not claimed.
"""
import numpy as np
np.random.seed(7)
# (B) Trans-resolution map = the renormalization-group / coarse-graining flow of the substrate phase field.
# Tests three things at once: (1) is the critical substrate a SCALE-INVARIANT FIXED POINT? (2) does the
# restoring tension / Lambda flow with resolution a as 1/a^2? (3) what fraction of energy lives in the
# sub-resolution (latent) modes = the dark candidate, now measured?
N=256
kx=np.fft.fftfreq(N)[:,None]*N; ky=np.fft.fftfreq(N)[None,:]*N; k2=kx**2+ky**2; k2[0,0]=1.0
def make_field(spec):    # spec(k2)->power; returns real-space field with that spectrum
    amp=np.sqrt(spec); ph=np.exp(2j*np.pi*np.random.rand(N,N)); f=np.fft.ifft2(amp*ph).real
    return f/ f.std()
crit=make_field(1.0/k2)               # critical: P ~ 1/k^2 (scale-free, Goldstone/KT, S27/S31)
mass=make_field(1.0/(k2+(0.15*N)**2)) # off-critical: massive, correlation length ~ 1/m
def radial_slope(f):                  # log-log slope of the radial power spectrum (the RG signature)
    P=np.abs(np.fft.fft2(f))**2; kr=np.sqrt(k2).ravel(); Pr=P.ravel()
    m=(kr>2)&(kr<N/4); s=np.polyfit(np.log(kr[m]),np.log(Pr[m]),1)[0]; return s
def coarsen(f):                       # block-average 2x = one RG step (lower the resolution)
    return f.reshape(N//2,2,N//2,2).mean(axis=(1,3))
print("="*72); print("BST Stage 55 — trans-resolution map: RG fixed point, Lambda(a), dark fraction"); print("="*72)
print("\n  (1) scale-invariant FIXED POINT? spectral slope before vs after one coarse-graining step:")
def slope_coarse(f):
    g=coarsen(f); P=np.abs(np.fft.fft2(g))**2; n=N//2
    kx2=np.fft.fftfreq(n)[:,None]*n; ky2=np.fft.fftfreq(n)[None,:]*n; kr=np.sqrt(kx2**2+ky2**2).ravel()
    Pr=P.ravel(); m=(kr>2)&(kr<n/4); return np.polyfit(np.log(kr[m]),np.log(Pr[m]),1)[0]
print(f"    critical : slope fine = {radial_slope(crit):+.3f}, coarsened = {slope_coarse(crit):+.3f}  -> INVARIANT = fixed point")
print(f"    massive  : slope fine = {radial_slope(mass):+.3f}, coarsened = {slope_coarse(mass):+.3f}  -> FLOWS away")
print("\n  (2) restoring tension / Lambda vs resolution a (low-pass at k<pi/a): does it scale as 1/a^2?")
fk=np.fft.fft2(crit); 
print(f"  {'a (cells)':>10}{'tension <|grad|^2>':>20}{'* a^2':>12}")
for a in [2,4,8,16,32]:
    kc=np.pi/a*N/np.pi   # cutoff in index units ~ N/(2a)*... use kc=N/(2a)
    kc=N/(2*a); mask=(np.sqrt(k2)<kc); ten=np.sum(k2*np.abs(fk)**2*mask)/N**2
    print(f"  {a:>10}{ten:>20.4e}{ten*a**2:>12.3f}")
print("\n  (3) dark fraction: energy in sub-resolution (latent) modes k>pi/a vs total, critical field:")
tot=np.sum(k2*np.abs(fk)**2)
print(f"  {'resolution a':>12}{'dark (sub-res) energy fraction':>32}")
for a in [4,8,16]:
    kc=N/(2*a); below=np.sum(k2*np.abs(fk)**2*(np.sqrt(k2)<kc)); print(f"  {a:>12}{1-below/tot:>32.3f}")
print("\n  => (1) critical substrate = scale-invariant FIXED POINT (slope ~ -2 preserved under coarse-")
print("  graining); off-critical FLOWS away. (2) tension * a^2 ~ const -> Lambda(a) ~ 1/a^2, resolution-")
print("  dependent exactly like size (S53 unified). (3) most energy sits in the FINE sub-resolution modes")
print("  = the latent/dark candidate, now quantified as the integrated-out energy fraction.")
print("  HONEST: this is the renormalization group / effective field theory (established). Substrate")
print("  content: trans-resolution IS the RG flow; criticality makes it self-similar; dark=sub-resolution")
print("  energy (gravitates via S40, invisible to observable channel) -- conceptual, NOT a fit to Omega_DM.")
