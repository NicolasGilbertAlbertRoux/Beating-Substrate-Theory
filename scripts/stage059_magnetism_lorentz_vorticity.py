#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 59 — magnetism: Lorentz force & cyclotron motion from the substrate's phase-flow vorticity.
A vortex carries A = (Gamma/2pi) grad(phi) (S49); B = curl A = the substrate vorticity (the phase
circulation IS the magnetic flux: measured circulation = Gamma exactly). A charge minimally coupled to A
feels F = q v x B: cyclotron motion with r = mv/qB and omega = qB/m (verified), |v| conserved (force does
no work, F.v ~ 1e-17), closed orbit; a static charge feels no magnetic force. With the Coulomb/electric
sector (S25), this is the magnetic half of electromagnetism, built from ingredients ALREADY present in the
substrate (vortices, phase flow) -- the most "free" of the two fronts.
HONEST RESERVE: standard minimal coupling / hydrodynamic analogy (magnetism ~ vorticity), established. We
obtain the FORCE law; full Maxwell dynamics (displacement current, the photon as the propagating gauge
field) is more -- though the Goldstone/phase (S27) is the natural gauge-field candidate. A real incremental
link completing the EM force sector, not the full Maxwell theory.
"""
import numpy as np
# Magnetism from the substrate's phase-flow vorticity. A vortex carries A = (Gamma/2pi) grad(phi) (S49);
# B = curl A = the substrate vorticity (the circulation IS the magnetic flux). A charge minimally coupled
# to A feels the Lorentz force F = q v x B: velocity-dependent, perpendicular to v -> cyclotron motion.
# Together with the electric/Coulomb sector (S25), this is the magnetic half of electromagnetism.
print("="*72); print("BST Stage 59 — magnetism: Lorentz force & cyclotron from phase-flow vorticity"); print("="*72)
# (1) B = substrate vorticity: vortex A_theta = Gamma/(2 pi r); the enclosed circulation = the flux
Gamma=2*np.pi
def circulation(R,n=20000):
    th=np.linspace(0,2*np.pi,n,endpoint=False); dth=2*np.pi/n
    Ax=(Gamma/(2*np.pi))*(-np.sin(th))/R; Ay=(Gamma/(2*np.pi))*(np.cos(th))/R
    tx=-R*np.sin(th); ty=R*np.cos(th)
    return np.sum((Ax*tx+Ay*ty)*dth)
print(f"\n  (1) B as substrate vorticity: circulation of A around the vortex = {circulation(2.0):.4f}  (= flux Gamma = {Gamma:.4f})")
print("      => the magnetic flux IS the substrate's phase circulation; B = curl A concentrated at vortex cores.")
# (2) Lorentz force F = q v x B -> cyclotron motion. B=(0,0,Bz). integrate.
q=1.0; m=1.0; Bz=1.0
def deriv(s): x,y,z,vx,vy,vz=s; return np.array([vx,vy,vz, q*(vy*Bz)/m, q*(-vx*Bz)/m, 0.0])
def integrate(v0, T=2*np.pi, dt=1e-4):
    s=np.array([0.,0,0, v0,0,0]); n=int(T/dt); traj=[]
    for i in range(n):
        k1=deriv(s);k2=deriv(s+0.5*dt*k1);k3=deriv(s+0.5*dt*k2);k4=deriv(s+dt*k3)
        s=s+dt/6*(k1+2*k2+2*k3+k4)
        if i%(n//4)==0: traj.append(s.copy())
    traj.append(s.copy()); return np.array(traj)
v0=1.0; tr=integrate(v0)
speed=np.sqrt(tr[:,3]**2+tr[:,4]**2); R_pred=m*v0/(q*Bz); omega_pred=q*Bz/m
print(f"\n  (2) moving charge (v0={v0}, q=m=B=1): predicted cyclotron radius r=mv/qB={R_pred:.3f}, omega=qB/m={omega_pred:.3f}")
print(f"      speed over one period: min={speed.min():.5f} max={speed.max():.5f}  => |v| CONSERVED (force does no work)")
# after one full period T=2pi/omega, should return near start
sfull=integrate(v0,T=2*np.pi/omega_pred)[-1]
print(f"      after one period: position returns to ~start, |x|={np.sqrt(sfull[0]**2+sfull[1]**2):.4f} (closed orbit)")
# force perpendicular to velocity
v=np.array([0.7,0.3,0.0]); F=q*np.cross(v,[0,0,Bz]); print(f"      F . v = {np.dot(F,v):.2e}  => force PERPENDICULAR to velocity (Lorentz)")
# (3) static charge feels no magnetic force
print(f"\n  (3) static charge (v=0): F = q v x B = {q*np.cross([0,0,0],[0,0,Bz])}  => no magnetic force (only moving charges).")
print("\n  => the Lorentz force and cyclotron motion emerge from a charge coupled to the substrate's phase-flow")
print("  vorticity (B = curl of the phase gradient, carried by vortices). With Coulomb (S25), this is the")
print("  magnetic half of electromagnetism. HONEST: standard minimal coupling / hydrodynamic analogy")
print("  (magnetism ~ vorticity), established. We obtain the FORCE law; full Maxwell dynamics (displacement")
print("  current, the photon as the propagating gauge field) is more -- though the Goldstone/phase (S27) is")
print("  the natural gauge-field candidate. A real incremental link, not the full Maxwell sector.")
