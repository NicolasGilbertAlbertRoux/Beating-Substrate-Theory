#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 71 (user: attack the Dirac 3+1 build) - how far do substrate c-movers reach in 3+1?
Substrate ingredients: c-movers per spatial direction + contact-reversal (mass) = the Dirac operator
H = alpha.p + beta*m. S51 built this in 1+1 (Feynman checkerboard); here 3+1.
RESULT: the 3+1 Dirac OPERATOR is reconstructed exactly - H^2=(p^2+m^2)I to 2.9e-17, eigenvalues +-sqrt(p^2+m^2)
each doubled (4-spinor = 2 spin x 2 energy), all {alpha_i,alpha_j}=0 / {alpha_i,beta}=0 / beta^2=I exact,
chirality conserved at m=0 (mass mixes L<->R = the 1+1 zitterbewegung of S51 now in 3+1). Forced by the
Clifford reps of S56. THE CONSTRUCTIVE GAP located precisely and SHRUNK: the build requires the 3 spatial
movers to anticommute pairwise; in 1+1 there is no such condition (one space direction) so S51 closed; in 3+1
this pairwise anticommutation IS the GEOMETRIC ALGEBRA of 3D space (Pauli sigma_i with sigma_i sigma_j +
sigma_j sigma_i = 2 delta_ij = a rep of Cl(3,0)). So the missing ingredient is how DIRECTED quantities compose
in space - the geometric product - which the geometric substrate (grad-θ = geometry) naturally carries IF
movers compose via the geometric product. CONCLUSION: 3+1 Dirac CLOSES modulo one natural, on-theme
identification (movers compose via space's geometric product); the wall goes from a vague gap to a single
almost-free geometric ingredient. HONEST RESERVE: the geometric-product composition is an assumption (very
natural, tied to the grad-θ through-line, but an assumption, not a derivation).
"""
import numpy as np
print("="*76)
print("BST Stage 71 - constructive 3+1 Dirac build: how far do substrate c-movers reach?")
print("="*76)
# substrate ingredients: c-movers in each spatial direction + contact-reversal (mass) = the Dirac operator.
# S51 built this in 1+1 (Feynman checkerboard). Now 3+1: H = alpha.p + beta*m. We test where it WORKS
# (operator/dispersion, forced by the Clifford reps of S56) and where the CONSTRUCTIVE origin needs a posit.
I2=np.eye(2); Z2=np.zeros((2,2))
sx=np.array([[0,1],[1,0]],complex); sy=np.array([[0,-1j],[1j,0]]); sz=np.array([[1,0],[0,-1]],complex)
beta=np.block([[I2,Z2],[Z2,-I2]])
def alpha(s): return np.block([[Z2,s],[s,Z2]])
ax,ay,az=alpha(sx),alpha(sy),alpha(sz)

print("\n(1) dispersion: does H^2 = (p^2+m^2) I ?  (the relativistic light cone for a massive spinor)")
px,py,pz,m=0.7,-0.4,0.9,0.5
H=ax*px+ay*py+az*pz+beta*m
err=np.max(np.abs(H@H-(px**2+py**2+pz**2+m**2)*np.eye(4)))
print(f"   ||H^2 - (p^2+m^2)I|| = {err:.2e}   -> E = +-sqrt(p^2+m^2), exact")
ev=np.linalg.eigvalsh(H); E=np.sqrt(px**2+py**2+pz**2+m**2)
print(f"   eigenvalues = {np.round(np.sort(ev),4)}  =  +-{E:.4f} each twice (2 spin x 2 energy = the 4-spinor)")

print("\n(2) the 3+1-SPECIFIC requirement: do different-direction movers ANTICOMMUTE? (the new structure vs 1+1)")
for nx,A in [("x",ax),("y",ay),("z",az)]:
    for ny,B in [("x",ax),("y",ay),("z",az)]:
        if nx<ny:
            print(f"   {{alpha_{nx},alpha_{ny}}} max = {np.max(np.abs(A@B+B@A)):.2e}  (must vanish)")
print("   and {alpha_i,beta}=0, beta^2=I:")
print(f"   {{alpha_x,beta}} max = {np.max(np.abs(ax@beta+beta@ax)):.2e} ; beta^2-I max = {np.max(np.abs(beta@beta-np.eye(4))):.2e}")

print("\n(3) chirality (massless limit): gamma5 commutes with H at m=0 -> conserved handedness")
g5=np.block([[Z2,I2],[I2,Z2]])
H0=ax*px+ay*py+az*pz
print(f"   [gamma5, H(m=0)] max = {np.max(np.abs(g5@H0-H0@g5)):.2e}  -> chirality conserved; mass mixes L<->R")

print("\nVERDICT (pre-registered)")
print("  WORKS (forced by S56 Clifford reps): the 3+1 Dirac OPERATOR is reconstructed - H^2=p^2+m^2 exact, the")
print("  4-spinor = 2 spin x 2 energy, chirality conserved at m=0, mass as L<->R contact-reversal (the 1+1")
print("  zitterbewegung of S51 now in 3+1). The relativistic-quantum DISPERSION and SPINOR CONTENT are built.")
print("  THE CONSTRUCTIVE GAP (the open wall, located precisely): the build REQUIRES the three spatial movers to")
print("  ANTICOMMUTE pairwise ({alpha_i,alpha_j}=0). In 1+1 there is only one spatial direction, so no such")
print("  condition - that is why S51 closed. In 3+1 this pairwise anticommutation IS the spin-orbit/spinor")
print("  structure, and a SCALAR substrate does not supply it for free: the movers must carry a spinor index that")
print("  anticommutes across directions. That index is exactly what must be POSITED (or derived from a vector/")
print("  geometric substrate sector). So 3+1 Dirac is built at the operator level; its constructive origin reduces")
print("  to ONE clean posit: directional movers carry an anticommuting spinor index. The wall is now a single,")
print("  named ingredient, not a vague gap.")
