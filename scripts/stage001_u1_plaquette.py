#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Beating Substrate Theory — Stage 1 (funnel): validate a clean compact-U(1) MC.

Cheapest fail-fast: a new, minimal 4D compact-U(1) Wilson gauge Metropolis MC.
Pre-registered observable: average plaquette P = <cos θ_plaq> vs coupling beta.
Pre-registered expectation (textbook compact U(1)):
   - P monotonically increasing in beta,
   - strong coupling (small beta):  P ~ beta/2,
   - weak coupling (large beta):    P -> 1.
If the new code does NOT reproduce this, STOP (machinery broken). Requires numpy.
"""
import numpy as np

def run_u1(L=4, beta=1.0, n_therm=120, n_meas=60, eps=0.5, seed=0):
    rng=np.random.default_rng(seed)
    shape=(4,L,L,L,L)
    θ=rng.uniform(-np.pi,np.pi,shape)        # link angles U_mu(x)=exp(i θ)
    def roll(a,mu,s): return np.roll(a,-s,axis=mu)  # shift site index along dir mu (axes 1..4)
    def staple_sum(mu):
        # complex staple A_mu(x) so that local action ~ -beta Re[exp(i θ_mu) * A]
        A=np.zeros((L,L,L,L),dtype=complex)
        for nu in range(4):
            if nu==mu: continue
            tnu=θ[nu]; tmu=θ[mu]
            # forward staple: U_nu(x+mu) U_mu(x+nu)^* U_nu(x)^*
            f = roll(tnu,mu,1) - roll(tmu,nu,1) - tnu
            # backward staple: U_nu(x+mu-nu)^* U_mu(x-nu)^* U_nu(x-nu)
            b = -roll(roll(tnu,mu,1),nu,-1) - roll(tmu,nu,-1) + roll(tnu,nu,-1)
            A += np.exp(1j*f)+np.exp(1j*b)
        return A
    def sweep():
        acc=0; tot=0
        for mu in range(4):
            A=staple_sum(mu)
            R=np.abs(A); psi=np.angle(A)
            prop=θ[mu]+rng.uniform(-eps,eps,(L,L,L,L))
            dS=-beta*(R*np.cos(prop+psi)-R*np.cos(θ[mu]+psi))
            acc_mask=rng.random((L,L,L,L))<np.exp(-dS)
            θ[mu]=np.where(acc_mask,prop,θ[mu])
            acc+=acc_mask.sum(); tot+=acc_mask.size
        return acc/tot
    def avg_plaquette():
        s=0.0; npl=0
        for mu in range(4):
            for nu in range(mu+1,4):
                tp=θ[mu]+roll(θ[nu],mu,1)-roll(θ[mu],nu,1)-θ[nu]
                s+=np.cos(tp).mean(); npl+=1
        return s/npl
    for _ in range(n_therm): sweep()
    Ps=[]
    for _ in range(n_meas):
        sweep(); Ps.append(avg_plaquette())
    return float(np.mean(Ps)), float(np.std(Ps))

print("="*60); print("BST Stage 1 — compact U(1) MC validation (P vs beta)"); print("="*60)
print(f"{'beta':>6}{'P (meas)':>12}{'beta/2':>10}{'note':>22}")
betas=[0.5,1.0,1.5,2.0,4.0,8.0]; prev=-1; mono=True
for b in betas:
    P,sd=run_u1(beta=b)
    note = "strong~beta/2" if b<=1.0 else ("weak->1" if b>=4 else "transition")
    print(f"{b:>6.1f}{P:>9.3f}±{sd:<4.2f}{b/2:>8.2f}   {note:>18}")
    if P<prev-0.02: mono=False
    prev=P
print("\nPre-registered check: P monotone in beta, ~beta/2 at small beta, ->1 at large.")
print(f"Monotonic in beta: {mono}.  (If yes and limits hold, Stage 1 PASSES -> Stage 2.)")
