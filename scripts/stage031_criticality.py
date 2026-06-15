#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 31 — is the beating-phase substrate CRITICAL (scale-invariant)? (the pivot test.)
S30 showed: cross-resolution calibration reaches deep ONLY if the substrate's coupling is near
scale-invariant (critical). Here we test the substrate's own phase-correlation structure (its 2D
XY-equilibrium description) across coupling strength (= 1/T). We measure C(r)=<cos(θ(0)-
θ(r))> and ask: POWER-LAW decay (scale-invariant -> critical -> resolution chain is ONE) or
EXPONENTIAL (a characteristic length -> off-critical -> chain fragmented)?

The 2D XY model is special (Kosterlitz-Thouless): below T_KT~0.89 it has an ENTIRE critical PHASE
with power-law correlations (quasi-long-range order), not just a single critical point. PRE-
REGISTERED: strong coupling / low T -> power-law (critical, scale-invariant); weak coupling / high
T -> exponential (finite xi). If so, the substrate is critical over a BROAD regime -> the cross-
scale predictivity condition of S30 is generically met in the ordered phase. Honest: this is the
XY-equilibrium proxy for the beating substrate's phase correlations; KT is standard physics --
the point is whether the substrate inherits a broad scale-invariant phase, not new physics.
"""
import numpy as np
def mc_sweep(θ,T,rng,delta=1.5):
    i,j=np.indices(θ.shape)
    for color in (0,1):
        mask=((i+j)%2==color)
        θp=θ+delta*rng.uniform(-np.pi,np.pi,θ.shape)
        up,dn,lf,rt=np.roll(θ,1,0),np.roll(θ,-1,0),np.roll(θ,1,1),np.roll(θ,-1,1)
        Eo=-(np.cos(θ-up)+np.cos(θ-dn)+np.cos(θ-lf)+np.cos(θ-rt))
        En=-(np.cos(θp-up)+np.cos(θp-dn)+np.cos(θp-lf)+np.cos(θp-rt))
        acc=(rng.random(θ.shape)<np.exp(-(En-Eo)/T))&mask
        θ=np.where(acc,θp,θ)
    return θ
def corr(θ,rmax):
    return np.array([0.5*(np.mean(np.cos(θ-np.roll(θ,r,0)))+np.mean(np.cos(θ-np.roll(θ,r,1))))
                     for r in range(1,rmax)])
def run(T,L=48,eq=3000,meas=500,seed=0):
    rng=np.random.default_rng(seed); θ=rng.uniform(0,2*np.pi,(L,L))
    for _ in range(eq): θ=mc_sweep(θ,T,rng)
    acc=np.zeros(L//2-1)
    for m in range(meas):
        θ=mc_sweep(θ,T,rng)
        if m%5==0: acc+=corr(θ,L//2)
    return acc/(meas//5)
def classify(C):
    r=np.arange(1,len(C)+1); good=C>0.02
    if good.sum()<4: return "exp(short)",0,0
    lr,lc,rr=np.log(r[good]),np.log(C[good]),r[good]
    # power-law fit: log C vs log r ; exponential fit: log C vs r
    pw=np.polyfit(lr,lc,1); ex=np.polyfit(rr,lc,1)
    r2=lambda y,f:1-np.sum((y-f)**2)/np.sum((y-y.mean())**2)
    r2pw=r2(lc,np.polyval(pw,lr)); r2ex=r2(lc,np.polyval(ex,rr))
    xi=-1/ex[0] if ex[0]<0 else np.inf
    return ("POWER-LAW (critical)" if r2pw>=r2ex else "EXPONENTIAL (off-critical)"), r2pw, r2ex, -pw[0], xi
print("="*72); print("BST Stage 31 — is the beating-phase substrate critical (scale-invariant)?"); print("="*72)
print(f"\n  (T_KT ~ 0.89; strong coupling = low T)")
print(f"  {'T':>5}{'C(1)':>8}{'C(half)':>9}   best fit                exponent / xi")
for T in [0.40,0.70,1.00,1.40]:
    C=run(T); kind,r2pw,r2ex,η,xi=classify(C)
    tail = f"η~{η:.2f}" if "POWER" in kind else f"xi~{xi:.1f}"
    print(f"  {T:>5.2f}{C[0]:>8.3f}{C[-1]:>9.3f}   {kind:<26}{tail}")
print("\nPower-law at low T => the substrate has a broad SCALE-INVARIANT (critical) phase =>")
print("the resolution chain is ONE there (S30 cross-scale predictivity condition met).")
print("Exponential at high T => characteristic length => chain fragmented.")
