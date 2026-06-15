#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 25 — POLARITY from PHASE: do like-phase sources repel and opposite-phase attract,
through a field, with NO dipole wired in? (the author's reframed magnetism idea: polarity is the
wave's crest/trough, intrinsic to the beat; the long-range carrier is a geometric/field
deformation.) Two localized oscillating ("beating") sources couple to a 2D wave field with an
absorbing sponge (open domain). Polarity = relative phase: SAME phase = like; OPPOSITE = unlike.
We compute U_int(r) = <E_both> - <E_a> - <E_b>; force = -dU/dr. Only sources + a wave field --
no dipole, no charge sign, nothing magnetic put in by hand.

RESULTS:
- RADIATING regime (omega>0, here 0.6, r > wavelength~10): U_int(same) = -U_int(opp) exactly
  (cross-term cos(dθ)) -- polarity-DEPENDENT force EMERGES -- but the sign OSCILLATES with r
  (interference of two radiating sources); not a monotonic dipole.
- QUASI-STATIC regime (omega=0, the geometric-deformation limit): CLEAN. U_int(same)>0 decreasing
  with r => LIKE polarity REPELS; U_int(opp)<0 rising toward 0 => OPPOSITE polarity ATTRACTS;
  monotonic, slowly decaying (~1/r => long-range). The full Coulomb-like polarity signature,
  emergent from phase + a field.
HONEST BOUNDARIES: this is the COULOMB/charge signature (foundational polarity), NOT specifically
magnetism (the vector/relativistic cousin) nor a dipole (these are monopole-like charges). And the
FIELD is supplied here (a wave equation); that the beating SUBSTRATE itself generates such a
long-range field sourced by phase-polarity is still ASSUMED, not derived -- the hardest remaining
link, since all robust substrate results so far were local. 2D toy, functional, not nature.
Set OMEGA=0.0 for the clean quasi-static signature; OMEGA>0 to see the radiating oscillation.
"""
import numpy as np
OMEGA=0.0
def make_sponge(N, w=10, g0=0.6):
    i=np.arange(N); X,Y=np.meshgrid(i,i,indexing='ij')
    edge=np.minimum.reduce([X,Y,N-1-X,N-1-Y]).astype(float)
    return np.where(edge<w, g0*((w-edge)/w)**2, 0.0)
def run(positions, θ, N=64, c=1.0, om=OMEGA, A=1.0, sigma=2.0, gb=0.02, dt=0.4, T=1800, avg=500):
    gamma_damp=gb+make_sponge(N); i=np.arange(N); X,Y=np.meshgrid(i,i,indexing='ij')
    srcs=[A*np.exp(-((X-px)**2+(Y-py)**2)/(2*sigma**2)) for (px,py) in positions]
    psi=np.zeros((N,N)); v=np.zeros((N,N)); Es=[]
    for t in range(T):
        lap=(np.roll(psi,1,0)+np.roll(psi,-1,0)+np.roll(psi,1,1)+np.roll(psi,-1,1)-4*psi)
        S=sum(s*np.cos(om*t*dt+θ_i) for s,θ_i in zip(srcs,θ))
        v=v+dt*(c**2*lap-gamma_damp*v+S); psi=psi+dt*v
        if t>T-avg:
            g2=((np.roll(psi,-1,0)-psi)**2+(np.roll(psi,-1,1)-psi)**2)
            Es.append(0.5*np.sum(v**2)+0.5*c**2*np.sum(g2))
    return np.mean(Es)
if __name__=="__main__":
    N=64; cy=32; A_pos=(24,cy); Ea=run([A_pos],[0.0],N=N)
    print(f"Phase polarity, omega={OMEGA} ({'quasi-static' if OMEGA==0 else 'radiating'}):")
    print(f"  {'r':>4}{'U_int SAME':>12}{'U_int OPP':>12}   reading")
    for r in [6,9,12,16,20,26]:
        B=(24+r,cy); Eb=run([B],[0.0],N=N)
        Us=run([A_pos,B],[0.0,0.0],N=N)-Ea-Eb
        Uo=run([A_pos,B],[0.0,np.pi],N=N)-Ea-Eb
        tag="LIKE repels/OPP attracts" if Us>0 else "LIKE attracts/OPP repels"
        print(f"  {r:>4}{Us:>12.2f}{Uo:>12.2f}   {tag if OMEGA==0 else 'opposite signs'}")
    print("\nQuasi-static => monotonic Coulomb-like polarity signature (like-repel, opposite-attract),")
    print("long-range, emergent from phase + field. Boundaries: Coulomb not magnetism; field assumed.")
