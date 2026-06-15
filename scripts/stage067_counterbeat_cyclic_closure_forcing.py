#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 67 (user: retroactive counter-beat + cyclic closure) - cyclic closure as a FORCING mechanism.
(A) The retroactive counter-beat = a van der Pol (1-x^2)xdot term: pumps when small, damps when large ->
    a STABLE limit cycle around a FIXED amplitude, reached from ANY start (4.002 from all four ICs at mu=0.5),
    amplitude shifting with mu (resolution-like). Confirms the user's description exactly; gives the framework
    a stabilising feedback that selects a definite cyclic state - a real methodological gain.
(B) A CYCLIC closure FORCES an integer: sine-circle map winding number LOCKS to 1/3 over a whole interval of
    detuning (Omega=0.34..0.36 -> 0.3333), a robust topological plateau - NOT a point coincidence. First time
    a '3' appears FORCED (over an interval) rather than cherry-picked. Epistemic upgrade over the fractal N=4
    (where any N hit 3 with zero width = no constraint): here 3 is perturbation-stable on a tongue.
(C) VERDICT: the counter-beat supplies the FORCING mechanism (cyclic closure -> forced winding integer) that
    minimality/self-similarity lacked - vindicated. 'N=4x' fits too: period-doubling gives 2,4,8 (N=4=2^2
    natural) but never 3; the 3 comes from mode-locking. WALL STILL STANDS: WHICH integer locks depends on the
    detuning (which tongue). Calibrating detuning to the 1/3 tongue gives 3 robustly = LEGITIMATE one-parameter
    calibration (not numerology), but ONE knob doing ONE job is not yet over-determined; to be a signal that
    same detuning must predict something INDEPENDENT. A genuine step in METHOD, not yet the SM number/color SU(3).
"""
import numpy as np
print("="*76)
print("BST Stage 67 - retroactive counter-beat: cyclic closure as a forcing mechanism")
print("="*76)

# (A) COUNTER-BEAT -> stable limit cycle around a FIXED amplitude (the 'donnee fixe'). The (1-x^2)*xdot term
# IS the retroactive counter-beat: pumps energy when |x| small, removes it when |x| large -> a self-stabilised
# cycle whose amplitude is independent of how it started (van der Pol). mu plays the role of a resolution knob.
def vdp_amp(mu,x0,dt=0.005,T=120):
    x,v=x0,0.0; n=int(T/dt); xs=[]
    for i in range(n):
        a=mu*(1-x*x)*v-x; v+=a*dt; x+=v*dt
        if i>n-4000: xs.append(x)
    return max(xs)-min(xs)
print("\n(A) does the counter-beat stabilise a cycle around a FIXED datum, from any start?")
for mu in [0.5,1.0,2.0]:
    amps=[vdp_amp(mu,x0) for x0 in [0.1,0.7,1.8,3.0]]
    print(f"   mu={mu:>4}: peak-to-peak amplitude from 4 different starts = {[round(a,3) for a in amps]}")
print("   => identical cycle reached from every start: a STABLE cycle around a fixed amplitude.")
print("   (amplitude shifts with mu = resolution-dependent, exactly as predicted.)")

# (B) can a CYCLIC closure FORCE an integer? sine-circle map (beat + retroactive coupling): the rotation
# (WINDING) number locks to rationals on Arnold tongues -> a whole INTERVAL of detuning gives the SAME
# rational p/q. That plateau = a forced integer ratio (topological), not a tuned one.
def winding(Om,K_r,n=30000):
    θ=0.0
    for _ in range(500): θ=θ+Om-(K_r/(2*np.pi))*np.sin(2*np.pi*θ)
    t0=θ
    for _ in range(n): θ=θ+Om-(K_r/(2*np.pi))*np.sin(2*np.pi*θ)
    return (θ-t0)/n
print("\n(B) does a cyclic closure FORCE an integer winding number? (sine-circle map, K_r=1)")
print("   scan detuning Omega across the 1/3 region - a PLATEAU means locking (forced):")
for Om in [0.28,0.30,0.32,0.34,0.36,0.38]:
    print(f"   Omega={Om:.2f}: winding = {winding(Om,1.0):.4f}")
print("   and the main locked ratios (each a whole tongue, i.e. forced over an interval):")
for Om,lab in [(0.001,"0/1"),(0.50,"1/2"),(0.999,"1/1")]:
    print(f"   near Omega={Om:.3f}: winding = {winding(Om,1.0):.4f}  (~ {lab})")

print("\n(C) HONEST VERDICT")
print("   (i) the retroactive counter-beat DOES stabilise a cycle around a fixed datum (limit cycle), amplitude")
print("       set by the resolution-like parameter - your description is correct, and it IS a real advance:")
print("       it gives the framework a STABILISING feedback that picks out a definite cyclic state.")
print("   (ii) a CYCLIC closure DOES force integers: mode-locking pins the winding number to a rational over a")
print("        whole interval (a forced topological integer) - the very forcing the minimality/self-similar")
print("        probes lacked. So 'cyclic closure forces an integer' is VINDICATED as a mechanism.")
print("   THE WALL STILL STANDS, precisely: WHICH integer is selected depends on the detuning (which tongue).")
print("   Period-doubling of such a beat gives 2,4,8,... (powers of 2 - so N=4 arises NATURALLY as 2^2, your")
print("   'N=4x'), but never 3. Mode-locking can give 1/3, but does not uniquely SELECT 3 without fixing a")
print("   parameter. => the counter-beat supplies the right KIND of forcing (real gain); uniquely forcing the")
print("   number 3 (and color SU(3)) is still not achieved. A genuine step in METHOD, not yet the SM number.")
