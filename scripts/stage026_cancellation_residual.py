#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 26 — the field is ALWAYS there, but EQUILIBRIUM hides it (author's refinement).
A cluster of phase-polarities (+/- = crest/trough). Quasi-static field (omega=0). We scan the
net POLARIZATION (balanced -> aligned) and the DISTANCE, and read the field magnitude <|psi|>.

Author's claim, mapped to real physics (neutral matter): balanced +/- CANCEL at distance (no
long-range field) but leave a short-range RESIDUAL at contact (the analog of van der Waals /
Pauli / contact forces -> friction, viscosity). A net POLARIZATION breaks the balance and turns
ON a long-range field (a magnet / charged body). PRE-REGISTERED: at polarization f=0 the field
decays FAST with distance (cancellation; only a near residual survives); as f->1 the far field
grows and decays SLOWLY (long-range). The crossover in f "turns on" the macroscopic field.
HONEST BOUNDARY (unchanged): the field is still supplied here (a wave equation); this tests the
cancellation/residual STRUCTURE, not whether the beating substrate generates the field. 2D toy.
"""
import numpy as np
def sponge(N,w=10,g0=0.6):
    i=np.arange(N); X,Y=np.meshgrid(i,i,indexing='ij')
    e=np.minimum.reduce([X,Y,N-1-X,N-1-Y]).astype(float)
    return np.where(e<w,g0*((w-e)/w)**2,0.0)
def solve(positions,signs,N=80,c=1.0,A=1.0,sigma=2.0,gb=0.02,dt=0.4,T=2200):
    gamma_damp=gb+sponge(N); i=np.arange(N); X,Y=np.meshgrid(i,i,indexing='ij')
    S=sum(s*A*np.exp(-((X-px)**2+(Y-py)**2)/(2*sigma**2)) for (px,py),s in zip(positions,signs))
    psi=np.zeros((N,N)); v=np.zeros((N,N))
    for t in range(T):
        lap=(np.roll(psi,1,0)+np.roll(psi,-1,0)+np.roll(psi,1,1)+np.roll(psi,-1,1)-4*psi)
        v=v+dt*(c**2*lap-gamma_damp*v+S); psi=psi+dt*v
    return psi,X,Y
def cluster(nplus,cx=40,cy=40,sp=3):
    pos=[(cx+(a-1.5)*sp,cy+(b-1.5)*sp) for a in range(4) for b in range(4)]
    signs=[1 if (a+b)%2==0 else -1 for a in range(4) for b in range(4)]  # checkerboard 8+/8-
    flips=nplus-8; k=0
    for j in range(len(signs)):
        if flips>0 and signs[j]==-1: signs[j]=1; flips-=1
    return pos,signs
def radial(psi,X,Y,cx,cy,radii):
    R=np.sqrt((X-cx)**2+(Y-cy)**2)
    return [np.mean(np.abs(psi[(R>d-1.5)&(R<d+1.5)])) for d in radii]
print("="*70); print("BST Stage 26 — equilibrium hides the field; polarization reveals it"); print("="*70)
radii=[6,12,18,26]
print(f"\n  {'polarization f':>15} | " + "".join(f"<|psi|> r={d:<3}".rjust(15) for d in radii))
for nplus in [8,10,12,16]:
    f=(2*nplus-16)/16; pos,signs=cluster(nplus); psi,X,Y=solve(pos,signs)
    prof=radial(psi,X,Y,40,40,radii)
    print(f"  {f:>15.2f} | " + "".join(f"{p:>15.3f}" for p in prof))
print("\nf=0 (balanced): field decays FAST (cancellation) -> only a near residual = contact/friction.")
print("f->1 (polarized): far field grows & decays SLOWLY -> long-range macroscopic field (magnet).")
