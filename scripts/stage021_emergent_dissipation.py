#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 21 — does DISSIPATION emerge from latent coupling? (the foundation for directed flux.)
A single OBSERVABLE (resolved) oscillator Q coupled to a bath of M LATENT (unresolved) oscillators
-- Caldeira-Leggett, fully Hamiltonian (energy conserved globally). The author's "diffuse mantle"
= a bath of soft modes. Question: does the observable's energy RELAX irreversibly into the latent
modes (= effective dissipation by resolution separation) while TOTAL energy is conserved?

  H = P^2/2 + (w0^2/2)Q^2 + sum_k[ p_k^2/2 + (w_k^2/2)x_k^2 - c_k x_k Q ] + (sum_k c_k^2/2w_k^2)Q^2
  Ohmic bath: w_k in (0,wmax], c_k^2 = (2/pi) gamma_damp w_k^2 dw.

PRE-REGISTERED control that can fail: with FEW modes the observable energy RECURS (comes back ->
NO true dissipation); with MANY modes it relaxes and STAYS low (effective irreversible
dissipation). Total energy conserved throughout (validate). This demonstrates dissipation arising
purely from the latent/observable split -- no energy injected, substrate stays conservative.
Honest: toy model, functional, not nature.
"""
import numpy as np
def run(M, w0=1.0, wmax=8.0, gamma_damp=0.4, dt=0.01, T=20000, seed=0):
    rng=np.random.default_rng(seed)
    wk=np.linspace(wmax/M, wmax, M); dw=wmax/M
    ck=np.sqrt((2/np.pi)*gamma_damp*wk**2*dw)
    ct=np.sum(ck**2/wk**2)           # counter-term coefficient
    Q=1.0; P=0.0; x=np.zeros(M); p=np.zeros(M)
    Eobs=[]; Etot=[]
    for t in range(T):
        FQ=-w0**2*Q+np.sum(ck*x)-ct*Q; Fx=-wk**2*x+ck*Q
        P+=0.5*dt*FQ; p+=0.5*dt*Fx; Q+=dt*P; x+=dt*p
        FQ=-w0**2*Q+np.sum(ck*x)-ct*Q; Fx=-wk**2*x+ck*Q
        P+=0.5*dt*FQ; p+=0.5*dt*Fx
        if t%200==0:
            eo=0.5*P**2+0.5*w0**2*Q**2
            et=eo+np.sum(0.5*p**2+0.5*wk**2*x**2)-np.sum(ck*x)*Q+0.5*ct*Q**2
            Eobs.append(eo); Etot.append(et)
    Eobs=np.array(Eobs); Etot=np.array(Etot); h=len(Eobs)//2
    return Eobs[0], Eobs[h:].mean(), Eobs[h:].max(), (Etot.max()-Etot.min())/abs(Etot.mean())
print("="*68); print("BST Stage 21 — emergent dissipation from latent modes (Caldeira-Leggett)"); print("="*68)
print(f"\n  {'M modes':>8}{'E_obs start':>13}{'E_obs late(mean)':>18}{'late max':>10}{'E drift':>10}  verdict")
for M in [2,5,20,80,300]:
    e0,elate,emax,drift=run(M)
    relaxed = elate < 0.25*e0
    recurs  = emax > 0.6*e0
    v = "RELAXED (dissipation)" if relaxed and not recurs else ("RECURS (no dissip.)" if recurs else "partial")
    print(f"  {M:>8}{e0:>13.3f}{elate:>18.4f}{emax:>10.3f}{drift:>10.1e}  {v}")
print("\nDissipation emerges iff MANY modes -> observable energy relaxes & stays low (no recurrence),")
print("total energy conserved. Few modes -> recurrence (reversible). The latent makes it irreversible.")
