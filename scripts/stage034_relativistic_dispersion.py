#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 34 — relativity bridge, first test: does the conservative beat give a LIGHT CONE?
A wave equation is Lorentz-invariant; its excitations have a LINEAR dispersion omega = c*k (a
light/sound cone) with an emergent speed limit c. We measure the excitation dispersion of the
phase substrate under (i) CONSERVATIVE beat dynamics (Hamiltonian: θ-dot=p, p-dot=lattice
sine-force) and (ii) RELAXATIONAL dynamics (overdamped: θ-dot = force). 

PRE-REGISTERED: conservative -> omega(k) linear at small k (omega= c k, RELATIVISTIC light cone),
analytic omega=2|sin(k/2)|, so omega/k -> c=1; relaxational -> decay rate Gamma(k) ~ k^2 (DIFFUSIVE,
non-relativistic). The conservative beat is what gives the substrate its relativistic kinematics --
the prerequisite for the analog-gravity (acoustic-metric) bridge to gravity. Honest: standard
relativistic-phonon / analog-relativity physics, inherited because the conservative wave dynamics
IS Lorentz-invariant at long wavelength; the value is the coherent bridge under the geometry
framing, and it sets up the flow-tilts-the-cone (gravity) step. 1D.
"""
import numpy as np
def conservative(k, N=256, A=0.03, dt=0.05, steps=5000):
    x=np.arange(N); θ=A*np.cos(k*x); p=np.zeros(N); amp=[]
    for t in range(steps):
        F=np.sin(np.roll(θ,-1)-θ)+np.sin(np.roll(θ,1)-θ)
        p=p+0.5*dt*F; θ=θ+dt*p
        F=np.sin(np.roll(θ,-1)-θ)+np.sin(np.roll(θ,1)-θ)
        p=p+0.5*dt*F
        amp.append(np.sum(θ*np.cos(k*x)))
    a=np.array(amp); a=a-a.mean(); f=np.fft.rfftfreq(len(a),dt); P=np.abs(np.fft.rfft(a))
    return 2*np.pi*f[np.argmax(P)]
def relaxational(k, N=256, A=0.03, dt=0.02, steps=3000):
    x=np.arange(N); θ=A*np.cos(k*x); amp=[]
    for t in range(steps):
        F=np.sin(np.roll(θ,-1)-θ)+np.sin(np.roll(θ,1)-θ); θ=θ+dt*F
        amp.append(np.sum(θ*np.cos(k*x)))
    a=np.abs(np.array(amp)); a=a/a[0]; t=np.arange(len(a))*dt
    good=a>0.05
    return -np.polyfit(t[good],np.log(a[good]),1)[0]   # decay rate Gamma
print("="*70); print("BST Stage 34 — does the conservative beat give a relativistic light cone?"); print("="*70)
print(f"\n  {'k':>7}{'omega (conserv.)':>18}{'omega/k = speed':>16}{'Gamma (relax.)':>16}{'Gamma/k^2':>11}")
N=256
for m in [2,4,8,16,32,48]:
    k=2*np.pi*m/N
    om=conservative(k,N=N); g=relaxational(k,N=N)
    print(f"  {k:>7.3f}{om:>18.4f}{om/k:>16.4f}{g:>16.5f}{g/k**2:>11.4f}")
print("\n  Conservative: omega/k ~ constant = c (LINEAR dispersion = light cone = RELATIVISTIC).")
print("  Relaxational: Gamma/k^2 ~ constant (DIFFUSIVE = non-relativistic).")
print("  => the conservative beat is the origin of the substrate's relativistic kinematics.")
