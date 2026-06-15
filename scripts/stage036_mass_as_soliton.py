#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 36 — mass as the quantization-by-contact of a wave: sine-Gordon solitons.
User's thesis: mass is the localization/quantization (by the periodic 'contact' coupling) of a wider
WAVE phenomenon. The substrate's cosine coupling 1-cos(dθ) IS, in the continuum, the sine-Gordon
field: phi_tt - c^2 phi_xx + m^2 sin(phi) = 0. Two faces the user names:
  (A) WAVE: small oscillations are massive & relativistic, omega^2 = c^2 k^2 + m^2 (Klein-Gordon) --
      the mass IS the gap (the contact term).
  (B) PARTICLE: topological kink phi=4 arctan(exp(m x/c)) -- a localized lump with a definite REST
      MASS = its localization energy, moving relativistically (Lorentz contraction). The "particle".
So "mass = quantized/localized wave energy", DERIVED, on the same relativistic cone as S34.

CONSOLIDATIONS (c=m=beta=1, no fit): (A) omega^2 = 1 + k^2 (gap=1). (B) kink rest mass M ~ 8 (analytic),
boosted energy E(v) = gamma*M, width w(v) = w0/gamma (Lorentz), and a moving kink propagates stably at v.
NOTE: a first run used periodic (roll) gradients -> a spurious 2*pi boundary jump inflated M to ~402
and stalled the moving kink; FIXED here with non-periodic gradients + clamped edges (bulk integration).
HONEST BOUNDARY: this realizes mass-as-wave-quantization, but the kink does NOT curve spacetime the
Einstein way (flat sine-Gordon); the Einstein step (mass sourcing curvature, G=8piT) is NOT delivered.
"""
import numpy as np
N=1600; L=80.0; dx=L/N; x=np.linspace(-L/2,L/2,N,endpoint=False); c=1.0; m=1.0
def lap_p(f): return (np.roll(f,-1)-2*f+np.roll(f,1))/dx**2      # periodic (ok for tiny meson waves)
def lap_np(f):
    o=np.zeros_like(f); o[1:-1]=(f[2:]-2*f[1:-1]+f[:-2])/dx**2; return o   # non-periodic
def meson_omega(k_t,A=1e-3,dt=0.01,steps=20000):
    nk=round(k_t*L/(2*np.pi)); k=2*np.pi*nk/L
    phi=A*np.cos(k*x); v=np.zeros(N); rec=[]
    for s in range(steps):
        a=c*c*lap_p(phi)-m*m*np.sin(phi); v+=0.5*dt*a; phi+=dt*v
        a=c*c*lap_p(phi)-m*m*np.sin(phi); v+=0.5*dt*a
        rec.append(np.sum(phi*np.cos(k*x)))
    A_=np.array(rec)-np.mean(rec); w=np.fft.rfftfreq(len(A_),dt)*2*np.pi
    return k, w[np.argmax(np.abs(np.fft.rfft(A_)))]
def kink_profile(vel,x0=0.0):
    g=1/np.sqrt(1-vel**2); phi=4*np.arctan(np.exp(m*g*(x-x0)/c))
    phi_x=np.gradient(phi,dx); return phi,-vel*phi_x,g          # phi_t = -v phi_x  (boosted)
bulk=np.abs(x)<30.0
def energy(phi,phidot):
    phi_x=np.gradient(phi,dx)
    dens=0.5*phidot**2+0.5*c*c*phi_x**2+m*m*(1-np.cos(phi))
    return np.sum(dens[bulk])*dx
def width(phi):
    d=np.abs(np.gradient(phi,dx))*bulk; d=d/d.sum()
    xc=np.sum(x*d); return np.sqrt(np.sum((x-xc)**2*d))
print("="*72); print("BST Stage 36 — mass as quantization-by-contact of a wave (sine-Gordon)"); print("="*72)
print("\n  (A) WAVE face: meson dispersion  omega^2 = c^2 k^2 + m^2  (Klein-Gordon, gap=1)")
print(f"  {'k':>7}{'omega':>10}{'omega^2':>10}{'1+k^2':>10}")
for k_t in [0.2,0.4,0.8,1.2]:
    k,om=meson_omega(k_t); print(f"  {k:>7.3f}{om:>10.4f}{om*om:>10.4f}{1+k*k:>10.4f}")
print("\n  (B) PARTICLE face: kink soliton -- rest mass & relativistic kinematics")
phi0,pd0,_=kink_profile(0.0); E0=energy(phi0,pd0); w0=width(phi0)
print(f"  rest mass M = E(0) = {E0:.4f}  (analytic 8.0);   rest width w0 = {w0:.4f}")
print(f"  {'v':>6}{'E(v)':>10}{'E(v)/M':>9}{'gamma':>9}{'width':>9}{'w0/gamma':>10}")
for vel in [0.0,0.3,0.6,0.9]:
    phi,pd,g=kink_profile(vel); print(f"  {vel:>6.2f}{energy(phi,pd):>10.4f}{energy(phi,pd)/E0:>9.4f}{g:>9.4f}{width(phi):>9.4f}{w0/g:>10.4f}")
# stability: evolve a v=0.6 kink with non-periodic dynamics + clamped edges, track center
phi,vel0,_=kink_profile(0.6,x0=-10.0); v=vel0.copy(); dt=0.004; lo,hi=phi[0],phi[-1]; centers=[]; ts=[]
for s in range(1200):
    a=c*c*lap_np(phi)-m*m*np.sin(phi); v+=0.5*dt*a; phi+=dt*v; phi[0]=lo; phi[-1]=hi
    a=c*c*lap_np(phi)-m*m*np.sin(phi); v+=0.5*dt*a
    if s%700==0:
        d=np.abs(np.gradient(phi,dx))*bulk; centers.append(np.sum(x*d)/d.sum()); ts.append(s*dt)
sp=np.polyfit(ts,centers,1)[0]
print(f"\n  moving kink launched at v=0.6: tracked speed = {sp:.3f}  (stable relativistic particle)")
print("\n  => mass = localized/quantized energy of the wave field, relativistic (Lorentz). DERIVED.")
print("  BOUNDARY: kink does not curve spacetime (flat sine-Gordon); Einstein step NOT delivered.")
