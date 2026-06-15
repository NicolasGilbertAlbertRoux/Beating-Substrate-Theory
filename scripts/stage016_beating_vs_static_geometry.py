#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 16 — DISTINCTIVENESS: does a BEATING core produce different ARCHITECTURE than a
STATIC soft core? (the content discriminator -- regular polyhedra are generic to attraction+
core; only a BEATING-vs-STATIC difference would be distinctive to the author's substrate.)

For each N: relax from random init with (a) STATIC repulsion (fixed R0) and (b) BEATING
repulsion (R(t)=R0(1+A sin omega t), fast beat so positions feel the time-averaged effect).
Compare the resulting ARCHITECTURE (scale-invariant): mean coordination number, NN-distance
regularity CV, and the normalized pairwise-distance pattern.

PRE-REGISTERED: if beating coordination/geometry == static for all N -> GENERIC (beating adds
nothing to architecture; its content is stability, not shape). If they DIFFER for some N ->
DISTINCTIVE (a real beating-specific architecture). Honest: 3D toy, functional, not nature.

RESULT + DECISIVE FOLLOW-UP: first glance showed beating coord/regularity DIFFERENT from
static for N=6,8,12 (beating more regular, higher coord; static CV high 0.42-1.10). BUT a
turn-off-the-beat test (relax the beating structure with a STATIC core) showed N=6,8 STAY
identical (coord 4.00->4.00, 4.75->4.75, CV unchanged; only a rescaling drift) => those
architectures ARE static equilibria, the beat merely HELPED REACH them. Static relaxation
from a good start disperses the cluster (coord 1.5-2.5) => the high static CV was a FAILED
RELAXATION, not the true static geometry. VERDICT: the apparent distinctiveness is largely a
RELAXATION ARTIFACT -- beating does not select distinctive architecture, it ANNEALS better.
N=12 inconclusive (collapses without beat, but static relaxation too unreliable to attribute).
Honest positive: beating acts as an integrated annealer (reaches order from random where static
freezes) -- a dynamical/functional capacity, consistent with the meta-pattern (beating content
is process, not static geometry), though any oscillation/noise also anneals (not unique).
"""
import numpy as np
def relax(N, beating, A=0.5, omega=10.0, G=1.0, k=3.0, R0=0.8, gamma_damp=0.6, T=1400, dt=0.008, seed=0, box=2.5):
    rng=np.random.default_rng(seed); X=rng.uniform(-box,box,(N,3)); V=np.zeros((N,3))
    for t in range(T):
        R=R0*(1+A*np.sin(omega*t*dt)) if beating else R0
        F=np.zeros((N,3))
        for i in range(N):
            r=X[i]-X; d=np.linalg.norm(r,axis=1); d[i]=1e9; u=r/d[:,None]
            F[i]=((k*np.maximum(0.0,2*R-d)-G/d**2)[:,None]*u).sum(0)
        V=(V+dt*F/1.0)*(1-gamma_damp*dt); X+=dt*V
    return X
def signature(X):
    D=np.linalg.norm(X[:,None]-X[None,:],axis=2); np.fill_diagonal(D,np.inf)
    nn=D.min(1); s=np.median(nn); cut=1.3*s
    return ((D<cut).sum(1)).mean(), nn.std()/max(nn.mean(),1e-9)
print("="*68); print("BST Stage 16 — beating vs static architecture (distinctiveness)"); print("="*68)
print(f"\n  {'N':>3} | {'STATIC coord':>13}{'CV':>7} | {'BEATING coord':>14}{'CV':>7} | {'different?':>12}")
for N in [4,6,8,12]:
    cs,cvs=[],[]; cb,cvb=[],[]
    for s in range(3):
        co,cv=signature(relax(N,False,seed=s)); cs.append(co); cvs.append(cv)
        co,cv=signature(relax(N,True,seed=s));  cb.append(co); cvb.append(cv)
    co_s,co_b=np.mean(cs),np.mean(cb)
    diff = "DIFFERENT" if abs(co_s-co_b)>0.4 else "same"
    print(f"  {N:>3} | {co_s:>13.2f}{np.mean(cvs):>7.2f} | {co_b:>14.2f}{np.mean(cvb):>7.2f} | {diff:>12}")
print("\nDistinctive iff beating coordination/geometry differs from static for some N.")
print("Otherwise the architecture is GENERIC; beating's content is stability (S14c), not shape.")
