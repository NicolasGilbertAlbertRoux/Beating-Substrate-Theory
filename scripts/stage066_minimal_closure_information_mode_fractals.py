#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 66 (user: do all three) - three PRE-REGISTERED probes toward internal structure, with the null
expected and reported for each.
(A) MINIMAL CLOSURE: smallest structure admitting a 2-dim spinor (double cover) = SU(2); adding chirality
    (complex reps) needs U(1) or SU(N>=3) -> minimality reaches SU(2)xU(1) (electroweak SIZE). Color N and
    the number of generations are FREE (SU(2)<SU(3); nothing forces replication). PRE-REG NULL HOLDS.
(B) latent reconstruction controls: entanglement entropy of a critical free-fermion chain (correlation-
    matrix method) -> S=(c/3)ln l + const, fitted c=1.000 (exact free-boson/superfluid value). latent reconstruction information
    = forced central charge / area-law, holographic-consistent (S64). c~1, NOT 3. PRE-REG NULL HOLDS.
(C) FRACTALS tuned to ALL our modes (η=1/4, jump 2/pi, 1/2, G_eff,...): Hausdorff d=lnN/ln(1/r). Branch
    number N is FREE, dims are generic reals; no construction forces d=3 or N=3. One entry lands at 3.07 only
    because N=4 was CHOSEN - the numerology trap, NOT a signal. PRE-REG NULL HOLDS (honestly, it was nothing).
VERDICT: all three nulls hold. Real & forced: minimal chiral-spinor SIZE (SU(2)xU(1)); latent reconstruction information = forced
central charge / area law. NOT forced: color SU(3), three generations, a fractal '3'. The gain is a MAP of
exactly where minimality and self-similar information reach and where they stop. SM numbers = still the wall.
"""
import numpy as np
print("="*76)
print("BST Stage 66 - three pre-registered probes: minimal closure / latent reconstruction information / mode-tuned fractals")
print("="*76)

# ---------- (A) MINIMAL CLOSURE: what does 'admit spinors + chirality + close' force? ----------
print("\n(A) MINIMAL CLOSURE  (does the shortest path force a gauge group?)")
# facts (rep theory): smallest faithful irrep dim, and whether the group has COMPLEX (chiral) irreps
groups = [("U(1)",1,1,"abelian",True),      # 1-dim reps, complex -> chirality yes, but no spinor double cover
          ("SU(2)",3,2,"rank1",False),       # smallest spinor (2-dim, double cover) ; reps pseudo-REAL -> no chirality alone
          ("SU(3)",8,3,"rank2",True),        # smallest SU(N) with complex reps + triality (Z3 center)
          ("SU(4)",15,4,"rank3",True)]
print(f"  {'group':>6}{'dim':>5}{'min spinor rep':>16}{'complex(chiral)?':>18}")
for g,dim,sp,_,cx in groups:
    print(f"  {g:>6}{dim:>5}{sp:>16}{('yes' if cx else 'no'):>18}")
print("  minimal structure admitting a 2-dim SPINOR (double cover) = SU(2); adding CHIRALITY (complex reps)")
print("  needs U(1) or SU(N>=3). => minimality reaches SU(2)xU(1) (electroweak SIZE). Color N and the NUMBER")
print("  of generations are FREE: SU(2) is smaller than SU(3), and nothing forces replication. PRE-REG NULL HOLDS.")

# ---------- (B) latent reconstruction information across the self-similar tower (free-fermion entanglement) ----------
print("\n(B) latent reconstruction controls: how does information scale across the latent tower?")
N=400; kF=np.pi/2
idx=np.arange(N)
def Cmat(n):
    i=np.arange(n)[:,None]; j=np.arange(n)[None,:]; d=i-j
    with np.errstate(divide='ignore',invalid='ignore'):
        C=np.sin(kF*d)/(np.pi*d); C[d==0]=0.5
    return C
def S_block(l):
    nu=np.linalg.eigvalsh(Cmat(l)); nu=np.clip(nu,1e-12,1-1e-12)
    return -np.sum(nu*np.log(nu)+(1-nu)*np.log(1-nu))
ls=np.array([10,20,40,80,160]); S=np.array([S_block(l) for l in ls])
# critical chain: S = (c/3) ln(l) + const ; fit slope -> c
slope,icpt=np.polyfit(np.log(ls),S,1); c=3*slope
print(f"  block sizes l = {list(ls)}")
print(f"  entropies   S = {[round(s,3) for s in S]}")
print(f"  fit S = (c/3)ln l + b  ->  c = {c:.3f}  (free-boson/superfluid fixed point: exact c=1)")
print("  => latent reconstruction information obeys a LOG/AREA law set by the central charge c (a FORCED fixed-point invariant),")
print("  consistent with the holographic dark-energy reframing (S64). c ~ 1, NOT 3. PRE-REG NULL HOLDS.")

# ---------- (C) FRACTALS TUNED TO OUR MODES (all of them) ----------
print("\n(C) FRACTALS tuned to our established modes - does any force the integer 3?")
modes={"KT η=1/4":0.25,"NK jump 2/pi":2/np.pi,"de Broglie c^2 recip":0.5,
       "spin-1/2 (1/2)":0.5,"helicity-2 (1/2 of 2pi)":0.5,"G_eff lambda^2/4pi @ lambda=1":1/(4*np.pi)}
print(f"  Hausdorff dim d = ln(N)/ln(1/r) for N branches at contraction r=mode:")
print(f"  {'mode (r)':>26}{'N=2':>8}{'N=3':>8}{'N=4':>8}")
for name,r in modes.items():
    if r>=1 or r<=0: continue
    ds=[np.log(N)/np.log(1/r) for N in (2,3,4)]
    print(f"  {name:>20} ({r:>4.3f}){ds[0]:>8.3f}{ds[1]:>8.3f}{ds[2]:>8.3f}")
print("  the branch number N is a FREE choice and the dims are generic reals; no construction FORCES d=3 or")
print("  N=3 from the modes alone. A '3' here would be cherry-picked. PRE-REG NULL HOLDS - it was, honestly, nothing.")

print("\nVERDICT: all three pre-registered NULLS hold. Real & forced: minimal chiral-spinor SIZE (SU(2)xU(1)),")
print("latent reconstruction information = forced central charge / area law (holographic-consistent). NOT forced by any probe:")
print("color SU(3), three generations, or a fractal that singles out '3'. The SM-specific numbers remain the wall;")
print("the honest gain is mapping exactly WHERE minimality and self-similar information reach, and where they stop.")
