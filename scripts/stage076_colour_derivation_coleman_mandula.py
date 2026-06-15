#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 76 (user: attempt to derive colour) - the obstruction is a THEOREM (Coleman-Mandula), not a gap.
Tested the user's refined hypothesis: a directional triplet true at ALL scales (latent & observable). DECISIVE
test: colour must COMMUTE with Lorentz (a red and a green quark have identical spin/mass/kinematics; a rotation
does not change a quark's colour). A directional triplet transforms under rotations (the three axes mix:
x->y, y->-x under a 90deg rotation about z), and being scale-invariant does NOT change this. So a spatial/
geometric triplet CANNOT be the internal colour - Coleman-Mandula (internal symmetry must be a direct product
with Poincare, i.e. commute). The S3/Z3 directional echo (S75) is real but lives in the SPATIAL/SPIN sector
(root R1, which transforms under Lorentz), NOT internal colour. Loopholes: SUSY (adds unobserved superpartners)
or Kaluza-Klein (gauge symmetry from extra COMPACT dimensions separate from the 4 large ones, hence internal) -
the latent can host such compact internal directions but does NOT force them; positing them IS positing colour.
VERDICT: colour cannot be derived from the large spatial directions (a theorem forbids it); it is necessarily
a POSITED internal sector, naturally homed in the latent. We tried and found the obstruction is a theorem, not
a missing step. Honest end of the colour question - stop without regret.
"""
import numpy as np
print("="*76)
print("BST Stage 76 - attempt to DERIVE colour from a directional triplet (incl. scale-invariant)")
print("="*76)
# the user's refined hypothesis: a triplet of directions true at ALL scales (latent & observable), so
# appearing internally and externally. We test whether such a directional triplet can BE colour SU(3).
# DECISIVE TEST: colour must COMMUTE with Lorentz/rotations (a red and a green quark have identical spin,
# mass, kinematics - colour is a rotation SINGLET in how it acts). Does a directional triplet commute?

print("\n[1] does a directional triplet transform under rotations, or stay a singlet?")
axes=np.eye(3)
Rz=np.array([[0,-1,0],[1,0,0],[0,0,1.0]])   # 90deg rotation about z
print("   the three axes x,y,z under a 90deg rotation about z:")
print("   x -> ", Rz@axes[:,0], "  y -> ", Rz@axes[:,1], "  z -> ", Rz@axes[:,2])
mix=np.max(np.abs(Rz@axes-axes))
print(f"   they MIX (max change {mix:.1f}): a 'colour=direction' label would ROTATE with space.")
print("   being 'true at all scales' does NOT change this - a scale-invariant SPATIAL triplet still rotates.")

print("\n[2] what colour actually requires (the decisive constraint):")
print("   colour SU(3) acts on an INTERNAL index and COMMUTES with the Poincare group (Coleman-Mandula):")
print("   a rotation must NOT change a quark's colour. But a directional triplet's label DOES change under")
print("   rotation (step 1). => a spatial/geometric triplet CANNOT be the internal colour. This is a THEOREM")
print("   (Coleman-Mandula: internal symmetry must be a DIRECT PRODUCT with spacetime, i.e. commute), not a")
print("   lack of cleverness on our part.")

print("\n[3] the only loopholes - and why each is still a posit:")
print("   - SUSY (graded algebras) evades Coleman-Mandula, but adds superpartners (not observed at our scale).")
print("   - Kaluza-Klein: gauge symmetry from the isometries of EXTRA COMPACT dimensions that are genuinely")
print("     SEPARATE from the 4 large ones (so they do NOT transform under 4D Lorentz -> legitimately internal).")
print("   The latent can host exactly this: three COMPACT internal directions, decoupled from the 4D rotations.")
print("   But positing three separate compact internal directions IS positing the internal sector (colour).")

print("\nVERDICT (honest, and it closes the colour question as far as it can go)")
print("  Colour CANNOT be derived from the large spatial directions - Coleman-Mandula forbids it (a theorem).")
print("  The triplet-of-directions echo (S3=Weyl, Z3=centre, S75) is real but lives in the SPATIAL/spin sector")
print("  (root R1), which transforms under Lorentz - so it is the rotation/spin structure, NOT internal colour.")
print("  Internal colour must come from a SEPARATE compact sector (Kaluza-Klein-style), which the latent can")
print("  host but does not FORCE. => colour is necessarily a POSITED internal sector, naturally homed in the")
print("  latent. We tried to derive it and found the obstruction is a THEOREM, not a gap. That is the honest")
print("  end: nothing more to extract here without positing - and we can stop without regret.")
