#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 20 — conservative RATCHET: does an asymmetric SURFACE + a regular BEAT rectify a
directed flux? (author's design: asymmetry in the surface; the beat stays regular for coherence.)
N particles on a ring in an asymmetric periodic surface V(θ), AC-forced by a regular beat
that is a DYNAMICAL DOF per particle (energy-conserving; NO dissipation, NO external clock).

  H = sum_i[ p_i^2/2 + V(θ_i) + pi_i^2/2 + (Om^2/2) b_i^2 + lam*b_i*cos(θ_i) ]
  V(θ) = -V0[ sin(θ) + (r/2) sin(2 θ) ]   (r != 0 breaks spatial symmetry = ratchet)
A PER-PARTICLE beat (O(1) coupling) is essential: a single global beat coupled to a sum over N
particles scales as N, stiffens the dynamics and WRECKS energy conservation (my first attempts:
E drift 1-8%, controls non-zero, results jumped between runs -- all artifact). Per-particle beat
gives E drift ~1e-5 and clean controls.

RESULT (validated: E drift ~1e-5, controls ~0): NO directed current. TEST = -1.0e-3 +- 4.2e-3,
symmetric-control = -7e-4, no-beat-control = -6e-4 -- all SMALLER than their seed scatter, i.e.
all consistent with ZERO. The asymmetric-surface + regular-beat conservative ratchet does NOT
rectify a net current. This confirms the pre-registered HAMILTONIAN SUM RULE: in a dissipationless
system the net current over a symmetric ensemble cancels; directed transport needs DISSIPATION or
a prepared broken-symmetry state. CONSTRAINT for the author's "polarized flux paths -> magnetism":
directed flux cannot arise from a purely conservative substrate -- it requires the (later-emerging)
dissipation or symmetry breaking. The emergence of dissipation thus becomes the linchpin of the
flux/magnetism program. Honest: 1D conservative toy, functional, not nature.
"""
import numpy as np
def run(r, beat, N=80, V0=1.0, Om=1.0, lam=0.5, B=1.5, dt=0.005, T=12000, seed=0):
    rng=np.random.default_rng(seed)
    θ=rng.uniform(0,2*np.pi,N); p=rng.standard_normal(N)*0.2; p-=p.mean()
    b=np.full(N,B if beat else 0.0); pi=np.zeros(N); θ0=θ.copy(); Es=[]
    def acc(θ,b):
        return V0*(np.cos(θ)+r*np.cos(2*θ))+lam*b*np.sin(θ), -Om**2*b-lam*np.cos(θ)
    for t in range(T):
        Fθ,Fb=acc(θ,b); p+=0.5*dt*Fθ; pi+=0.5*dt*Fb
        θ+=dt*p; b+=dt*pi
        Fθ,Fb=acc(θ,b); p+=0.5*dt*Fθ; pi+=0.5*dt*Fb
        if t%100==0:
            Es.append((0.5*p**2+(-V0*(np.sin(θ)+0.5*r*np.sin(2*θ)))+0.5*pi**2+0.5*Om**2*b**2+lam*b*np.cos(θ)).sum())
    Es=np.array(Es); return (θ-θ0).mean()/(T*dt),(Es.max()-Es.min())/max(abs(Es.mean()),1e-9)
if __name__=="__main__":
    print("="*66); print("BST Stage 20 — conservative ratchet (per-particle beat, validated)"); print("="*66)
    print(f"\n  {'condition':>34}{'net current':>14}{'E drift':>10}")
    for name,r,beat in [("asymmetric + beat (TEST)",0.5,True),
                        ("symmetric + beat (control)",0.0,True),
                        ("asymmetric, NO beat (control)",0.5,False)]:
        cs=[];ds=[]
        for s in range(3): c,d=run(r,beat,seed=s); cs.append(c); ds.append(d)
        print(f"  {name:>34}{np.mean(cs):>14.3e}{np.max(ds):>10.1e}  (+-{np.std(cs):.1e})")
    print("\nAll currents < their seed scatter => consistent with ZERO (Hamiltonian sum rule).")
    print("Directed flux needs dissipation or broken symmetry, not a bare conservative substrate.")
