#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 11 — refined claim: the FAST controls the SLOW where the LEVERS (attractors)
are accessible, and SPEED lets it catch the fleeting lever. (author's sharpened ontology.)

Slow bistable plant: dx = a(x - x^3) dt + noise dW + u dt. Wells at +/-1, barrier at 0.
Start in the + well; goal: flip to the - well. Control input u is SMALL (below the
deterministic barrier force) and is applied ONLY when |x| is near the barrier (= lever
accessible). A FAST controller samples every step (catches noise excursions to the lever);
a SLOW controller samples rarely (misses them).

PRE-REGISTERED (can fail): FAST+noise flips often; SLOW+noise rarely (misses levers);
FAST+NO-noise ~never (no lever appears -> small input can't climb the barrier). This would
confirm BOTH: control needs accessible levers AND speed to catch them. Honest: model result.
"""
import numpy as np
def trial(fast, noise, seed, a=0.3, dt=0.05, T=8000, u_max=0.08, lever=0.35):
    rng=np.random.default_rng(seed); x=1.0; period=1 if fast else 25; u=0.0
    for t in range(T):
        if t % period == 0:
            u = -u_max if (x>0 and abs(x)<lever) else 0.0   # push only at the lever
        x += dt*(a*(x - x**3) + u) + noise*np.sqrt(dt)*rng.normal()
        if x < -0.7: return True
    return False
def rate(fast, noise, n=80):
    return float(np.mean([trial(fast,noise,seed=s) for s in range(n)]))
print("="*64); print("BST Stage 11 — control at accessible levers + speed to catch them"); print("="*64)
print("(small input, applied only near the attractor boundary = the lever)\n")
print(f"  FAST controller + noise (can catch levers) : flip rate = {rate(True,0.5):.2f}")
print(f"  SLOW controller + noise (misses levers)    : flip rate = {rate(False,0.5):.2f}")
print(f"  FAST controller + NO noise (no lever)      : flip rate = {rate(True,0.0):.2f}")
print("\nRefined principle holds iff fast+noise >> slow+noise, and fast+no-noise ~ 0")
print("(control needs an accessible lever AND the speed to seize it).")

# --- FOLLOW-UP (honest record): does controller SPEED / bandwidth matter? ---
# Tested 3 ways (long horizon; time pressure; bandwidth scan with controller period
# from 1 to 800 steps, i.e. up to ~12x SLOWER than the plant's ~50-67 step timescale).
# RESULT: flip rate stayed 1.00 at EVERY controller period. Controller speed does NOT
# matter for this attractor-SWITCHING task: one well-placed push at a lever suffices and
# time provides enough chances. The "faster-than-plant" principle applies to CONTINUOUS
# TRACKING/STABILIZATION (reacting to fast disturbances), NOT to occasional switching.
# CONCLUSION: LEVER access = CONFIRMED necessary; controller SPEED = REFUTED for switching.
