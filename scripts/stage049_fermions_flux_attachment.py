#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 49 — fermions & spin-1/2 from flux-charge composite vortices (matter sector).
The substrate already has the ingredients: vortices carry a FLUX (circulation, S28/S32/S43) and the
polarity gives them a CHARGE (S25). A charge q transported around a flux Phi picks up the Aharonov-Bohm
phase q*Phi, which is TOPOLOGICAL (holonomy = enclosed flux only; ~0 if not enclosed). The exchange phase
theta = q*Phi/2 sets the statistics; spin = q*Phi/4pi.
RESULT: enclosing-loop holonomy = 2pi exact; non-enclosing ~1e-17. q*Phi/2pi = 0 -> boson; 1/3,1/2 ->
anyons; 1 (one flux quantum attached) -> exchange phase pi = FERMION with spin 1/2 = the spin-statistics
connection, emergent from the substrate's charged vortices.
HONEST RESERVE: this is exactly the standard anyon / flux-attachment / Chern-Simons physics (Wilczek) -- NOT
novel. What the substrate adds: it possesses the charged-vortex composites naturally, so spin-1/2 fermionic
statistics fall out of defect geometry rather than being postulated. NOT closed: the full Dirac equation /
relativistic spinors, the three generations, the Standard-Model fermion content.
"""
import numpy as np

# Fermions / spin-1/2 from flux-charge composite defects (vortices). A charge q transported around a
# vortex of flux Phi picks up the Aharonov-Bohm phase q*Phi (topological). Exchange phase = q*Phi/2.
# Flux attachment (q*Phi = 2pi) -> exchange phase pi -> FERMION; spin = q*Phi/4pi = 1/2 (spin-statistics).
def holonomy(Phi, q, R, x0=0.0, y0=0.0, n=20000):
    # charge q around a circle radius R centered at (x0,y0); vortex flux Phi at origin: A=(Phi/2pi)(-y,x)/r^2
    th=np.linspace(0,2*np.pi,n,endpoint=False); dth=2*np.pi/n
    px=x0+R*np.cos(th); py=y0+R*np.sin(th)
    tx=-R*np.sin(th); ty=R*np.cos(th)                 # tangent * R (dl = (tx,ty) dth)
    r2=px**2+py**2; Ax=(Phi/(2*np.pi))*(-py)/r2; Ay=(Phi/(2*np.pi))*(px)/r2
    return q*np.sum((Ax*tx+Ay*ty)*dth)               # q * closed line integral of A
print("="*72); print("BST Stage 49 — fermions & spin-1/2 from flux-charge composite vortices"); print("="*72)
print("\n  (1) Aharonov-Bohm holonomy is TOPOLOGICAL (only enclosed flux counts):")
print(f"    loop ENCLOSING vortex (R=2): q*Phi measured = {holonomy(2*np.pi,1.0,2.0):.4f}  (= q*Phi = 2pi = {2*np.pi:.4f})")
print(f"    loop NOT enclosing (R=1, centered at (5,0)): = {holonomy(2*np.pi,1.0,1.0,x0=5.0):.4e}  (~0)")
print("\n  (2) exchange phase theta = q*Phi/2 sets the statistics; spin = q*Phi/4pi:")
print(f"  {'q*Phi/2pi':>11}{'theta/pi':>10}{'spin':>8}{'statistics':>14}")
for f in [0.0,1.0/3,0.5,1.0]:
    qPhi=f*2*np.pi; theta=qPhi/2; spin=qPhi/(4*np.pi)
    stat={0.0:'boson',1.0:'FERMION'}.get(f,'anyon')
    print(f"  {f:>11.3f}{theta/np.pi:>10.3f}{spin:>8.3f}{stat:>14}")
print("\n  => flux attachment (q*Phi=2pi, one flux quantum) turns a boson into a FERMION (exchange phase pi)")
print("  with SPIN 1/2 -- the spin-statistics connection, emergent from the substrate's charged vortices.")
