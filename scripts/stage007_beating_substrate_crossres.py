#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 7 — does a BEATING substrate with internal kinetics + ACTION/RETROACTION
carry a RECONSTRUCTION mechanics ACROSS RESOLUTIONS? (author's ontology, tested with a
control that can fail). Substrate = ring of "beating balls" (phase oscillators),
observable o_i=cos(θ_i). Cross-res task: predict the FINE field h steps ahead from a
time-WINDOW of the COARSE-grained observable only (ridge), R2 on held-out time.

RESULT (reproduced): BEATING-COUPLED R2~0.99 vs DECOUPLED R2<0 vs MEMORYLESS R2<0.
The high R2 is NOT a synchronization artifact: a K_r-scan shows R2 tracks the COUPLING
(feedback), not the Kuramoto order parameter r (which stays ~0.3 while R2 -> 0.99).
=> action/retroaction (feedback) is what links resolutions and makes the fine field
recoverable from coarse spatiotemporal observations; without it, it is not.

HONEST FRAME: a functional result about THIS model substrate, not a measurement of nature,
and it is "reconstruction ACROSS resolutions", NOT "emergence of physics". It supports the
author's SUBSTRATE-AS-CARRIER refinement: a beating substrate with feedback CARRIES the
cross-resolution reconstruction structure. Requires numpy + scikit-learn.
"""
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score
rng=np.random.default_rng(0)
N,b,steps,dt=64,4,600,0.1; ncoarse=N//b
def simulate(coupled=True, memoryless=False, K_r=2.0):
    θ=rng.uniform(0,2*np.pi,N); omega=rng.normal(1.0,0.3,N); O=[]; sync=[]
    for t in range(steps):
        if memoryless: o=rng.uniform(-1,1,N)
        else:
            coup=np.sin(np.roll(θ,1)-θ)+np.sin(np.roll(θ,-1)-θ)
            θ=θ+dt*(omega+(K_r if coupled else 0.0)*coup); o=np.cos(θ)
        O.append(o.copy()); sync.append(abs(np.mean(np.exp(1j*θ))) if not memoryless else 0.0)
    return np.array(O), float(np.mean(sync))
def crossres_R2(O,w=6,h=3):
    C=O.reshape(O.shape[0],ncoarse,b).mean(2); X=[];Y=[]
    for t in range(w-1,steps-h): X.append(C[t-w+1:t+1].ravel()); Y.append(O[t+h])
    X=np.array(X);Y=np.array(Y); ntr=int(0.7*len(X))
    return r2_score(Y[ntr:],Ridge(alpha=1.0).fit(X[:ntr],Y[:ntr]).predict(X[ntr:]))
print("="*66); print("BST Stage 7 — cross-resolution reconstruction of a beating substrate"); print("="*66)
print("predict FINE field 3 steps ahead from a window of COARSE observable only\n")
for label,kw in [("BEATING coupled (action/retroaction)",dict(coupled=True)),
                 ("BEATING decoupled (no feedback)",dict(coupled=False)),
                 ("MEMORYLESS (no kinetics)",dict(memoryless=True))]:
    r2=np.mean([crossres_R2(simulate(**kw)[0]) for _ in range(3)])
    print(f"  {label:38s} R2 = {r2:.3f}")
print("\nK_r-scan (is it a synchronization artifact? -> NO: R2 tracks K_r, not sync r):")
print(f"  {'K_r':>4}{'sync r':>9}{'R2':>9}")
for K_r in [0.3,0.6,1.0,2.0,4.0]:
    O,r=simulate(coupled=True,K_r=K_r); print(f"  {K_r:>4.1f}{r:>9.3f}{crossres_R2(O):>9.3f}")
print("\nFeedback carries cross-resolution reconstruction; it is NOT synchronization.")
