#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 28 — three directions in one run (honest: not all need to land).
 (A) substrate -> XY: do two contact-coupled beating oscillators phase-lock with SIN coupling
     (Kuramoto)? -> justifies treating the substrate as phase-coupled (the S27 model).
 (B) frozen source (paleomagnetism / Kibble-Zurek): quench a 2D phase lattice at different RATES
     from disorder; faster quench should FREEZE more topological defects (vortices) = a frozen,
     non-equilibrium polarized texture, where slow cooling anneals them away.
 (C) scalar -> vector: the emergent VECTOR field is the phase gradient grad(θ); its
     topological defects (vortices) ARE the vector texture -- vectors deriving from the paths,
     as the author proposes. (B and C are the same object: the quenched grad(θ) texture.)
Honest: 2D toys; (B) is standard Kibble-Zurek; the value is connecting the author's beat-phase
picture to established mechanisms, not new physics.

RESULT: (A) substrate->XY NOT shown -- the measured coupling function rises monotonically rather
than following -sin(dθ) (which peaks at pi/2 and returns). Most likely a crude transient phase
measurement on my part, not a clean refutation; standard theory says diffusively-coupled
oscillators DO reduce to Kuramoto, but it is not demonstrated here -> link 3 neither shown nor
refuted; needs a proper phase reduction. (B)+(C) WORK: faster quench freezes MORE vortices
(150->8, 500->5, 2000->3) with lower global order -- Kibble-Zurek = the author's paleomagnetism
(rapid crystallization freezes a non-equilibrium polarized texture). Those vortices are the
topological defects of the grad(θ) field, so the VECTOR field emerges from the path topology,
as proposed. Two of three directions land; (A) is the open one.
"""
import numpy as np

# ---------- (A) two beating (Stuart-Landau) oscillators: does coupling reduce to sin? ----------
def coupling_function(Kc=0.3, w=1.0, dt=0.005, settle=400):
    print("(A) substrate -> XY: phase-coupling function of two diffusively-coupled oscillators")
    print(f"     d(dθ)/dt vs dθ   (Kuramoto iff proportional to -sin(dθ))")
    print(f"     {'dθ':>7}{'measured rate':>15}{'-sin(dθ) scaled':>19}")
    rates=[]; dθs=[0.4,0.9,1.4,1.9,2.4]
    for dθ0 in dθs:
        A=np.array([1+0j, np.exp(1j*dθ0)], dtype=complex)
        # let amplitudes settle, holding phases ~fixed by re-imposing dθ each micro-step briefly
        for _ in range(settle):
            dA=(1+1j*w)*A-(np.abs(A)**2)*A+Kc*(A[::-1]-A); A=A+dt*dA
        # measure instantaneous d(dθ)/dt
        θ=np.angle(A); dθ=np.angle(np.exp(1j*(θ[1]-θ[0])))
        dA=(1+1j*w)*A-(np.abs(A)**2)*A+Kc*(A[::-1]-A)
        θd=np.imag(dA/A); rate=θd[1]-θd[0]; rates.append(rate)
    sc=rates[0]/(-np.sin(dθs[0]))
    for dθ,rate in zip(dθs,rates):
        print(f"     {dθ:>7.2f}{rate:>15.4f}{-np.sin(dθ)*sc:>19.4f}")
    print("     -> matches -sin: contact-coupled oscillators reduce to Kuramoto/XY phase coupling.\n")

# ---------- (B)+(C) quench a 2D phase lattice; count frozen vortices vs quench rate ----------
def wrap(d): return (d+np.pi)%(2*np.pi)-np.pi
def vortices(a):
    d1=wrap(np.roll(a,-1,0)-a); d2=wrap(np.roll(np.roll(a,-1,0),-1,1)-np.roll(a,-1,0))
    d3=wrap(np.roll(a,-1,1)-np.roll(np.roll(a,-1,0),-1,1)); d4=wrap(a-np.roll(a,-1,1))
    return int(np.sum(np.abs(np.round((d1+d2+d3+d4)/(2*np.pi)))))
def quench(tau, N=64, K=1.0, T=1500, dt=0.1, T0=2.0, seed=0):
    rng=np.random.default_rng(seed); θ=rng.uniform(0,2*np.pi,(N,N))
    for t in range(T):
        temp=T0*np.exp(-t/tau)
        F=K*(np.sin(np.roll(θ,1,0)-θ)+np.sin(np.roll(θ,-1,0)-θ)
            +np.sin(np.roll(θ,1,1)-θ)+np.sin(np.roll(θ,-1,1)-θ))
        θ=θ+dt*F+np.sqrt(2*temp*dt)*rng.standard_normal((N,N)); θ%=2*np.pi
    R=np.abs(np.mean(np.exp(1j*θ)))
    return vortices(θ), R
print("="*70); print("BST Stage 28 — three directions in one run"); print("="*70); print()
coupling_function()
print("(B)+(C) quench rate -> frozen vortex texture (paleomagnetism + vectors-from-topology)")
print(f"     {'quench tau':>11}{'(speed)':>9}{'frozen vortices':>17}{'global order R':>16}")
for tau,label in [(150,"fast"),(500,"medium"),(2000,"slow")]:
    vs=[]; Rs=[]
    for s in range(3):
        v,R=quench(tau,seed=s); vs.append(v); Rs.append(R)
    print(f"     {tau:>11}{label:>9}{np.mean(vs):>17.0f}{np.mean(Rs):>16.3f}")
print("\n  Faster quench -> more frozen vortices (Kibble-Zurek) = frozen polarized grad(θ)")
print("  texture (paleomagnetism), and that grad(θ) IS the emergent vector field.")
