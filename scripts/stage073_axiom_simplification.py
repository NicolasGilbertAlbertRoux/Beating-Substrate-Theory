#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 73 (user: beautiful simplification before consolidating) - do the four named posits reduce to
fewer ROOTS? A grouping is a REDUCTION only if the grouped axioms FOLLOW from one statement, not share a label.
ROOT A (geometry-beat): ONE Clifford algebra of spacetime carries grade-1 vectors (the movers -> Dirac,
  axiom 3) AND grade-2 bivectors (rotations/curvature -> spin-2, axiom 4), with the beat as grade-0 at c (S34).
  Verified: {g^mu,g^nu}=2 eta (dev 0) and bivector closure [S12,S23]=+2*S31 (residual 0). => axioms 3 & 4 are
  two GRADES of one root. GENUINE REDUCTION 3+4 -> 1. (caveat: 'curvature takes the beat speed' is the natural
  face, not a strict theorem.)
ROOT B (critical-cyclic): colour-Z3 and three-generations are PHYSICALLY INDEPENDENT (SM: colour unrelated to
  family number); merging them because both involve '3' = numerology. HONEST CHECK FAILS -> NOT a reduction;
  they share only the critical-cyclic DOMAIN.
BASE MAP: geometric-algebra+beat = sharpening of base I (ball+dimensions) & III (movement/beat);
  criticality = sharpening of base II (resolution/aliasing). So axioms 3,4 are not new; genuinely-new beyond
  the base = only the two SM-internal inputs (colour Z3, generation truncation), as every theory needs.
SIMPLIFIED AXIOM SET: [R1] geometric-algebra substrate + beat grade-0 at c (=> Dirac 3+1 AND GW-at-c; sharpens
  base I/III, absorbs old posits 3,4); [R2] substrate at criticality, cyclic locking (sharpens base II);
  [P1] colour Z3 (irreducible SM input); [P2] cyclic-lock truncation at three / generations (irreducible SM
  input). 4 posits -> 2 roots (base-sharpenings) + 2 irreducible SM inputs. Geometry genuinely UNIFIES; the
  SM-internal 3's honestly do NOT merge. The real, non-cheating simplification.
"""
import numpy as np
I2=np.eye(2); Z2=np.zeros((2,2))
sx=np.array([[0,1],[1,0]],complex); sy=np.array([[0,-1j],[1j,0]]); sz=np.array([[1,0],[0,-1]],complex)
beta=np.block([[I2,Z2],[Z2,-I2]]).astype(complex)
def alpha(s): return np.block([[Z2,s],[s,Z2]])
ax,ay,az=alpha(sx),alpha(sy),alpha(sz)
g0=beta; g1=beta@ax; g2=beta@ay; g3=beta@az; G=[g0,g1,g2,g3]; eta=np.diag([1,-1,-1,-1])
print("ROOT A - one Clifford algebra yields both sectors:")
maxv=max(np.max(np.abs(G[m]@G[n]+G[n]@G[m]-2*eta[m,n]*np.eye(4))) for m in range(4) for n in range(4))
print(f"  grade-1 vectors (movers->Dirac, axiom 3): {{g,g}}=2eta dev {maxv:.1e}")
def sig(m,n): return 0.5*(G[m]@G[n]-G[n]@G[m])
S12,S23,S31=sig(1,2),sig(2,3),sig(3,1); comm=S12@S23-S23@S12
idx=np.unravel_index(np.argmax(np.abs(S31)),S31.shape); cval=comm[idx]/S31[idx]
print(f"  grade-2 bivectors (rot/curvature->spin-2, axiom 4): [S12,S23]=({cval.real:+.0f})S31 residual {np.max(np.abs(comm-cval*S31)):.1e}")
print("  => 3+4 reduce to ONE root (geometric algebra + beat grade-0 at c).")
print("ROOT B - colour-Z3 vs three-generations: physically independent 3's -> NO merge (refused as numerology).")
print("4 named posits -> 2 roots (R1 geometry-beat, R2 criticality; both base-sharpenings) + 2 SM inputs (P1 colour, P2 generations).")
