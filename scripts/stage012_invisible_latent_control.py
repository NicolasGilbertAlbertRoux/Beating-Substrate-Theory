#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 12 — INVISIBLE LATENT CONTROL (author's reframed claim). Speed's role is not
control-bandwidth (refuted in S11) but INVISIBILITY: a latent oscillating faster than the
observable's sampling/resolution is ALIASED -> invisible to the observable's aliasing; yet
it can still CONTROL the slow plant via levers (S11). The observable sees only the EFFECT
(its slow state), not the CAUSE (the fast latent).

Part A — invisibility by temporal aliasing: a fast latent (freq f_L) sampled by a SLOW
observable yields a WRONG (aliased) recovered frequency; a FAST observer recovers f_L.
Part B — control: the SAME fast latent flips the slow bistable plant (lever-gated push).

PRE-REGISTERED (can fail): slow observer recovers freq != f_L (invisible); fast observer
recovers ~f_L (it's really there); and the fast latent flips the plant (controls it).
Honest: a model demonstration uniting aliasing (resolution channel) + lever control (S11).
"""
import numpy as np
rng=np.random.default_rng(0); fL=3.0; total=40.0
print("="*64); print("BST Stage 12 — invisible latent control"); print("="*64)
print(f"\nPart A — is a fast latent (f_L={fL}) visible to an observer's sampling?")
for fobs in [1.0, 0.7, 20.0]:
    ts=np.arange(0,total,1.0/fobs); z=np.sin(2*np.pi*fL*ts)
    fr=np.fft.rfftfreq(len(ts),d=1.0/fobs); P=np.abs(np.fft.rfft(z)); frec=fr[1+np.argmax(P[1:])]
    tag="VISIBLE" if abs(frec-fL)<0.3 else "ALIASED/invisible"
    print(f"  observer f_s={fobs:>4} (Nyquist {fobs/2:.2f}): recovered f={frec:.2f}  ->  {tag}")
print(f"\nPart B — does the SAME fast latent CONTROL the slow plant (flip it)?")
def control_trial(seed, dt=0.005, a=0.3, u_max=0.10, lever=0.35, noise=0.4, T=8000):
    rng=np.random.default_rng(seed); x=1.0
    for t in range(T):
        lat=np.sin(2*np.pi*fL*t*dt)
        push=-u_max if (lat>0 and x>0 and abs(x)<lever) else 0.0
        x+=dt*(a*(x-x**3)+push)+noise*np.sqrt(dt)*rng.normal()
    return x<-0.5
rate=np.mean([control_trial(s) for s in range(60)])
print(f"  fast latent flips the slow plant: success rate = {rate:.2f}")
print("\nInvisible latent control holds iff: slow observer ALIASES the latent (cannot see")
print("its true frequency) WHILE the latent still controls the plant. Observable sees the")
print("effect (state), not the cause (fast latent) -- exactly the author's picture.")

# --- ESSENTIAL CONTROL (honest record): does the latent CONTROL, or does noise flip? ---
# Compared latent-ON vs no-latent (baseline) across noise levels 0.10..0.45. Control gain
# (ON - baseline) was <=0.04 everywhere: the latent push does NOT beat noise-driven escape.
# => Part B (invisible latent CONTROL) FAILS: the latent is invisible (Part A, solid) but
# does NOT demonstrably control the plant; noise does the flipping. This ALSO retroactively
# corrects Stage 11: that 'lever control confirmed' lacked a no-push baseline; with it, the
# push adds ~nothing, so S11's control claim was likely a noise artifact too.
# WHAT HOLDS: invisibility via aliasing (resolution channel). WHAT FAILS: latent control.
