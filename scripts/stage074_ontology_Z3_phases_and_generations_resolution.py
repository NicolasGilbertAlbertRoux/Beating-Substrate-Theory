#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 74 (user post-reading ontological feedback on the two SM inputs).
[A] PROPOSAL 1 - is colour Z3 the three phases of the beat (contraction/dilatation/in-between)? REFUTED as a
    derivation: a single beat cycle has Z2 symmetry (cos(t+pi)=-cos(t), order 2), with TWO turning points, not a
    third equal state; a genuine Z3 needs three phases at 120deg (sum=0) = positing Z3 in another form; and
    colour is INTERNAL while beat phases are TEMPORAL (orthogonal, S69), so identifying them crosses that
    orthogonality. Appealing but relocates/conflates - does NOT derive Z3. P1 stays posited.
[B] PROPOSAL 2 - do extra generations fall below the resolution threshold? AFFIRMED - a real improvement.
    Tongue widths decrease (1/2=0.074>1/3=0.031>1/4=0.016>1/5=0.008>1/6~0); with the resolution threshold
    (the aliasing = base II) cutting between the 3rd and 4th lock (w_thr~0.012), exactly THREE locks are
    detectable, the rest fall into the latent (undetectable). This UPGRADES P2: from 'hierarchy truncates at
    three' (ad hoc) to 'the hierarchy is infinite but only locks wider than the resolution are observable' -
    tied to the framework's CORE concept (resolution), and PREDICTS extra sub-threshold generations
    (heavier/undetectable), consistent with no observed light 4th generation. Residual posit shrinks to 'the
    resolution threshold sits between the 3rd and 4th lock' (a physical calibration, not an arbitrary number).
    Count three still threshold-dependent (not uniquely forced) but P2 is now natural, unified, content-ful.
"""
import numpy as np
print("="*76)
print("BST Stage 74 - two ontological proposals on the SM inputs (color Z3 ; three generations)")
print("="*76)

print("\n[A] PROPOSAL 1: is Z3 the three phases of the beat (contraction / dilatation / brief in-between)?")
t=np.linspace(0,2*np.pi,2000,endpoint=False); beat=np.cos(t)
# symmetry of a single beat cycle: half-period maps contraction<->dilatation with a sign flip -> Z2 (order 2)
halfshift=np.cos(t+np.pi)
print(f"   single beat cycle under t->t+T/2: cos(t+pi) = -cos(t)  (max dev {np.max(np.abs(halfshift+beat)):.1e}) -> Z2, order 2")
print("   so a contraction/dilatation beat has TWO main phases related by half-period = Z2, and TWO turning")
print("   points (max & min), not one 'third state'. Z2 is order 2, not the order-3 Z3.")
# a genuine Z3 needs THREE phases at 120deg (three-phase), which sum to zero:
three=sum(np.cos(t-2*np.pi*k/3) for k in range(3))
print(f"   a genuine Z3 = THREE phases at 120deg: sum_k cos(t-2pi k/3) = {np.max(np.abs(three)):.1e} (==0) -> three-phase")
print("   VERDICT: a simple beat gives Z2, not Z3. Getting Z3 needs a genuinely THREE-PHASE beat = positing Z3")
print("   in another form. And colour is an INTERNAL index while beat phases are TEMPORAL (orthogonal, S69), so")
print("   identifying them crosses that orthogonality. Appealing picture, but it relocates/conflates - it does")
print("   NOT derive the colour Z3. (honest: I have to push back here.)")

print("\n[B] PROPOSAL 2: do EXTRA generations simply fall below the resolution threshold (undetectable)?")
def winding(Om,K_r,n=4000):
    θ=0.0
    for _ in range(300): θ=θ+Om-(K_r/(2*np.pi))*np.sin(2*np.pi*θ)
    t0=θ
    for _ in range(n): θ=θ+Om-(K_r/(2*np.pi))*np.sin(2*np.pi*θ)
    return (θ-t0)/n
def width(q,K_r=1.0,N=700,tol=1.2e-3):
    lo,hi=1.0/q-0.05,1.0/q+0.05; Oms=np.linspace(lo,hi,N)
    return np.mean([abs(winding(Om,K_r)-1.0/q)<tol for Om in Oms])*(hi-lo)
qs=[2,3,4,5,6]; ws=[width(q) for q in qs]
print("   tongue widths at criticality (a proxy for robustness/detectability):")
for q,w in zip(qs,ws): print(f"     lock 1/{q}: width = {w:.4f}")
print("   count of locks ABOVE a resolution threshold w_thr (= the aliasing, base II):")
for w_thr in [0.050,0.025,0.012,0.006,0.002]:
    cnt=sum(w>w_thr for w in ws); mark="  <-- gives THREE" if cnt==3 else ""
    print(f"     w_thr={w_thr:.3f}: {cnt} detectable lock(s){mark}")
print("   VERDICT: this is a REAL improvement. Instead of 'the hierarchy truncates at three' (arbitrary), it")
print("   says the hierarchy is INFINITE but only locks wider than the resolution threshold (the aliasing =")
print("   base II) are detectable - and a threshold band gives exactly three. It RELOCATES the posit from an")
print("   ad-hoc cutoff to the framework's CORE concept (resolution), and it PREDICTS extra generations existing")
print("   sub-threshold (heavier/undetectable) - consistent with no observed light 4th generation. The residual")
print("   posit shrinks to 'the resolution threshold sits between the 3rd and 4th lock' (a physical calibration,")
print("   not an arbitrary number). The count three is still threshold-dependent (not uniquely forced), but P2")
print("   is now more natural, more unified, and content-ful. Your instinct is right - we upgrade P2.")
