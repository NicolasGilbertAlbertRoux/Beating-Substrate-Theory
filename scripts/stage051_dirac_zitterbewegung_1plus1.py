#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 51 — Dirac (1+1D) from a c-mover + contact-reversal (the wave<->contact translation).
The fermion front past S49 (statistics) to the DIRAC DYNAMICS. Wave language: each spinor component is a
c-mover on the light cone. Contact language: a massive sub-luminal particle. The translation is the
zitterbewegung / Feynman checkerboard: a c-mover that zigzags, the MASS = the reversal (contact) rate
coupling the two movers. H(k) = k*sigma_z + m*sigma_x; the 2-spinor (psi_R,psi_L) = right/left movers =
chirality = emergent spin-1/2.
RESULT: eigenvalues = +/-sqrt(k^2+m^2) exact (gap 2m at k=0); packet group velocity = k0/sqrt(k0^2+m^2)
matched to <0.1% and < c for m>0 (=c for m=0). So 1+1D Dirac IS a c-mover (wave, S34 light cone) made
massive by contact reversals (S36 mass mechanism); spin-1/2 falls out of the which-way (R/L) degree.
HONEST RESERVE: 1+1D is the tractable Feynman-checkerboard case -- established, not novel. The full 3+1D
Dirac (4-component spinor, full Clifford/gamma algebra, the relation to rotations) is NOT done here.
"""
import numpy as np
# Dirac fermion in 1+1D from wave<->contact: a c-mover that zigzags (Feynman checkerboard / zitterbewegung).
# 2-spinor (psi_R, psi_L) = right/left movers (chirality). H(k) = k*sigma_z + m*sigma_x. The mass term
# (sigma_x) = the reversal/contact coupling between the two c-movers. Eigenvalues +/-sqrt(k^2+m^2) = the
# relativistic dispersion; group velocity v_g = k/sqrt(k^2+m^2) < c (contact) while each mover goes at c.
print("="*72); print("BST Stage 51 — Dirac (1+1D) from a c-mover + contact-reversal (wave<->contact)"); print("="*72)
def E(k,m): return np.sqrt(k**2+m**2)
# (1) dispersion from the 2x2 Dirac Hamiltonian eigenvalues
print("\n  (1) H(k)=k*sigma_z + m*sigma_x eigenvalues vs sqrt(k^2+m^2):")
m=0.8
for k in [0.0,0.5,1.0,2.0]:
    H=np.array([[k,m],[m,-k]]); ev=np.sort(np.linalg.eigvalsh(H))
    print(f"    k={k:4.1f}:  eig = {ev[0]:+.4f},{ev[1]:+.4f}   sqrt(k^2+m^2)={E(k,m):.4f}  (gap at k=0 = 2m={2*m})")
# (2) evolve a wave packet under 1+1D Dirac; measure group velocity vs k0/sqrt(k0^2+m^2)
N=2048; L=400.0; dx=L/N; x=np.linspace(-L/2,L/2,N,endpoint=False)
k=2*np.pi*np.fft.fftfreq(N,d=dx); k0=1.0; s=12.0
def group_velocity(m):
    env=np.exp(-(x)**2/(4*s**2))*np.exp(1j*k0*x)
    # positive-energy spinor at k0
    Ek=E(k0,m); cR=np.sqrt((1+k0/Ek)/2); cL=np.sqrt((1-k0/Ek)/2)
    psiR=cR*env.copy(); psiL=cL*env.copy()
    fR=np.fft.fft(psiR); fL=np.fft.fft(psiL); t=20.0
    Ekk=E(k,m); c=np.cos(Ekk*t); sn=np.sin(Ekk*t)/np.where(Ekk==0,1,Ekk)
    # exp(-iH t) = cos(E t) I - i sin(E t)/E * H, H=[[k,m],[m,-k]]
    gR=(c-1j*sn*k)*fR + (-1j*sn*m)*fL; gL=(-1j*sn*m)*fR + (c+1j*sn*k)*fL
    pR=np.fft.ifft(gR); pL=np.fft.ifft(gL); rho=np.abs(pR)**2+np.abs(pL)**2; rho/=rho.sum()
    x0=np.sum(x*np.abs(env)**2)/np.sum(np.abs(env)**2)
    return (np.sum(x*rho)-x0)/t
print("\n  (2) packet group velocity vs k0/sqrt(k0^2+m^2)  (k0=1.0):")
print(f"  {'m':>6}{'v_group(meas)':>16}{'k0/E (pred)':>14}{'< c ?':>8}")
for m in [0.0,0.5,1.0,2.0]:
    vg=group_velocity(m); pred=k0/E(k0,m); print(f"  {m:>6.1f}{vg:>16.4f}{pred:>14.4f}{'yes' if pred<1 else 'c':>8}")
print("\n  => m=0: massless, each mover at c (v_g=c). m>0: the contact-reversal couples R<->L, dispersion")
print("  becomes sqrt(k^2+m^2), v_group = k/E < c. The 2-spinor (R,L) = chirality = emergent spin-1/2.")
print("  Dirac (1+1D) IS a c-mover (wave) zigzagging by contact (mass = reversal rate). Same key as S36.")
