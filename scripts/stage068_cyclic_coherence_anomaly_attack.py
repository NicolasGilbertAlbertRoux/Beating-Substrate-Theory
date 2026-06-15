#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 68 (user: attack the cyclic-coherence / anomaly angle) - does self-consistency FIX the tongue?
The retroactive counter-beat closes the loop on its OWN detuning: Omega = Omega0 + g*w, w = winding(Omega),
solved self-consistently so the detuning is no longer free. Which Arnold tongue does it self-select?
RESULT (pre-registered null HELD): self-consistency does remove the detuning freedom (closure works, kept),
but it self-selects the DOMINANT/widest tongues - 0/1, 1/1, 1/2 (g=0.25: 1/1 6/19, 0/1 4/19, 1/2 2/19;
g=0.5: 0/1 8/19, 1/1 3/19, 1/2 2/19, 1/3 only 1/19 = noise). NEVER robustly 1/3. The anomaly-style sum rule
Sum(w_i)=1 distributes windings but leaves the sector COUNT N as an input (1/N for any N). => cyclic closure
forces the SIMPLEST ratio; the number 3 is specifically BEYOND simple closure. No independent second
prediction emerged. ALL our forcing mechanisms (minimality->2, self-similarity->unconstrained, cyclic
closure->1 or 2) land on 1 or 2, never 3: '3 is not the simplest fixed point of anything'. In real physics
the colour 3 is protected by the Z3 centre of SU(3) (triality) - a SYMMETRY protection, not self-consistency.
So colour SU(3)/Z3 must be POSITED, not derived. The counter-beat is a real methodological gain (stabilising
feedback + a forcing mechanism, kept); it sharpens the wall ('3 is not simplest') without breaching it.
"""
import numpy as np
print("="*76)
print("BST Stage 68 - cyclic coherence as anomaly-analogue: does self-consistency FIX the tongue?")
print("="*76)
def winding(Om,K_r=1.0,n=6000):
    θ=0.0
    for _ in range(300): θ=θ+Om-(K_r/(2*np.pi))*np.sin(2*np.pi*θ)
    t0=θ
    for _ in range(n): θ=θ+Om-(K_r/(2*np.pi))*np.sin(2*np.pi*θ)
    return (θ-t0)/n
def nearest_ratio(w):
    best=(1,1,9); 
    for q in range(1,8):
        for p in range(0,q+1):
            e=abs(w-p/q)
            if e<best[2]-1e-9 and e<0.02: best=(p,q,e)
    return f"{best[0]}/{best[1]}" if best[2]<0.02 else f"{w:.3f}(none)"

# the retroactive counter-beat closes the loop on its OWN detuning: Omega = Omega0 + g*w, w = winding(Omega).
# self-consistent fixed point => detuning is no longer free. Which ratio does it self-select?
def self_consistent(Om0,g,K_r=1.0,iters=80):
    Om=Om0
    for _ in range(iters):
        w=winding(Om,K_r); Om_new=Om0+g*w
        Om_new-=np.floor(Om_new)             # keep on the circle [0,1)
        if abs(Om_new-Om)<1e-4: Om=Om_new; break
        Om=Om_new
    return winding(Om,K_r)

print("\n self-consistent winding selected, scanning the starting detuning Omega0 (g=0.25):")
tally={}
for Om0 in np.linspace(0.05,0.95,19):
    w=self_consistent(Om0,0.25); r=nearest_ratio(w)
    tally[r]=tally.get(r,0)+1
for r,c in sorted(tally.items(),key=lambda kv:-kv[1]):
    print(f"   ratio {r:>10}:  selected from {c:>2}/19 starting points")
print("\n same with stronger retroaction g=0.5:")
tally2={}
for Om0 in np.linspace(0.05,0.95,19):
    w=self_consistent(Om0,0.5); r=nearest_ratio(w)
    tally2[r]=tally2.get(r,0)+1
for r,c in sorted(tally2.items(),key=lambda kv:-kv[1]):
    print(f"   ratio {r:>10}:  selected from {c:>2}/19 starting points")

print("\n(anomaly-style sum rule across N coupled sectors: does Sum(w_i)=1 force N=3?)")
print("  symmetric stable solution = all equal = 1/N for ANY N -> N=2 gives 1/2 each, N=3 gives 1/3 each,")
print("  N=4 gives 1/4 each. The COUNT N is an input; the sum rule distributes but does not force N=3.")

print("\nVERDICT (pre-registered null check)")
print("  Self-consistency DOES remove the detuning freedom - the retroactive counter-beat closes on its own")
print("  parameter and self-selects a definite ratio (real: closure works). But it lands overwhelmingly on the")
print("  DOMINANT tongues (0/1, 1/2, 1/1) - the simplest/widest locks - NOT on 1/3. And the sum-rule analogue")
print("  distributes windings but leaves the sector COUNT as an input. => cyclic closure forces the SIMPLEST")
print("  ratio; the number 3 is specifically BEYOND simple closure. No independent second prediction emerged.")
print("  Honest outcome: the pre-registered null HOLDS. The counter-beat is a real forcing/stabilising mechanism")
print("  (kept), but it selects 1 or 2, never 3 - pinpointing that 3 needs a symmetry-PROTECTED third lock,")
print("  not mere self-consistency. The wall stands, now sharper: '3 is not the simplest fixed point'.")
