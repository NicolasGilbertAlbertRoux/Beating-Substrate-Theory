#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 22 — CAPSTONE: emergent dissipation + asymmetric topology -> directed flux?
Combines the two validated pieces: the conservative ratchet/beat (S20) + a per-particle LATENT
BATH (S21, which gives emergent dissipation for M>=~80). Fully Hamiltonian (total energy
conserved). Tests the author's reconstruction: a conservative substrate, coupled to a latent
bath (the "diffuse mantle") that dissipates by resolution separation, plus an ASYMMETRIC emergent
topology (the "comb" surface), should rectify a DIRECTED flux -- where the bare conservative
ratchet (S20) could not (Hamiltonian sum rule).

RESULT (M=110, real dissipation regime; energy drift ~5e-5): SUPPORTS the mechanism, with
caveats. TEST (asymmetric+beat+bath) = -3.8e-3 with TIGHT scatter (robustly nonzero); SYMMETRIC
control ~0 (-6e-4 +- 8e-4) => the current REQUIRES the asymmetry. The bath makes the current
DEFINITE (tight) vs the no-bath S20 case (noisy, sum-rule cancellation). CAVEATS: the
rectification here runs through the bath's STATE-DEPENDENT friction (a legitimate but specific
dissipative-ratchet mechanism); the beat ENHANCES (-3.8 vs -1.6e-3 without beat) but is not the
sole driver; small 1D toy, small currents; NO parameter sweep (deliberately, to avoid fishing) so
this is a PROOF OF PRINCIPLE, not a characterization. Loop closed in principle: conservative
substrate + latent bath (emergent dissipation) + asymmetric topology -> directed flux.
Honest: functional, not nature.
"""
import numpy as np
# Capstone: ratchet (asymmetric surface) + per-particle beat (AC drive) + per-particle latent bath
# (emergent dissipation). Fully Hamiltonian. Does directed current appear where the bare
# conservative ratchet (S20) gave ~0? Controls: no bath, symmetric surface.
def run(r, beat, bath, N=25, M=110, V0=1.0, Om=1.0, lam=0.6, B=1.5,
        wmax=8.0, gamma_damp=0.5, dt=0.005, T=6000, seed=0):
    rng=np.random.default_rng(seed)
    θ=rng.uniform(0,2*np.pi,N); p=rng.standard_normal(N)*0.2; p-=p.mean()
    b=np.full(N,B if beat else 0.0); pi=np.zeros(N)
    wk=np.linspace(wmax/M,wmax,M); dw=wmax/M
    ck=np.sqrt((2/np.pi)*gamma_damp*wk**2*dw); ct=np.sum(ck**2/wk**2)
    x=np.zeros((N,M)); px=np.zeros((N,M)); θ0=θ.copy(); Es=[]
    def acc(θ,b,x):
        s=np.sin(θ)
        sumcx=(ck[None,:]*x).sum(1) if bath else 0.0
        Fθ=V0*(np.cos(θ)+r*np.cos(2*θ))+lam*b*np.sin(θ)
        if bath: Fθ=Fθ+np.cos(θ)*(sumcx-ct*s)
        Fb=-Om**2*b-lam*np.cos(θ)
        Fx=(-wk[None,:]**2*x+ck[None,:]*s[:,None]) if bath else np.zeros_like(x)
        return Fθ,Fb,Fx
    for t in range(T):
        Fθ,Fb,Fx=acc(θ,b,x); p+=0.5*dt*Fθ; pi+=0.5*dt*Fb; px+=0.5*dt*Fx
        θ+=dt*p; b+=dt*pi; x+=dt*px
        Fθ,Fb,Fx=acc(θ,b,x); p+=0.5*dt*Fθ; pi+=0.5*dt*Fb; px+=0.5*dt*Fx
        if t%150==0:
            s=np.sin(θ)
            E=(0.5*p**2+(-V0*(np.sin(θ)+0.5*r*np.sin(2*θ)))+0.5*pi**2+0.5*Om**2*b**2+lam*b*np.cos(θ)).sum()
            if bath: E+=(0.5*px**2+0.5*wk[None,:]**2*(x-(ck/wk**2)[None,:]*s[:,None])**2).sum()
            Es.append(E)
    Es=np.array(Es); return (θ-θ0).mean()/(T*dt),(Es.max()-Es.min())/max(abs(Es.mean()),1e-9)
print("CAPSTONE: ratchet + beat + latent bath (emergent dissipation). N=25,M=110 (real dissipation regime)")
print(f"  {'condition':>40}{'net current':>13}{'E drift':>10}")
for name,r,beat,bath in [("asymmetric + beat + BATH (TEST)",0.5,True,True),
                         ("symmetric + beat + bath (control)",0.0,True,True),
                         ("asymmetric + beat, NO bath (=S20)",0.5,True,False),
                         ("asymmetric, NO beat + bath (control)",0.5,False,True)]:
    cs=[];ds=[]
    for s in range(2):
        c,d=run(r,beat,bath,seed=s); cs.append(c); ds.append(d)
    print(f"  {name:>40}{np.mean(cs):>13.3e}{np.max(ds):>10.1e}  (+-{np.std(cs):.1e})")
print("\nVALID iff E drift small & controls~0. Content iff TEST clearly nonzero & >> controls.")
