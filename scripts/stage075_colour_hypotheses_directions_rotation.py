#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 75 (user: two new hypotheses for colour Z3).
[1] DIRECTIONAL DISPLACEMENT + back-reaction (user's main bet) - the STRONGEST colour lead so far. The 120deg
    rotation about (1,1,1) cyclically permutes the axes x->y->z->x (verified orthogonal, det+1, R^3=I) = Z3.
    The full permutation group of 3 directions is S3 = EXACTLY the Weyl group of SU(3); the cyclic Z3 = EXACTLY
    the centre of SU(3). So three directions carry the precise group skeleton of colour SU(3) (far stronger
    than the beat-phase Z2 idea). HONEST BIND: colour is INTERNAL (commutes with Lorentz; Coleman-Mandula).
    Large spatial dims -> colour spacetime-entangled, contradicts internal (S69). Internal/compact dims ->
    legitimately internal Z3/S3 but positing 3 internal directions = positing colour again. Right SHAPE
    (S3/Z3 = SU(3) skeleton), realisation still relocates the posit; not yet a derivation. Upgrades colour
    from 'fully posited' to 'right group skeleton identified, blocked by the internal-vs-spacetime bind'.
[2] ROTATION (+ counter-rotation) - rotation in a plane is SO(2)/U(1) (continuous, no natural 3); and a
    rotating wave = intrinsic angular momentum = SPIN, already carried by root R1 (grade-2 bivectors ->
    spin-1/2, spin-2). So hypothesis 2 reproduces the SPIN sector, not a new colour Z3; counter-rotation just
    stabilises a limit cycle in the angle. User's instinct to bet less on it is correct.
VERDICT: #1 is the stronger bet and gives the first exact SU(3) group-skeleton echo from a substrate feature,
blocked only by the internal-vs-spacetime bind; #2 lands on spin (R1), not colour.
"""
import numpy as np
print("="*76)
print("BST Stage 75 - two new hypotheses for colour Z3: directional displacement / rotation")
print("="*76)

print("\n[1] DISPLACEMENT through the substrate + directional back-reaction (the user's main bet)")
# the symmetry of the THREE spatial directions: a 120deg rotation about the body diagonal (1,1,1) cyclically
# permutes the axes x->y->z->x. That cyclic permutation is a Z3.
R=np.array([[0,0,1],[1,0,0],[0,1,0]])   # 120deg rotation about (1,1,1)/sqrt3
e=np.eye(3)
print(f"   120deg rotation about (1,1,1): orthogonal={np.allclose(R@R.T,e)}, det={np.linalg.det(R):+.0f}, order: R^3=I? {np.allclose(np.linalg.matrix_power(R,3),e)}")
print(f"   action on axes: x->{['x','y','z'][np.argmax(R@e[:,0])]}, y->{['x','y','z'][np.argmax(R@e[:,1])]}, z->{['x','y','z'][np.argmax(R@e[:,2])]}  (cyclic = Z3)")
print("   GROUP-THEORY ECHO (the real reason this bet is good):")
print("   - the full permutation group of 3 directions is S3 (6 elements).")
print("   - S3 is EXACTLY the WEYL GROUP of SU(3); the cyclic Z3 is EXACTLY the CENTER of SU(3).")
print("   So 'three directions of displacement' carry the precise group skeleton of colour SU(3) - Weyl S3,")
print("   centre Z3. This is a genuine structural echo, far stronger than the beat-phase idea (which was Z2).")
print("   HONEST CAVEAT (the bind): colour is an INTERNAL symmetry (commutes with Lorentz/Poincare). If these")
print("   are the 3 LARGE spatial directions, colour becomes spacetime-entangled -> contradicts colour-as-")
print("   internal (the S69 orthogonality, and Coleman-Mandula). If instead they are 3 INTERNAL/compact")
print("   directions of the substrate, the Z3/S3 is legitimately internal - but positing 3 internal directions")
print("   IS positing the internal structure (colour) in another form. => right SHAPE (S3/Z3 = SU(3) skeleton),")
print("   but the realisation still relocates the posit; it does not yet DERIVE colour. Best lead so far, honestly.")

print("\n[2] ROTATION (+ retroactive counter-rotation) of the primordial waves")
# rotation in a plane = SO(2)/U(1): continuous, no preferred 3-fold. A specific angle gives Z_n for ANY n.
angs=np.array([0,120,240])  # a 3-fold choice would be a POSIT
print(f"   rotation in a plane is SO(2)/U(1): continuous symmetry, no natural 3 (a 120deg choice = Z_n posited).")
print("   moreover, the ROTATION of a wave = intrinsic angular momentum = SPIN, which the framework already")
print("   carries in root R1 (grade-2 bivectors = rotations, giving spin-1/2 and spin-2). So 'rotating waves'")
print("   reproduces the SPIN sector (already in R1), not a new colour Z3. Counter-rotation just stabilises a")
print("   limit cycle in the angle (the spin analogue of the counter-beat). => hypothesis 2 lands on SPIN, not")
print("   colour; it does not give a natural Z3. Your instinct to bet LESS on it is correct.")

print("\nVERDICT")
print("  #1 (directions) is the STRONGER bet, and rightly so: the permutation symmetry of three directions IS")
print("  the SU(3) skeleton (Weyl S3 + centre Z3) - the first time a substrate feature reproduces colour's exact")
print("  group structure. But colour-as-internal forces a choice: large dims (contradicts internal) or internal")
print("  dims (posits colour). The echo is real; the derivation is not closed. #2 (rotation) reproduces SPIN")
print("  (root R1), not colour. So: #1 upgrades the colour problem from 'fully posited' to 'right group skeleton")
print("  identified, blocked only by the internal-vs-spacetime bind' - a sharper, more honest place to stand.")
