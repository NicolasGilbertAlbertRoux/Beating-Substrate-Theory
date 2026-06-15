#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 24 — DEFORMABLE combs: does like-pole REPULSION emerge smoothly (no singularity)?
(completes the dipole signature beyond S23's rigid limit.) Each comb is a row of waves connected
to rest positions by ELASTIC springs (so teeth bend/deform instead of overlapping). Inter-comb
interaction is a smooth bounded MORSE law (attraction + soft repulsion, finite at r->0, no
singularity). Everything orientation-blind by construction. We relax both deformable combs at
each face-to-face gap H and report the interaction energy E(H) (Morse + elastic deformation
cost; E(inf)=0).

PRE-REGISTERED: inverse (meshing) -> E develops a NEGATIVE well (smooth attraction); identical
(clashing) -> E stays POSITIVE / rises (smooth REPULSION, the teeth deform apart, no singularity);
flat control -> no orientation dependence. If identical now gives a clean positive (repulsive)
energy while inverse binds, the FULL dipole signature (attract-opposite / repel-like) is
reproduced from geometry+deformation. Honest: 2D toy; still STERIC short-range, not a 1/r^3 field.

RESULT: NEGATIVE (opposite failure mode from rigid S23). All orientations are deeply attractive
(inverse -470, identical -486, flat -466), identical even slightly deeper; orientation-dependence
WASHED OUT (~4% spread). Soft surfaces DEFORM to optimize contact regardless of orientation -- the
teeth "melt" together, killing the geometric distinction; NO repulsion emerges. Combined with S23
(rigid -> differential attraction but only singularity-artifact "repulsion"), the STERIC comb
mechanism does NOT produce the dipole SIGN structure (attract-opposite / repel-like) at either
extreme. DEEP REASON: like-pole repulsion is a long-range FIELD effect, not contact geometry --
steric complementarity can modulate attraction strength but cannot make identical shapes repel at
a distance. The only remaining route for the magnetism idea is the DYNAMIC flux version (like-
polarized flux paths repelling), an extension of S20-S22, not static comb geometry.
"""
import numpy as np
D,a,r0=1.0,2.0,1.0
def comb_rest(n=6, period=2.0, amp=1.0, up=True, offset=0.0, base=0.0, dens=1):
    L=n*period; x=np.linspace(0,L,int(L*dens)); ph=((x-offset)/period)%1.0
    tri=amp*(1-np.abs(2*ph-1)); return np.stack([x,base+(tri if up else -tri)],1)
def relax_E(restA,restB,kel=2.0,gamma_damp=0.6,dt=0.04,T=400):
    A=restA.copy(); B=restB.copy(); VA=np.zeros_like(A); VB=np.zeros_like(B)
    for t in range(T):
        diff=A[:,None,:]-B[None,:,:]; d=np.linalg.norm(diff,axis=2)+1e-9; u=diff/d[:,:,None]
        e=np.exp(-a*(d-r0)); fmag=2*D*a*(1-e)*e
        FA=-(fmag[:,:,None]*u).sum(1)-kel*(A-restA)
        FB=+(fmag[:,:,None]*u).sum(0)-kel*(B-restB)
        VA=(VA+dt*FA)*(1-gamma_damp*dt); VB=(VB+dt*FB)*(1-gamma_damp*dt); A+=dt*VA; B+=dt*VB
    diff=A[:,None,:]-B[None,:,:]; d=np.linalg.norm(diff,axis=2)
    Emorse=(D*((1-np.exp(-a*(d-r0)))**2-1)).sum()
    Eel=0.5*kel*(((A-restA)**2).sum()+((B-restB)**2).sum())
    return Emorse+Eel
def scan(kind):
    A=comb_rest(up=True,base=0.0); best=np.inf; bestH=None
    for H in np.linspace(1.0,5.0,10):
        if kind=="inverse":    B=comb_rest(up=False,base=H,offset=1.0)
        elif kind=="identical": B=comb_rest(up=False,base=H,offset=0.0)
        else:                   B=comb_rest(up=False,base=H,amp=0.0)
        E=relax_E(A,B)
        if E<best: best,bestH=E,H
    # also report E at close approach (H=1.4) to see repulsion
    if kind=="inverse":    Bc=comb_rest(up=False,base=1.4,offset=1.0)
    elif kind=="identical": Bc=comb_rest(up=False,base=1.4,offset=0.0)
    else:                   Bc=comb_rest(up=False,base=1.4,amp=0.0)
    Eclose=relax_E(A,Bc)
    return best,bestH,Eclose
print("="*64); print("BST Stage 24 — deformable combs: smooth repulsion for like poles?"); print("="*64)
print(f"\n  {'config':>12}{'min E':>11}{'gap@min':>9}{'E at close(H=1.4)':>19}   reading")
for kind in ["inverse","identical","flat"]:
    E,H,Ec=scan(kind)
    r={"inverse":"attraction?","identical":"repulsion?","flat":"control"}[kind]
    print(f"  {kind:>12}{E:>11.2f}{H:>9.2f}{Ec:>19.2f}   {r}")
print("\nFull dipole signature iff inverse binds (min E<0) AND identical stays repulsive (E>0,")
print("rising at close approach) -- smoothly, no singularity. Flat = no orientation dependence.")
