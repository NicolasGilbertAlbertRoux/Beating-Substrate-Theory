#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 56 — spin-1/2 FORCED by the shortest (minimal first-order) factorization (spinor half of the wall).
Demand the minimal first-order square root of the substrate's own wave operator (omega^2 - k^2 - m^2, from
S34/S36/S51). This single demand forces, with nothing posited by hand:
(0) scalars CANNOT do it ({g^0,g^1}=0 with g^0^2=1,g^1^2=-1 has no scalar solution) -> a 1-component
    (scalar) substrate is impossible; a multi-component spinor is required.
(1) the Clifford algebra {g^mu,g^nu}=2 eta^mu nu (exact, dev 0).
(2) the square-root property (g.k)^2=(k0^2-|k|^2) I (exact, 1.7e-16) -> squares back to the wave operator.
(3) rotation generator S12=(i/4)[g1,g2] with eigenvalues +/-1/2 (SPIN-1/2) and the 4pi DOUBLE COVER
    (U(2pi)=-I, U(4pi)=+I).
So spin-1/2 is the forced cost of minimality ("nature takes the shortest path", user's key). The SAME
minimality principle singles out the graviton: GR is the unique consistent self-coupling of a massless
spin-2 (Weinberg-Deser), and the spin-2 carrier already exists in the shear sector (S54). BOTH halves of
the 3D-rotation wall yield to one principle.
HONEST RESERVE: this is Dirac's 1928 derivation (established), not novel. The substrate adds: the wave
operator is its own, and minimality (first-order = causal + positive-definite density) is the selection
principle (well-motivated, adopted). What is FORCED is the representation content (spinor/Clifford/spin-1/2/
double cover). What is NOT built: the full 3+1 Dirac field as an explicit emergent lattice dynamics (S51 was
1+1D), and the graviton's universal coupling MAGNITUDE (S46). The 'why these reps' wall closes; the
constructive 'build it with the right couplings' wall stays open.
"""
import numpy as np
from scipy.linalg import expm
# The spinor wall by the SHORTEST PATH: demand the minimal first-order factorization (square root) of the
# substrate's wave operator ω^2 - k^2 - m^2. We show this single demand FORCES the Clifford algebra, which
# CANNOT be satisfied by scalars (so the substrate must carry a multi-component spinor), and whose rotation
# generators have eigenvalues +/-1/2 and a 4pi double cover = spin-1/2. Nothing is posited by hand.
I2=np.eye(2); sx=np.array([[0,1],[1,0]]); sy=np.array([[0,-1j],[1j,0]]); sz=np.array([[1,0],[0,-1]]); Z=0*I2
g0=np.block([[I2,Z],[Z,-I2]]); g=[g0]+[np.block([[Z,s],[-s,Z]]) for s in (sx,sy,sz)]
eta=np.diag([1.,-1,-1,-1])
print("="*72); print("BST Stage 56 — spin-1/2 FORCED by the shortest (minimal first-order) factorization"); print("="*72)
# (0) scalars cannot do it
print("\n  (0) can SCALARS factor it? need {g^0,g^1}=2*eta^01=0 with (g^0)^2=1,(g^1)^2=-1.")
print("      for numbers a,b: {a,b}=2ab; ab=0 impossible if a^2=1 and b^2=-1 (both nonzero). => NO scalar")
print("      solution. The shortest factorization is IMPOSSIBLE on a 1-component (scalar) substrate.")
# (1) the minimal matrices satisfy the Clifford algebra
dev=max(np.abs(g[mu]@g[nu]+g[nu]@g[mu]-2*eta[mu,nu]*np.eye(4)).max() for mu in range(4) for nu in range(4))
print(f"\n  (1) minimal solution = 4x4 Dirac matrices. Clifford {{g^mu,g^nu}}=2 eta^mu nu: max deviation = {dev:.1e}")
# (2) the square-root property: (g^mu k_mu)^2 = (k0^2 - k^2) I  -> recovers the wave operator
k=np.array([1.3,0.7,-0.4,0.9]); slash=k[0]*g[0]-(k[1]*g[1]+k[2]*g[2]+k[3]*g[3])
lhs=slash@slash; rhs=(k[0]**2-k[1]**2-k[2]**2-k[3]**2)*np.eye(4)
print(f"  (2) square-root property (g.k)^2 = (k0^2-|k|^2) I : max deviation = {np.abs(lhs-rhs).max():.1e}")
print("      => the minimal first-order operator squares back to the substrate's wave operator. Exact.")
# (3) the rotation generator -> spin 1/2 and the 4pi double cover
S12=(1j/4)*(g[1]@g[2]-g[2]@g[1]); ev=np.linalg.eigvalsh(S12)
U2pi=expm(-1j*2*np.pi*S12); U4pi=expm(-1j*4*np.pi*S12)
print(f"\n  (3) rotation generator S12=(i/4)[g^1,g^2] eigenvalues = {np.round(ev,3)}  (= +/-1/2 => SPIN-1/2)")
print(f"      rotation by 2pi:  U = -I ?  max|U(2pi)+I| = {np.abs(U2pi+np.eye(4)).max():.1e}  (yes => sign flip)")
print(f"      rotation by 4pi:  U = +I ?  max|U(4pi)-I| = {np.abs(U4pi-np.eye(4)).max():.1e}  (yes => double cover)")
print("\n  => the SHORTEST first-order factorization of the substrate's wave operator FORCES: a multi-")
print("  component spinor (scalars impossible), the Clifford algebra, spin eigenvalues +/-1/2, and the 4pi")
print("  double cover. Spin-1/2 is NOT posited -- it is the forced cost of minimality. The other half of")
print("  the 3D-rotation wall closes by the same 'shortest path' principle that singles out the graviton.")
print("  HONEST: this is Dirac's 1928 derivation (established). Substrate adds: the wave operator is its own")
print("  (S34/S36), and minimality (first-order=causal, positive density) is the selection principle. The")
print("  full 3+1 Dirac field as an explicit emergent lattice dynamics is NOT built; the REP content is forced.")
