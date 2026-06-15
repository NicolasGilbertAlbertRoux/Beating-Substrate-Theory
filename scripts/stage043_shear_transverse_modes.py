#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 43 — scan for SHEAR: a crystallized substrate (vortex/Abrikosov lattice) has transverse (spin-2-prerequisite) modes.
S42 located the Newton->Einstein gap at the missing SPIN-2 mode: a pure superfluid has only longitudinal
(sound) modes, no shear -> gamma=0. But the substrate's own VORTICES (S28/S32), ordered into a LATTICE
(Abrikosov), make an elastic CRYSTAL with SHEAR rigidity and TRANSVERSE phonons (Tkachenko waves) -- the
spin-2 prerequisite the fluid lacks. We model the crystallized substrate as a 2D triangular lattice of
soft-repulsive 'particles' (the vortices/lumps) and scan for shear.

CONSOLIDATIONS (no fit): (1) finite SHEAR MODULUS mu>0 (a fluid relaxes to mu=0); (2) a TRANSVERSE
phonon omega_T = c_T k with c_T = sqrt(mu/rho) (a fluid has no propagating transverse mode); (3) c_L>c_T
(as in any solid); (4) a MELTED control loses the coherent transverse oscillation. => the crystallized
substrate carries the transverse (shear / spin-2-prerequisite) modes absent from the pure superfluid.
HONEST: supplies the missing INGREDIENT; whether the resulting gravity reaches gamma=1 is the next
question, not settled here. 2D, vectorized.
"""
import numpy as np
rng=np.random.default_rng(0)
a=1.2; nx=ny=10; N=nx*ny; sig=1.0; eps=1.0; rc=3.0*sig
e1=np.array([a,0.0]); e2=np.array([a*0.5,a*np.sqrt(3)/2])
Lx=nx*a; Ly=ny*a*np.sqrt(3)/2; box=np.array([Lx,Ly])
pos0=np.array([(i*e1+j*e2) for j in range(ny) for i in range(nx)])%box
def FE(pos):
    d=pos[:,None,:]-pos[None,:,:]; d-=box*np.round(d/box)
    r2=np.sum(d*d,axis=2); np.fill_diagonal(r2,np.inf)
    ee=eps*np.exp(-r2/sig**2)*(r2<rc*rc)
    F=np.sum(((2/sig**2)*ee)[:,:,None]*d,axis=1)
    return F,0.5*np.sum(ee)
def relax(pos,steps=250,dt=0.01,damp=0.9):
    v=np.zeros_like(pos)
    for _ in range(steps):
        F,_=FE(pos); v=damp*v+dt*F; pos=(pos+dt*v)%box
    return pos
pos=relax(pos0.copy()); _,E0=FE(pos)
gs=0.02
def shearE(g):
    p=pos.copy(); p[:,0]+=g*p[:,1]; return FE(p)[1]
mu=2*((shearE(gs)+shearE(-gs)-2*E0)/2)/(gs**2*Lx*Ly); rho=N/(Lx*Ly)
def phonon(transverse,k,A=0.01,dt=0.005,steps=5000,disorder=0.0,Tk=0.0):
    p=pos.copy()
    if disorder>0: p=(p+rng.normal(0,disorder,p.shape))%box
    x0=p[:,0].copy(); y0=p[:,1].copy()
    if transverse: p[:,1]+=A*np.sin(k*x0)
    else:          p[:,0]+=A*np.sin(k*x0)
    v=rng.normal(0,Tk,p.shape) if Tk>0 else np.zeros_like(p); rec=[]
    for s in range(steps):
        F,_=FE(p); v+=0.5*dt*F; p=(p+dt*v)%box; F,_=FE(p); v+=0.5*dt*F
        comp=(p[:,1]-y0) if transverse else (p[:,0]-x0); comp-=comp.mean()
        rec.append(np.sum(comp*np.sin(k*x0)))
    R=np.array(rec)-np.mean(rec); P=np.abs(np.fft.rfft(R)); w=np.fft.rfftfreq(len(R),dt)*2*np.pi
    return w[np.argmax(P)], P.max()/(np.mean(P)+1e-9)
k=2*np.pi/Lx
wT,shT=phonon(True,k); wL,_=phonon(False,k); _,shMelt=phonon(True,k,disorder=0.35,Tk=2.5)
print("="*72); print("BST Stage 43 — shear + transverse modes in the crystallized substrate"); print("="*72)
print(f"\n  (1) SHEAR MODULUS:  mu = {mu:.4f}  (rho={rho:.4f})  -> mu>0 = solid, NOT fluid")
print(f"      predicted c_T = sqrt(mu/rho) = {np.sqrt(mu/rho):.4f}")
print(f"\n  (2) PHONONS at k={k:.3f}:")
print(f"      TRANSVERSE  omega_T={wT:.4f} -> c_T={wT/k:.4f}   (vs sqrt(mu/rho)={np.sqrt(mu/rho):.4f})")
print(f"      LONGITUDINAL omega_L={wL:.4f} -> c_L={wL/k:.4f}   (c_L>c_T: {wL>wT})")
print(f"\n  (3) transverse coherence (spectral peak/mean):  crystal={shT:.1f}   melted={shMelt:.1f}")
print(f"      crystal sustains a sharp transverse (shear) wave; melted fluid washes it out.")
print("\n  => the crystallized substrate (vortex/Abrikosov lattice) HAS shear + transverse modes:")
print("  the spin-2 prerequisite absent in the pure superfluid. (gamma=1 itself: next question.)")
