#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 30 — does a calibration at ONE resolution reach DOWN the resolution chain? (the author's
question.) A hierarchy of resolutions z_0 (coarsest = observable) ... z_{L-1} (deepest latent),
coupled scale-to-scale by the substrate with strength c (each finer scale = c*g(coarser) +
independent fine detail). We calibrate/train a predictor using ONLY the observable z_0 and ask how
well it predicts each deeper latent scale, out-of-sample (R^2 vs depth).

PRE-REGISTERED: coupled (c>0) -> the observable predicts the near latent well, R^2 DECAYING with
depth (calibration reaches a finite depth set by c); decoupled (c=0) -> R^2~0 at every depth (a
calibrated observable says nothing about the latent). The decay tells us HOW FAR one resolution's
calibration propagates -- and whether the deep latent is forever beyond observable calibration
(consistent with S8 saturation / S13 "infinitely latent"). Honest: a generic cascade model; it
measures the STRUCTURE of cross-resolution calibration transfer, a real and answerable question,
not a derivation of physics.
"""
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
def gen(N, L, c, seed=0):
    rng=np.random.default_rng(seed); Z=[rng.standard_normal(N)]
    for i in range(1,L):
        g=np.tanh(1.3*Z[-1])                       # fixed nonlinear scale-to-scale map
        raw=c*g+np.sqrt(max(1-c*c,0.0))*rng.standard_normal(N)
        raw=(raw-raw.mean())/(raw.std()+1e-9); Z.append(raw)
    return np.array(Z)                             # (L,N)
def reach(c, N=6000, L=7, seed=0):
    Z=gen(N,L,c,seed); tr=slice(0,N//2); te=slice(N//2,N)
    X0tr=Z[0,tr].reshape(-1,1); X0te=Z[0,te].reshape(-1,1); r2=[]
    for i in range(1,L):
        m=RandomForestRegressor(n_estimators=120,max_depth=8,random_state=0,n_jobs=2)
        m.fit(X0tr,Z[i,tr]); r2.append(r2_score(Z[i,te],m.predict(X0te)))
    return r2
print("="*70); print("BST Stage 30 — how far down the resolution chain does one calibration reach?"); print("="*70)
print(f"\n  R^2 of predicting each latent depth from the OBSERVABLE (z_0), out-of-sample:")
print(f"  {'coupling c':>12} | " + "".join(f"depth {d}".rjust(10) for d in range(1,7)))
for c in [0.95,0.7,0.4,0.0]:
    r2=reach(c)
    print(f"  {c:>12.2f} | " + "".join(f"{v:>10.3f}" for v in r2))
print("\nCoupled: R^2 decays with depth -> calibration reaches a FINITE depth (set by c).")
print("Decoupled (c=0): R^2~0 everywhere -> observable calibration says NOTHING about the latent.")
print("The depth where R^2 falls low = how far the observable image constrains the latent chain.")
