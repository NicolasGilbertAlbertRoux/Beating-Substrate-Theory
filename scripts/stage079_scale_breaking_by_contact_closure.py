#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 79 (user: S78 closed too fast - does the model break scale-invariance INTERNALLY?). The user is
right: S78 only rules out the EXACTLY scale-free case. The model has scale-breaking ingredients (dissipation,
lockings, contact closures) that can SELECT a scale - and dimensional transmutation can generate hierarchies.
[A] A feedback/closure DOES select a definite scale (van der Pol limit-cycle attractor: amplitude 2/sqrt(beta),
    start-independent). But it tracks the closure coefficient beta -> for the ABSOLUTE scale the freedom
    relocates to that coefficient (not absolute-from-nothing).
[B] DIMENSIONAL TRANSMUTATION (the real lead): a dimensionless coupling g0 that runs generates an exponential
    scale RATIO Lambda/mu0 = exp(-1/(2 b g0^2)) (g0=0.25 -> ~35 orders). This is how QCD makes Lambda_QCD and
    how hierarchies are NATURAL. The model's closures could transmute into the mass/Planck ratio.
[C] IRONCLAD CEILING (dimensional analysis): a dimensionful number needs ONE reference scale - so ONE anchor
    (a unit = the posited kink value, a legitimate calibration) is unavoidable. But RATIOS can emerge on top.
    S78 conflated 'absolute scale' (needs 1 unit) with 'ratios' (can emerge) - that was the over-reach.
[D] G ~ (induced curvature)/(kink energy) can share the UV/kink/closure lock; Lambda ~ 1/L_IR^2 (horizon) is a
    SEPARATE IR scale -> plausibly a SECOND lock. The user's anticipation is correct.
VERDICT: the door is RE-OPENED. Honest live program: (1) posit ONE kink/closure unit (unavoidable anchor);
(2) seek the dimensionless closure that transmutes into the mass/G hierarchy; (3) test whether Lambda follows
the same lock or a second IR/horizon lock. RESERVE: transmutation is the right TYPE of mechanism and a genuine
avenue, but it is NOT yet shown that the model's specific closures produce the OBSERVED hierarchy or the messy
mass spectrum - that remains to be done. Corrects S78's over-reach; magnitudes are a live avenue, not a closed door.
"""
import numpy as np
print("="*78)
print("BST Stage 79 - Scale-breaking by contact closure: does the model select a scale internally?")
print("="*78)

print("\n[A] does a feedback/closure select a definite scale (attractor)?  (van der Pol limit cycle, S67)")
def vdp_amp(mu,beta,x0,dt=0.005,T=120):
    x,v=x0,0.0; n=int(T/dt); xs=[]
    for i in range(n):
        a=mu*(1-beta*x*x)*v-x; v+=a*dt; x+=v*dt
        if i>n-4000: xs.append(x)
    return (max(xs)-min(xs))/2
print("   amplitude attractor from different starts (mu=1):")
for beta in [1.0,4.0,0.25]:
    amps=[vdp_amp(1.0,beta,x0) for x0 in [0.2,1.0,2.5]]
    print(f"   beta={beta:>4}: amplitude = {[round(a,3) for a in amps]}  (attractor ~ 2/sqrt(beta) = {2/np.sqrt(beta):.3f})")
print("   => YES, a closure selects a definite scale (attractor, start-independent). BUT it TRACKS beta (the")
print("   nonlinear/closure coefficient): the selected scale relocates the freedom to that coefficient. An")
print("   attractor fixes the scale RELATIVE to a parameter - not an absolute scale from nothing.")

print("\n[B] dimensional transmutation: can a DIMENSIONLESS coupling generate a scale RATIO? (this is the real lead)")
# RG running dg/d(ln mu) = -b g^3 (asymptotic freedom) -> scale where g diverges: Lambda = mu0 * exp(-1/(2 b g0^2))
b=0.1
print("   emergent scale ratio Lambda/mu0 = exp(-1/(2 b g0^2)) from a dimensionless coupling g0:")
for g0 in [0.5,0.4,0.3,0.25]:
    ratio=np.exp(-1/(2*b*g0**2))
    print(f"   g0={g0}: Lambda/mu0 = {ratio:.3e}   ({np.log10(ratio):.1f} orders below the reference)")
print("   => a small DIMENSIONLESS coupling generates an EXPONENTIALLY large hierarchy from a reference scale.")
print("   This is how QCD makes Lambda_QCD, and how hierarchies can be NATURAL (not fine-tuned). The model's")
print("   contact/feedback closures could do the same -> the mass/Planck RATIO could be emergent.")

print("\n[C] the ironclad ceiling (dimensional analysis, not a model flaw):")
print("   you cannot get a dimensionful number from purely dimensionless inputs without ONE reference scale.")
print("   So ONE dimensionful anchor (a unit) is always needed - this is exactly the 'posited kink value',")
print("   a legitimate calibration. What transmutation CAN give for free is the RATIOS (hierarchies) on top of")
print("   that one anchor. S78 conflated 'absolute scale' (needs 1 unit, always) with 'ratios' (can emerge).")

print("\n[D] does ONE closure fix G AND Lambda, or are two locks needed?")
print("   G ratio  ~ (induced curvature)/(kink energy): can follow from the SAME closure (UV/kink scale).")
print("   Lambda   ~ 1/L_IR^2: L_IR = the horizon = a separate IR scale, NOT the kink/UV closure.")
print("   => G can share the kink/closure lock; Lambda plausibly needs a SECOND, IR lock (horizon/resolution).")
print("   Your own anticipation is right: one calibrator likely fixes masses & G (a UV closure), Lambda a second.")

print("\nVERDICT (honest - the door is RE-OPENED, precisely)")
print("  You were right: S78 only rules out the EXACTLY scale-free case. The model's closures DO break scale-")
print("  invariance and select scales (attractors), and DIMENSIONAL TRANSMUTATION can generate exponential")
print("  hierarchies from dimensionless couplings (the real, QCD-like lead for the mass/Planck ratio). The hard")
print("  ceiling is only this: ONE dimensionful anchor (a unit = the posited kink value) is unavoidable by pure")
print("  dimensional analysis - but it is a single legitimate calibration, and the RATIOS can be emergent on top")
print("  of it. So the honest, live program is: (1) posit ONE kink/closure unit; (2) seek the dimensionless")
print("  closure that transmutes into the mass/G hierarchy; (3) test whether Lambda follows the same lock or a")
print("  second IR/horizon lock. That is a genuine open avenue - not a closed door. Thank you for the catch.")
