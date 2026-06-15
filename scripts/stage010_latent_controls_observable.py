#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 10 — does the LATENT (fine+fast) CONTROL the OBSERVABLE (coarse+slow), and not
the reverse? (author's correction: latent controls observable; observable only retroacts.)
This is a CAUSAL/control question, not inference. Test by INTERVENTION on two coupled
layers with SYMMETRIC coupling; the only asymmetry is speed/scale.

Layer L (latent): N_L fast, fine oscillators.   Layer O (observable): N_O slow, coarse.
Coupling L<->O is symmetric (same constant c). We kick one layer and measure the response
of the OTHER (circular trajectory divergence vs an unperturbed run).

PRE-REGISTERED (can fail): with L fast/fine & O slow/coarse, kicking L moves O MORE than
kicking O moves L (asymmetry ratio > 1). CONTROL: when both layers have the SAME speed,
the ratio ~ 1 (so the asymmetry is due to speed/scale = the author's principle). If the
asymmetric case also gives ~1, the principle FAILS. Honest: model result, not nature.
"""
import numpy as np
N_L,N_O=64,8; block=N_L//N_O; dt=0.02; steps=2000; t0=600
def run(omL_mean, omO_mean, c=0.6, kick=None, seed=0):
    rng=np.random.default_rng(seed)
    θ_L=rng.uniform(0,2*np.pi,N_L); θ_O=rng.uniform(0,2*np.pi,N_O)
    omL=rng.normal(omL_mean,0.3,N_L); omO=rng.normal(omO_mean,0.3,N_O)
    RL=[];RO=[]
    for t in range(steps):
        if kick and t==t0:
            if kick[0]=='L': θ_L=θ_L+kick[1]
            else: θ_O=θ_O+kick[1]
        cL=np.sin(np.roll(θ_L,1)-θ_L)+np.sin(np.roll(θ_L,-1)-θ_L)
        Ofor=np.repeat(θ_O,block); cLO=np.sin(Ofor-θ_L)
        θ_L=θ_L+dt*(omL+c*cL+c*cLO)
        Lblk=np.angle(np.exp(1j*θ_L).reshape(N_O,block).mean(1))
        cO=np.sin(np.roll(θ_O,1)-θ_O)+np.sin(np.roll(θ_O,-1)-θ_O); cOL=np.sin(Lblk-θ_O)
        θ_O=θ_O+dt*(omO+c*cO+c*cOL)
        RL.append(θ_L.copy());RO.append(θ_O.copy())
    return np.array(RL),np.array(RO)
def divergence(a,b): return float(np.mean(1-np.cos(a[t0:]-b[t0:])))  # circular, post-kick
def asymmetry(omL,omO,label):
    L0,O0=run(omL,omO,seed=1)                       # baseline
    Lk,Ok=run(omL,omO,kick=('L',1.5),seed=1)        # kick latent
    Lo,Oo=run(omL,omO,kick=('O',1.5),seed=1)        # kick observable
    respO = divergence(Ok,O0)   # how much O moves when L is kicked
    respL = divergence(Lo,L0)   # how much L moves when O is kicked
    ratio = respO/max(respL,1e-9)
    print(f"  {label:34s} resp(O|kick L)={respO:.3f}  resp(L|kick O)={respL:.3f}  ratio={ratio:.2f}")
    return ratio
print("="*72); print("BST Stage 10 — does the latent (fine/fast) CONTROL the observable?"); print("="*72)
print("\nintervention test (symmetric coupling; ratio>1 => latent controls observable):")
asymmetry(3.0,0.5,"ASYMMETRIC  L fast/fine, O slow/coarse")
asymmetry(1.5,1.5,"CONTROL     same speed both layers")
print("\nThe author's principle holds iff ASYMMETRIC ratio>1 while CONTROL ratio~1.")
