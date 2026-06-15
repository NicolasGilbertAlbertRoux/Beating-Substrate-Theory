#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 14 — the ATOMIC brick of the author's wave-contact ontology: do two beating
spheres form a STABLE bound oscillation, and does it require SYNCHRONIZATION?
(funnel: cheapest fail-fast test before any big topology scan.)

Model (author's mechanism, my explicit choices -- to be corrected):
 - each sphere has a beating radius R_i(t) = R0(1 + A sin(omega t + phase_i)).
 - REPULSION when mantles overlap (expansion-driven collision): F_rep = k_r*max(0, R1+R2 - d).
 - SUCTION/void during contraction (each wave falls back): F_suc = -k_s*max(0, -sin(omega t)).
 - separation d obeys m d'' = F_rep + F_suc.
Outcome classified as: BOUND (d stays in a bounded oscillating range), FLY-APART (d->inf),
or COLLAPSE (d->0).

PRE-REGISTERED (each can fail):
 - k_s=0 (no suction): FLY-APART (repulsion alone can't bind) -> suction is necessary.
 - some k_s window: BOUND (the cycle the author describes).
 - desynchronized (phase offset pi): binding DEGRADES/lost -> tests the synchronicity claim.
RESULT (honest, INCONCLUSIVE): with MY crude force choices, no synchronized bound state
forms (collapse or fly-apart); only ANTI-phase binds (opposite to the synchronicity claim).
BUT this is dominated by an arbitrary modeling choice -- the 'suction' was a constant,
DISTANCE-INDEPENDENT, phase-gated pull, which is unphysical for a void/suction. So this does
NOT refute the author's picture; it reveals that the picture's behavior hinges entirely on
the precise CONTACT FORCE LAW (suction/repulsion as a function of separation AND phase),
which is unspecified. NEXT (funnel): the author specifies the contact mechanics precisely
(quantitative ontology) -> implement THAT faithfully -> the brick test becomes decisive ->
only then scan N-wave polyhedra, with an out-of-sample control (does the dynamics SELECT
regular polyhedra from random init vs a null, not just reproduce what was put in?).
Honest: a 1D toy of a 3D picture; the load-bearing unknown is the contact force law.
"""
import numpy as np
def simulate(k_r=2.0,k_s=0.5,A=0.5,omega=1.5,R0=1.0,m=1.0,d0=2.2,T=6000,dt=0.02,phase2=0.0):
    d=d0; v=0.0; ds=[]
    for t in range(T):
        tm=t*dt
        R1=R0*(1+A*np.sin(omega*tm)); R2=R0*(1+A*np.sin(omega*tm+phase2))
        F_rep=k_r*max(0.0,(R1+R2)-d)
        F_suc=-k_s*max(0.0,-np.sin(omega*tm))
        v+=dt*(F_rep+F_suc)/m; d+=dt*v
        if d<=0.05: return "collapse"
        if d>12*d0: return "fly_apart"
        ds.append(d)
    ds=np.array(ds[T//2:])
    return "BOUND" if (ds.min()>0.1 and ds.max()<12*d0) else "fly_apart"
print("="*60); print("BST Stage 14 — two-wave bound state (atomic brick)"); print("="*60)
print("\nScan suction strength k_s (synchronized phases):")
print(f"  {'k_s':>6}{'outcome':>14}")
for k_s in [0.0,0.2,0.4,0.6,0.8,1.2,2.0,3.0]:
    print(f"  {k_s:>6.1f}{simulate(k_s=k_s):>14}")
print("\nSynchronization test (k_s in a binding range, vary phase offset):")
print(f"  {'phase offset':>14}{'outcome':>12}")
for ph,lab in [(0.0,"sync"),(np.pi/2,"quarter"),(np.pi,"anti")]:
    print(f"  {lab:>14}{simulate(k_s=0.6,phase2=ph):>12}")
print("\nBrick holds iff: k_s=0 fails (suction needed), a k_s window BINDS, and binding")
print("needs synchronization (anti-phase degrades it).")
