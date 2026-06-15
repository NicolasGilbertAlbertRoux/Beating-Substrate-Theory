#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 37 — the contact/wave coordinate SHIFT is the de Broglie matter wave.
User's hint: the coordinate of the CONTACT (the localized lump / where energy localizes / where it
'clicks') need not coincide with the coordinate of the WAVE that provokes it. In a massive field (the
meson/Klein-Gordon sector of the sine-Gordon substrate, S36), a 'particle at rest' is a clock
oscillating at omega0 = m. BOOST it to velocity v (Lorentz): the CONTACT (energy packet) moves at the
GROUP velocity v, while the WAVE (phase) moves at the PHASE velocity c^2/v -- they slide past each
other, and the spatial period of that SHIFT is the de Broglie wavelength lambda = h/p. This is de
Broglie's 1924 'harmony of phases'. It DERIVES the cornerstone QM relation lambda=h/p from the
relativistic boost of a mass, ties S29(quantum)+S34(relativity)+S36(mass).

PRE-REGISTERED & CONSOLIDATIONS (c=m=hbar=1, no fit): KG dispersion omega=sqrt(m^2+k^2). For a boost
v, de Broglie k=gamma m v (=p), omega=gamma m: v_phase=omega/k=c^2/v, v_group=k/omega=v, so
v_phase*v_group=c^2, and omega^2-k^2=m^2 (mass shell, same m as S36). A packet shows the carrier (wave)
sliding FORWARD through the envelope (contact) -- the visible decalage. 1D linear KG.
"""
import numpy as np
m=1.0; c=1.0
def kg_omega(k_t,L=120.0,N=2400,A=1e-3,dt=0.01,steps=24000):
    dx=L/N; x=np.linspace(0,L,N,endpoint=False)
    nk=round(k_t*L/(2*np.pi)); k=2*np.pi*nk/L
    phi=A*np.cos(k*x); pt=np.zeros(N); rec=[]
    def lap(f): return (np.roll(f,-1)-2*f+np.roll(f,1))/dx**2
    for s in range(steps):
        a=c*c*lap(phi)-m*m*phi; pt+=0.5*dt*a; phi+=dt*pt
        a=c*c*lap(phi)-m*m*phi; pt+=0.5*dt*a
        rec.append(np.sum(phi*np.cos(k*x)))
    R=np.array(rec)-np.mean(rec); w=np.fft.rfftfreq(len(R),dt)*2*np.pi
    return k, w[np.argmax(np.abs(np.fft.rfft(R)))]
print("="*74); print("BST Stage 37 — contact/wave shift = de Broglie matter wave"); print("="*74)
print("\n  (1) KG dispersion of the substrate's meson sector: omega = sqrt(m^2 + k^2)")
print(f"  {'k':>7}{'omega_meas':>12}{'sqrt(1+k^2)':>13}")
disp={}
for k_t in [0.3,0.6,1.0,1.5]:
    k,om=kg_omega(k_t); disp[round(k,3)]=om; print(f"  {k:>7.3f}{om:>12.4f}{np.sqrt(1+k*k):>13.4f}")
print("\n  (2) Boost a rest-mass clock to v -> de Broglie. CONTACT moves at v_group, WAVE at v_phase.")
print(f"  {'v':>6}{'k=gamma*v':>11}{'omega_meas':>12}{'gamma':>9}{'v_phase':>9}{'v_group':>9}{'vph*vgr':>9}{'w^2-k^2':>9}")
for v in [0.3,0.5,0.7]:
    g=1/np.sqrt(1-v*v); k_t=g*v
    k,om=kg_omega(k_t)              # measured omega at the de Broglie wavevector
    vph=om/k; vgr=k/om              # v_group = domega/dk = k/omega for KG
    print(f"  {v:>6.2f}{k:>11.4f}{om:>12.4f}{g:>9.4f}{vph:>9.4f}{vgr:>9.4f}{vph*vgr:>9.4f}{om*om-k*k:>9.4f}")
print("\n  v_group = v (the CONTACT), v_phase = c^2/v (the WAVE) -> they differ: the decalage.")
print("  v_phase*v_group = c^2 = 1; omega^2-k^2 = m^2 = 1 (same mass as S36). lambda=2pi/k=h/p.")
