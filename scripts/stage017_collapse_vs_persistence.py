#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 17 — does the BEAT prevent COLLAPSE? (revisits S16's too-quick "generic" verdict)
The static contact potential U = -G/d + (k/2)max(0,2R0-d)^2 has a finite soft repulsion but a
-G/d attraction that diverges at d->0: its GLOBAL minimum is COLLAPSE to a point. A static
extended cluster is only METASTABLE. Claim (author's "movement vs death"): the BEAT robustly
stabilizes extended structure where the static collapses under perturbation.

Take an octahedron (N=6) at the equilibrium spacing; evolve with small dissipation + noise
(perturbations probing metastability); track the MINIMUM pairwise distance over time.
PRE-REGISTERED: static cluster COLLAPSES under noise (some pair distance -> ~0) while the
BEATING cluster stays EXTENDED (min distance stays near equilibrium). Control that could fail:
the beating might also collapse, or the static might NOT (deep enough metastable well).
Honest: 3D toy, functional, not nature.

RESULT: hypothesis NOT supported. At moderate noise (0.05) NEITHER collapses (0/5 both); at
strong noise (0.12) BOTH disperse to a gas (not collapse). The octahedron's geometric rigidity
holds the static cluster -- each pair is kept apart by the others, so the isolated-pair collapse
(S14c) does NOT extend to the cluster. Only a faint directional hint (static creeps inward,
beating drifts outward). VERDICT: the beat is NOT shown to prevent collapse at the cluster level;
claim withdrawn. (The PAIR-level S14c result stands; the cluster adds rigidity the pair lacks.)
NOTE on S16: the framing was the real flaw -- the beat is independently motivated (Axiom III,
kinetics for action/retroaction), so static is the DEGENERATE case, not the bar to beat. "Beat
provides needed kinetics + does not break structure + anneals order from random" is a fair
POSITIVE reading; the invented "beat static at geometry" bar was not the relevant one.
"""
import numpy as np
OCT=np.array([[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]],float)
def evolve(beating, A=0.5, omega=10.0, G=1.0, k=3.0, R0=0.8, gamma_damp=0.02,
           T=3000, dt=0.006, seed=0, noise=0.05):
    rng=np.random.default_rng(seed); X=OCT.copy(); n=len(X); V=np.zeros((n,3)); mind=[]
    for t in range(T):
        R=R0*(1+A*np.sin(omega*t*dt)) if beating else R0
        F=np.zeros((n,3))
        for i in range(n):
            r=X[i]-X; d=np.linalg.norm(r,axis=1); d[i]=1e9; u=r/d[:,None]
            F[i]=((k*np.maximum(0.0,2*R-d)-G/d**2)[:,None]*u).sum(0)
        V=(V+dt*F)*(1-gamma_damp*dt)+noise*np.sqrt(dt)*rng.standard_normal((n,3)); X+=dt*V
        if t%300==0:
            D=np.linalg.norm(X[:,None]-X[None,:],axis=2); np.fill_diagonal(D,1e9); mind.append(D.min())
    return np.array(mind)
print("="*66); print("BST Stage 17 — does the beat prevent collapse? (octahedron, N=6)"); print("="*66)
print(f"\nEquilibrium NN spacing ~ {np.sqrt(2):.3f}. Collapse = min distance -> ~0.\n")
print(f"  {'condition':>12}{'min-dist start':>16}{'min-dist end':>14}{'collapsed?':>14}")
for label,beat in [("STATIC",False),("BEATING",True)]:
    ends=[]; coll=0
    for s in range(5):
        m=evolve(beat,seed=s); ends.append(m[-1])
        if m[-1]<0.4: coll+=1
    print(f"  {label:>12}{np.mean([evolve(beat,seed=s)[0] for s in range(2)]):>16.3f}{np.mean(ends):>14.3f}{f'{coll}/5':>14}")
print("\nIf static collapses (min->0) and beating stays extended: the beat does MORE than")
print("anneal -- it STABILIZES extended structure against collapse (matches S14c). That would")
print("REVISE S16's 'just an annealer' verdict upward.")
