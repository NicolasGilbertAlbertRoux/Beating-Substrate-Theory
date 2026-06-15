#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 19 — POLARIZED flux from a TRAVELLING beat (conservative; fixes the S18 error).
The beat is a DYNAMICAL degree of freedom (own coordinate b_i, momentum pi_i, freq Omega),
NOT a prescribed k(t) -- so the Hamiltonian is time-independent and energy is CONSERVED (no
external clock, no parametric blow-up). The beat amplitude modulates the transport-chain
coupling; energy flows reversibly between beat and transport (action/retroaction).

Seed the transport chain x with small zero-net-momentum random velocities (no initial net
current). Excite the beat field three ways and ask: does a SPATIALLY-POLARIZED (travelling)
beat rectify a NET DIRECTED energy current in the transport chain, where a static or standing
beat does not?
  - static   : beat at rest (B=0)              -> control, expect net current ~ 0
  - standing : beat excited, zero momentum      -> control (energy but no direction), ~ 0
  - travelling: beat is a travelling wave        -> "polarized"; pre-registered NET current != 0
VALIDATION FIRST: energy drift must be tiny and the static control must give ~0 current, else
the result is not trusted. Honest: 1D conservative toy, functional, not nature.

RESULT: design VALIDATED (energy drift ~1e-5, static control current ~0). But NEGATIVE: the
travelling ("polarized") beat gives net current ~ -5e-4, NOT distinct from the static/standing
controls (all ~1e-4, noise band, inconsistent signs). So a polarized beat does NOT rectify a
directed flux HERE. EXPECTED PHYSICS: a LINEAR conservative chain cannot rectify a DC current --
directed flux needs NON-LINEARITY + broken symmetry (a ratchet/pump); linear response averages
to zero. Constraint for the author's "polarized flux paths -> magnetism": directed flux cannot
arise from a linear substrate. NEXT (principled, not tuning): same validated conservative rig
with the REAL non-linear contact law + an asymmetry, and test whether a travelling beat rectifies
a net current vs static/standing controls.
"""
import numpy as np
def run(mode, N=16, k0=1.0, alpha=0.3, Omega=1.2, B=0.8, m=2, dt=0.01, T=1200, seed=0, xkick=0.3):
    rng=np.random.default_rng(seed)
    x=np.zeros(N); p=rng.standard_normal(N)*xkick; p-=p.mean()
    i=np.arange(N); ph=2*np.pi*m*i/N
    if mode=="static":    b=np.zeros(N); pi=np.zeros(N)
    elif mode=="standing":b=B*np.cos(ph); pi=np.zeros(N)
    else:                 b=B*np.cos(ph); pi=B*Omega*np.sin(ph)   # travelling wave
    dk=alpha*0.5*k0
    def kbond(b): return k0*(1+alpha*0.5*(b+np.roll(b,-1)))
    def forces(x,b):
        kb=kbond(b); strain=x-np.roll(x,-1)
        Fx=-(kb*strain)+(np.roll(kb,1)*np.roll(strain,1))
        Fb=-Omega**2*b-0.5*dk*(strain**2+np.roll(strain,1)**2)
        return Fx,Fb,kb,strain
    Js=[]; Es=[]
    for t in range(T):
        Fx,Fb,_,_=forces(x,b); p+=0.5*dt*Fx; pi+=0.5*dt*Fb
        x+=dt*p; b+=dt*pi
        Fx,Fb,kb,strain=forces(x,b); p+=0.5*dt*Fx; pi+=0.5*dt*Fb
        if t%20==0:
            vavg=0.5*(p+np.roll(p,-1)); J=-(kb*strain*vavg).mean()
            E=(0.5*p**2).sum()+(0.5*pi**2).sum()+(0.5*Omega**2*b**2).sum()+(0.5*kb*strain**2).sum()
            Js.append(J); Es.append(E)
    Js=np.array(Js); Es=np.array(Es)
    return Js[len(Js)//2:].mean(), (Es.max()-Es.min())/abs(np.mean(Es))
print("="*68); print("BST Stage 19 — polarized flux from a travelling beat (conservative)"); print("="*68)
print(f"\n  {'mode':>12}{'net current':>16}{'energy drift':>15}")
for mode in ["static","standing","travelling"]:
    Js=[]; drifts=[]
    for s in range(4):
        J,dr=run(mode,seed=s); Js.append(J); drifts.append(dr)
    print(f"  {mode:>12}{np.mean(Js):>16.3e}{np.max(drifts):>15.2e}")
print("\nVALID only if energy drift tiny AND static~0. Content iff travelling >> static,standing.")
