#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 3a — VALIDATE DeGrand-Toussaint monopole extraction (before any claim).
Two correctness controls that CAN fail:
  (1) current conservation: monopole currents must form CLOSED loops -> div m = 0
      exactly at every dual site (integer). If not, the extraction is wrong.
  (2) known physics: monopole density high in confined phase (small beta), dropping
      sharply across deconfinement (beta ~ 1). If flat/inverted, extraction wrong.
Only if BOTH pass do we proceed to loop geometry (the user's spiral test).
"""
import numpy as np
from itertools import permutations

def shift(a,axis,s): return np.roll(a,-s,axis=axis)

def eps4(a,b,c,d):
    idx=(a,b,c,d)
    if len(set(idx))!=4: return 0
    s=1
    for i in range(4):
        for j in range(i+1,4):
            if idx[i]>idx[j]: s=-s
    return s

def mc(L=6, beta=1.0, n_therm=160, eps=0.5, seed=0):
    rng=np.random.default_rng(seed); θ=rng.uniform(-np.pi,np.pi,(4,L,L,L,L))
    def staple(mu):
        A=np.zeros((L,L,L,L),dtype=complex)
        for nu in range(4):
            if nu==mu: continue
            f=shift(θ[nu],mu,1)-shift(θ[mu],nu,1)-θ[nu]
            b=-shift(shift(θ[nu],mu,1),nu,-1)-shift(θ[mu],nu,-1)+shift(θ[nu],nu,-1)
            A+=np.exp(1j*f)+np.exp(1j*b)
        return A
    for _ in range(n_therm):
        for mu in range(4):
            A=staple(mu); R=np.abs(A); psi=np.angle(A)
            prop=θ[mu]+rng.uniform(-eps,eps,(L,L,L,L))
            dS=-beta*(R*np.cos(prop+psi)-R*np.cos(θ[mu]+psi))
            m=rng.random((L,L,L,L))<np.exp(-dS); θ[mu]=np.where(m,prop,θ[mu])
    return θ

def plaq_int(θ,mu,nu):
    tp=θ[mu]+shift(θ[nu],mu,1)-shift(θ[mu],nu,1)-θ[nu]
    return np.round(tp/(2*np.pi)).astype(int)     # Dirac string integer n_{mu,nu}

def monopoles(θ):
    L=θ.shape[1]; n={}
    for mu in range(4):
        for nu in range(mu+1,4):
            n[(mu,nu)]=plaq_int(θ,mu,nu)
    def nf(r,s):
        if r==s: return np.zeros((L,)*4,int)
        return n[(r,s)] if r<s else -n[(s,r)]
    m=[]
    for mu in range(4):
        acc=np.zeros((L,)*4)
        for nu in range(4):
            for r in range(4):
                for s in range(4):
                    e=eps4(mu,nu,r,s)
                    if e==0: continue
                    acc=acc+0.5*e*(shift(nf(r,s),nu,1)-nf(r,s))
        m.append(np.round(acc).astype(int))
    return m   # m[mu](x): monopole current on dual links

def divergence(m):
    L=m[0].shape[0]; d=np.zeros((L,)*4,int)
    for mu in range(4):
        d=d+(shift(m[mu],mu,1)-m[mu])   # FORWARD diff (matches forward-diff curl -> exact conservation)
    return d

print("="*60); print("BST Stage 3a — monopole extraction validation"); print("="*60)
print(f"{'beta':>6}{'density':>10}{'max|div m|':>12}  control")
betas=[0.6,0.8,1.0,1.2,1.6,2.0]; dens=[]
for beta in betas:
    th=mc(beta=beta); m=monopoles(th)
    rho=float(np.mean([np.abs(mm).mean() for mm in m]))
    md=int(np.max(np.abs(divergence(m))))
    dens.append(rho)
    print(f"{beta:>6.1f}{rho:>10.4f}{md:>12}  {'CLOSED loops OK' if md==0 else 'NOT CONSERVED!'}")
print("\nControl 1 (conservation): max|div m| must be 0 at every beta.")
print(f"Control 2 (physics): density must DROP across deconfinement (~beta=1). "
      f"monotone-decreasing: {all(dens[i]>=dens[i+1]-1e-4 for i in range(len(dens)-1))}")
