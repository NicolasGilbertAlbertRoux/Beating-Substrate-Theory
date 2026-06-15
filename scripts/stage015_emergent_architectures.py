#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 15 — what ARCHITECTURES self-organize? (no polyhedra assumed; observe + detect.)
N beating spheres in 3D with the validated contact law (attraction -G/d^2 + soft repulsion
when mantles overlap). Relax from RANDOM initial positions; characterize what emerges, and
compare to a random-point NULL to see if regularity is SELECTED or generic.

Detectors (standard cluster-physics tools): nearest-neighbour distance regularity (CV =
std/mean; low = regular), mean coordination number, and the geometry vs known small clusters.
Run multiple seeds: do the SAME architectures recur (robust) or is it seed-dependent?

PRE-REGISTERED: relaxed clusters far MORE regular than the random null (CV much lower),
recurring across seeds => the dynamics SELECTS architecture. HONEST DISCRIMINATOR: these are
likely the GENERIC attraction+core (Lennard-Jones-like) geometries -- regular structure here
is EXPECTED and NOT distinctive to beating; distinctiveness would need beating-specific
geometry differing from a static soft-core control. 1D->3D, functional, not nature.

RESULT: small N (4,6) form PERFECT regular polyhedra (tetrahedron, octahedron), robust
across seeds, CV=0 vs null CV~0.35-0.52 -> dynamics SELECTS architecture. Large N (>=8):
UNRESOLVED -- damped relaxation got trapped in disorder; a simulated-annealing attempt
DISPERSED the cluster (mean coordination <2 = fragmented). Finding mid-N global minima is a
known-hard optimization problem (needs basin hopping / careful schedules); quick scripts are
inadequate, so large-N architecture is NOT determined here. CAVEAT: even the small-N polyhedra
are GENERIC (any attraction+core gives them) -- NOT distinctive to beating. Real content
question (untested): does the BEATING produce geometry differing from a STATIC soft-core?
"""
import numpy as np
def relax(N,G=1.0,k=3.0,R0=0.8,m=1.0,gamma_damp=0.6,T=900,dt=0.01,seed=0,box=2.5):
    rng=np.random.default_rng(seed); X=rng.uniform(-box,box,(N,3)); V=np.zeros((N,3))
    for t in range(T):
        F=np.zeros((N,3))
        for i in range(N):
            r=X[i]-X; d=np.linalg.norm(r,axis=1); d[i]=1e9; u=r/d[:,None]
            coef=(k*np.maximum(0.0,2*R0-d) - G/d**2)
            F[i]=(coef[:,None]*u).sum(0)
        V=(V+dt*F/m)*(1-gamma_damp*dt); X+=dt*V
    return X
def characterize(X):
    D=np.linalg.norm(X[:,None]-X[None,:],axis=2); np.fill_diagonal(D,np.inf)
    nn=D.min(1); cv=nn.std()/max(nn.mean(),1e-9)
    cut=1.3*np.median(nn); coord=((D<cut).sum(1)).mean()
    return cv,coord
KNOWN={4:"tetrahedron",6:"octahedron",8:"~square-antiprism",12:"~icosahedral",13:"icosahedron"}
print("="*70); print("BST Stage 15 — emergent architectures (observe + detect)"); print("="*70)
print(f"\n  {'N':>3}{'relaxed CV':>12}{'coord':>8}{'null CV':>10}{'recurs?':>20}")
for N in [4,6,8,12,13]:
    cvs=[]; coords=[]
    for s in range(4):
        cv,co=characterize(relax(N,seed=s)); cvs.append(cv); coords.append(co)
    rng=np.random.default_rng(99); ncv=np.mean([characterize(rng.uniform(-1.5,1.5,(N,3)))[0] for _ in range(4)])
    recur="yes" if np.std(cvs)<0.05 else "seed-dependent"
    print(f"  {N:>3}{np.mean(cvs):>12.3f}{np.mean(coords):>8.2f}{ncv:>10.3f}{recur:>20}  ~{KNOWN.get(N,'?')}")
print("\nDynamics SELECTS architecture iff relaxed CV << null CV and recurs across seeds.")
print("But regular clusters here are GENERIC (attraction+core); distinctiveness vs a static")
print("soft-core control is the real content question (next step).")
