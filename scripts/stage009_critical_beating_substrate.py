#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 9 — can a BEATING substrate be made SCALE-FREE (critical-like), and does it
then KEEP the cross-resolution reconstruction of Stage 7 at ALL scales (uniting S7+S8)?

single-scale substrate: nearest-neighbour coupling only (a natural scale -> saturates).
multi-scale substrate : coupling at octave offsets 1,2,4,8,16,32 (power-law weights) ->
                        structure injected at all scales (scale-free-ish).
Tests: (a) octave-variance spectrum (multi should be flatter than single);
       (b) cross-res reconstruction R2 as the COARSE view gets coarser (block b=2..32):
           does multi keep R2 high where single collapses past its natural scale?

PRE-REGISTERED (can fail): multi flatter spectrum AND retains R2 at large b; single
collapses at large b. If multi also collapses -> the union is not achieved this way.
HONEST FRAME: functional result about the MODEL substrate, not nature. Requires sklearn.
"""
import numpy as np
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score
rng=np.random.default_rng(0); N=256; dt=0.05
def simulate(offsets, weights, steps=500, K_r=1.5):
    θ=rng.uniform(0,2*np.pi,N); omega=rng.normal(1.0,0.3,N); O=[]
    for t in range(steps):
        coup=np.zeros(N)
        for d,w in zip(offsets,weights):
            coup=coup+w*(np.sin(np.roll(θ,d)-θ)+np.sin(np.roll(θ,-d)-θ))
        θ=θ+dt*(omega+K_r*coup); O.append(np.cos(θ).copy())
    return np.array(O[100:])
def octave(O):
    P=(np.abs(np.fft.rfft(O,axis=1))**2).mean(0); b=[]; j=1
    while 2**j<=N//2: b.append(P[2**(j-1):2**j].sum()); j+=1
    b=np.array(b); return b/b.sum()
def crossres(O,b,w=6,h=3):
    nc=N//b; C=O.reshape(O.shape[0],nc,b).mean(2); X=[];Y=[]
    for t in range(w-1,O.shape[0]-h): X.append(C[t-w+1:t+1].ravel()); Y.append(O[t+h])
    X=np.array(X);Y=np.array(Y); ntr=int(0.7*len(X))
    return r2_score(Y[ntr:],Ridge(1.0).fit(X[:ntr],Y[:ntr]).predict(X[ntr:]))
offs=[1,2,4,8,16,32]; wpl=[o**-0.5 for o in offs]
O_single=simulate([1],[1.0]); O_multi=simulate(offs,wpl)
print("="*70); print("BST Stage 9 — critical (multi-scale) beating substrate: S7 + S8"); print("="*70)
print("\nOctave variance (coarse->fine), flatter = more scale-free:")
for name,O in [("single-scale (nn only)",O_single),("multi-scale (octave coupling)",O_multi)]:
    ov=octave(O); print(f"  {name:30s}"+"".join(f"{v:6.3f}" for v in ov))
print("\nCross-res reconstruction R2 vs COARSE block size b (larger b = coarser view):")
print(f"  {'substrate':30s}"+"".join(f"b={b:<4}" for b in [2,4,8,16,32]))
for name,O in [("single-scale",O_single),("multi-scale (critical-like)",O_multi)]:
    print(f"  {name:30s}"+"".join(f"{crossres(O,b):6.2f}" for b in [2,4,8,16,32]))
print("\nUnion achieved iff multi-scale stays scale-free AND keeps R2 high at large b")
print("where single-scale collapses (its structure is gone below its natural scale).")
