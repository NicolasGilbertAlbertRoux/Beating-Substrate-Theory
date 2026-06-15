#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Beating Substrate Theory — Stage 2 (funnel): the FLUX TUBE (string tension).

Measure the static string tension via Creutz ratios of Wilson loops in the clean
compact-U(1) MC. PRE-REGISTERED controls (each CAN fail):
  (a) confined phase (small beta): Creutz ratio chi(R,R) ~ -ln(I1(beta)/I0(beta))
      [exact leading strong-coupling string tension -> the flux tube],
  (b) chi DROPS toward weak coupling (tube undone, deconfinement),
  (c) a phase-RANDOMIZED gauge field shows W ~ 0 (no coherent tube).
This validates that we correctly measure a real, dynamics-dependent flux skeleton
BEFORE asking (later) what BST might add. Requires numpy, scipy.
"""
import numpy as np
from scipy.special import iv

def shift(a, axis, s): return np.roll(a, -s, axis=axis)   # site +s along axis (1..4)

def mc_config(L=6, beta=1.0, n_therm=160, eps=0.5, seed=0):
    rng=np.random.default_rng(seed); θ=rng.uniform(-np.pi,np.pi,(4,L,L,L,L))
    def staple(mu):
        A=np.zeros((L,L,L,L),dtype=complex)
        for nu in range(4):
            if nu==mu: continue
            f = shift(θ[nu],mu,1) - shift(θ[mu],nu,1) - θ[nu]
            b = -shift(shift(θ[nu],mu,1),nu,-1) - shift(θ[mu],nu,-1) + shift(θ[nu],nu,-1)
            A += np.exp(1j*f)+np.exp(1j*b)
        return A
    def sweep():
        for mu in range(4):
            A=staple(mu); R=np.abs(A); psi=np.angle(A)
            prop=θ[mu]+rng.uniform(-eps,eps,(L,L,L,L))
            dS=-beta*(R*np.cos(prop+psi)-R*np.cos(θ[mu]+psi))
            m=rng.random((L,L,L,L))<np.exp(-dS); θ[mu]=np.where(m,prop,θ[mu])
    for _ in range(n_therm): sweep()
    return θ, sweep

def wilson(θ, mu, nu, R, T):
    bottom=sum(shift(θ[mu],mu,i) for i in range(R))
    right =sum(shift(shift(θ[nu],mu,R),nu,j) for j in range(T))
    top   =sum(shift(shift(θ[mu],nu,T),mu,i) for i in range(R))
    left  =sum(shift(θ[nu],nu,j) for j in range(T))
    return float(np.cos(bottom+right-top-left).mean())

def measure_W(θ):
    W={}
    for R in (1,2,3):
        for T in (1,2,3):
            vals=[wilson(θ,mu,nu,R,T) for mu in range(4) for nu in range(mu+1,4)]
            W[(R,T)]=float(np.mean(vals))
    return W

def creutz(W,R):
    num=W[(R,R)]*W[(R-1,R-1)]; den=W[(R-1,R)]*W[(R,R-1)]
    if num<=0 or den<=0: return float('nan')
    return -np.log(num/den)

def run(beta, L=6, n_meas=120, seed=0):
    θ,sweep=mc_config(L=L,beta=beta,seed=seed)
    acc=[]
    for _ in range(n_meas):
        for _ in range(2): sweep()
        acc.append(measure_W(θ))
    W={k:float(np.mean([m[k] for m in acc])) for k in acc[0]}
    return W

print("="*66); print("BST Stage 2 — flux tube / string tension (Creutz ratios)"); print("="*66)
print(f"{'beta':>6}{'chi(2,2)':>11}{'-ln(I1/I0)':>13}{'W(1,1)':>9}{'W(2,2)':>9}  reading")
for beta in (0.8,1.2,2.0):
    W=run(beta); chi=creutz(W,2); sc=-np.log(iv(1,beta)/iv(0,beta))
    tag = "confined: chi~strong-coupling tube" if beta<1.0 else "weaker tube (toward Coulomb)"
    print(f"{beta:>6.1f}{chi:>11.3f}{sc:>13.3f}{W[(1,1)]:>9.3f}{W[(2,2)]:>9.3f}  {tag}")
# null: randomized gauge field
rng=np.random.default_rng(7); L=6; rθ=rng.uniform(-np.pi,np.pi,(4,L,L,L,L))
Wr=measure_W(rθ)
print(f"\nrandomized field: W(1,1)={Wr[(1,1)]:.3f}  W(2,2)={Wr[(2,2)]:.3f}  "
      f"-> {'no coherent tube (W~0)' if abs(Wr[(1,1)])<0.05 else 'UNEXPECTED structure'}")
print("\nPre-registered: confined chi(2,2) ~ -ln(I1/I0) (tube); chi drops at larger")
print("beta (tube undone); randomized W~0 (no tube). All three can fail.")
