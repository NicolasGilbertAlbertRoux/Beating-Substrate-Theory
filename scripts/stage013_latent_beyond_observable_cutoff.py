#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 13 — does latent resolution BEYOND the observable's cutoff carry real capacity?
(author's claim: the latent extends beyond observable limits -- a 'more complete latent
world'. Reframed falsifiably and WITHOUT violating c: not 'speed > c' but unbounded
RATE/RESOLUTION. The deep levels the observable cannot resolve still add genuine
reconstruction capacity if the latent is scale-free; they are wasted otherwise.)

Identity = K-level binary hierarchy (N=2^K). Level l resolves the l-th split. OBSERVABLE
accesses only levels 0..m_obs-1 (a resolution cutoff). LATENT accesses all K levels.
Exact-identity reconstruction accuracy using levels up to depth j.

  scale-free  : every level informative -> accuracy keeps rising past m_obs.
  single (null): levels >= m_obs constant/uninformative -> FLAT past m_obs (wasted).
  shuffled-MEM (anti-cheat): memory's DEEP levels keyed by a PERMUTED identity, so the
     query's true deep code no longer matches its own memory -> must COLLAPSE past m_obs.
NOTE: a first 'shuffled' control (permuting codebook rows) was MIS-DESIGNED -- a consistent
relabel stays informative, so it trivially passed. Fixed to shuffled-MEM, which collapses.

RESULT (reproduced): scale-free rises to ~0.91 past the cutoff; single stays ~0.11;
shuffled-MEM collapses to ~0.04. The invisible deep latent carries genuine capacity.
Honest: functional/possibility result conditional on the construction, not a claim about
nature -- but each control could fail and behaved correctly. Requires numpy.
"""
import numpy as np
rng=np.random.default_rng(0); K=6; N=2**K; d=4; m_obs=3
C=[rng.normal(size=(2**(l+1),d)) for l in range(K)]
def proto(idx,j): return np.concatenate([C[l][idx>>(K-1-l)] for l in range(j)])
def proto_single(idx,j):
    return np.concatenate([(C[l][idx>>(K-1-l)] if l<m_obs else C[l][0]*0) for l in range(j)])
def acc(j, mode, noise=0.7, reps=25):
    perm=rng.permutation(N)
    if mode=="scalefree": P=np.array([proto(i,j) for i in range(N)])
    elif mode=="single":  P=np.array([proto_single(i,j) for i in range(N)])
    elif mode=="shuf_mem":
        P=np.array([np.concatenate([C[l][(i if l<m_obs else perm[i])>>(K-1-l)] for l in range(j)]) for i in range(N)])
    ok=tot=0
    for i in range(N):
        for _ in range(reps):
            q=(proto_single(i,j) if mode=="single" else proto(i,j))+rng.normal(scale=noise,size=P.shape[1])
            ok+=(int(np.argmin(((P-q)**2).sum(1)))==i); tot+=1
    return ok/tot
print("="*66); print("BST Stage 13 — latent resolution beyond the observable cutoff"); print("="*66)
print(f"K={K} (N={N}); observable cutoff m_obs={m_obs} (deeper levels invisible to it)\n")
print(f"  {'depth j':>8}{'scale-free':>12}{'single(null)':>14}{'shuffled-MEM':>14}")
for j in range(1,K+1):
    tag=" <=cutoff" if j<=m_obs else " (beyond)"
    print(f"  {j:>8}{acc(j,'scalefree'):>12.3f}{acc(j,'single'):>14.3f}{acc(j,'shuf_mem'):>14.3f}{tag}")
print("\nDeep (observable-invisible) latent carries real capacity iff scale-free RISES past")
print("the cutoff while single stays flat AND shuffled-MEM collapses (genuine, not cheating).")
