#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 18 — does the BEAT open flux/wave PATHS that a COOLED STATIC medium excludes?
(the author's "wave/flux paths" claim; the dynamical frame where content has lived.)
A dissipative 1D chain. Drive one end; measure the signal reaching the FAR end.
- STATIC (cooled, dead): fixed coupling + dissipation -> the wave damps and DIES before crossing.
- BEATING (coherent): coupling stiffness beats k(t)=k0(1+A sin omega t) (mantles beat) -> can
  PUMP the mode (parametric gain) and keep the channel OPEN against dissipation.
- RANDOM-PHASE control: each bond beats with a random phase -> incoherent, no coherent pumping.
PRE-REGISTERED: coherent BEATING delivers MORE signal to the far end than the dead static
(opens a flux path), while RANDOM-PHASE does NOT (so it's the COHERENT kinetics, not mere
modulation). If beating ~ static at all omega -> claim NOT supported. omega scan reported in
full (parametric effects are resonant; no cherry-picking). Honest: 1D toy, functional, not nature.

RESULT: INVALID as designed. Modelling the beat as an EXTERNAL stiffness modulation injects
unbounded energy -> parametric RESONANCE INSTABILITY (far-end "signal" 1e5..1e27 = the sim
diverging, NOT transmission). This repeats the S14b error (a non-energy-conserving beat).
So this does NOT support the flux-path claim. HONEST PHYSICS TENSION: keeping a flux channel
open against a dissipative ("cooled") static REQUIRES energy input; an energy-conserving
internal beat can feed transport only TRANSIENTLY from a finite reserve. A cooled static SOLID
still carries phonons (it does not "exclude" wave paths) -- it lets them DIE under dissipation.
The real, limited core: a beating substrate is never at rest so has PERSISTENT flux a quiescent
static lacks, but this draws on stored energy (not free/perpetual). NEXT: redesign with an
INTERNAL energy-conserving beat coupled to the transport mode; measure a directed PERSISTENT
current vs uniform/incoherent controls (a control that can fail), no energy injection.
"""
import numpy as np
def far_signal(mode, N=12, k0=1.0, gamma_damp=0.12, A=0.6, omega=1.0, drive=0.5, dfreq=0.5,
               T=4000, dt=0.02, seed=0):
    rng=np.random.default_rng(seed); x=np.zeros(N); v=np.zeros(N)
    phi = rng.uniform(0,2*np.pi,N) if mode=="random" else np.zeros(N)
    rec=[]
    for t in range(T):
        tt=t*dt
        if mode=="static": k=np.full(N,k0)
        elif mode=="beating": k=k0*(1+A*np.sin(omega*tt))*np.ones(N)
        else: k=k0*(1+A*np.sin(omega*tt+phi))
        F=np.zeros(N)
        F[1:]+= k[1:]*(x[:-1]-x[1:]); F[:-1]+= k[:-1]*(x[1:]-x[:-1])
        F-=gamma_damp*v; F[0]+=drive*np.sin(dfreq*tt)
        v+=dt*F; x+=dt*v
        if t>T*0.6: rec.append(x[-1])
    return np.sqrt(np.mean(np.array(rec)**2))
print("="*70); print("BST Stage 18 — flux/wave paths: beating vs cooled static (far-end signal)")
print("="*70)
st=np.mean([far_signal("static",seed=s) for s in range(3)])
print(f"\nSTATIC (dead) far-end RMS: {st:.4e}   (the baseline the beat must beat)\n")
print(f"  {'omega':>7}{'BEATING far':>16}{'RANDOM-phase far':>18}{'beats static?':>16}")
for om in [0.4,0.7,1.0,1.3,1.6,2.0]:
    b=np.mean([far_signal("beating",omega=om,seed=s) for s in range(3)])
    r=np.mean([far_signal("random",omega=om,seed=s) for s in range(3)])
    flag="YES" if b>3*st and b>2*r else ("partial" if b>st else "no")
    print(f"  {om:>7.1f}{b:>16.4e}{r:>18.4e}{flag:>16}")
print("\nContent iff coherent beating opens the path (>> static) where random-phase does not.")
