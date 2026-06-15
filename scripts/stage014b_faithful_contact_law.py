#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 14b — two-wave bound state with the AUTHOR'S contact law (his specs):
 - ATTRACTION continuous, gravity/curvature-like: F_att = -G/d^2 (->0 at inf, ->large at 0).
 - REPULSION soft & diffuse (tennis-ball-like) when beating mantles overlap:
   F_rep = k*max(0, R1(t)+R2(t) - d),  R_i(t)=R0(1+A sin(omega t + phase_i)).  Continuous gate.
 - energy sustained by the beating. Separation d obeys m d'' = F_att + F_rep.

Exploratory scan (legitimate) WITH controls. Tests the author's two claims falsifiably:
 (1) is the BEATING necessary to bind? -> compare A>0 vs A=0 (static) at the same attraction.
 (2) is SYNCHRONIZATION necessary? -> compare in-phase vs anti-phase.
Outcomes: BOUND (d bounded), COLLAPSE (d->0), ESCAPE (d->inf).
PRE-REGISTERED targets to look for: a regime where STATIC collapses but BEATING binds
(=> beating necessary, author validated); and whether sync vs anti differ.
Honest: 1D toy of a 3D picture; this maps behavior, it is not a measurement of nature.
"""
import numpy as np
def sim(G,A,k=3.0,R0=0.8,omega=1.5,m=1.0,d0=2.5,T=9000,dt=0.01,phase2=0.0):
    d=d0; v=0.0
    for t in range(T):
        tm=t*dt
        R1=R0*(1+A*np.sin(omega*tm)); R2=R0*(1+A*np.sin(omega*tm+phase2))
        F=-G/max(d,0.05)**2 + k*max(0.0,(R1+R2)-d)
        v=np.clip(v+dt*F/m,-60,60); d+=dt*v
        if d<=0.06: return "collapse"
        if d>15*d0: return "escape"
    return "BOUND"
print("="*64); print("BST Stage 14b — two-wave bound state, author's contact law"); print("="*64)
print("\n(1) Is BEATING necessary? scan attraction G; static (A=0) vs beating (A=0.6):")
print(f"  {'G':>6}{'static A=0':>13}{'beating A=0.6':>15}")
for G in [0.3,0.6,1.0,1.6,2.4,3.5,5.0]:
    print(f"  {G:>6.1f}{sim(G,0.0):>13}{sim(G,0.6):>15}")
print("\n(2) Synchronization (pick a G where beating binds), phase offset:")
for ph,lab in [(0.0,"sync"),(np.pi/2,"quarter"),(np.pi,"anti")]:
    print(f"  {lab:>10}: {sim(2.4,0.6,phase2=ph)}")
print("\nBeating necessary iff some G: static=collapse/escape BUT beating=BOUND.")
print("Synchronization matters iff sync vs anti differ.")
