#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 38 — Born is CONSISTENT with the geometric mechanics (checked for no contradiction, not derived).
User's stance: the scale (hbar) may be axiomatic and the Born rule may be ADOPTED from established
physics, provided it does not contradict the framework's geometric mechanics -- which is checkable. We
verify that the density Born uses, rho=|psi|^2, IS the conserved quantity transported by the geometric
flow (phase gradient = the flow, S25-35). Quantum sector (Schrodinger/Madelung, S29): current
j = Im(psi* d_x psi) = rho v with v = d_x S the geometric phase-flow.

CONSOLIDATIONS (hbar=m=1, no fit): (1) total probability conserved to machine precision; (2) continuity
d_t rho + d_x j = 0 pointwise (one-step d_t rho; residual -> discretization: ~1e-3 free, ~1e-2 in a
well); (3) Ehrenfest d<x>/dt = p0/m -- the CONTACT (rho centroid) is carried by the geometric flow.
Free flowing packet AND harmonic well. NOTE: a first run estimated d_t rho over 50 steps (Dt=0.1) ->
inflated residual (5%/57%); fixed with a one-step backward difference.
HONEST: establishes CONSISTENCY (Born density = the conserved flow-density of the geometry); the
stochastic single-outcome postulate (one contact, prob rho) stays ADOPTED, not derived -- which the
user accepts as long as it does not contradict the mechanics (it does not).
"""
import numpy as np
def run(Vfun,p0,x0=-6.0,sig=1.5,L=80.0,N=2048,dt=0.002,steps=3000):
    dx=L/N; x=np.linspace(-L/2,L/2,N,endpoint=False); k=2*np.pi*np.fft.fftfreq(N,d=dx)
    psi=np.exp(-(x-x0)**2/(4*sig**2))*np.exp(1j*p0*x); psi/=np.sqrt(np.sum(np.abs(psi)**2)*dx)
    V=Vfun(x); kin=np.exp(-1j*0.5*k**2*(dt/2))
    norms=[]; xmean=[]; ts=[]; cont=[]; rho_last=np.abs(psi)**2
    for s in range(steps):
        psi=np.fft.ifft(np.fft.fft(psi)*kin); psi=psi*np.exp(-1j*V*dt); psi=np.fft.ifft(np.fft.fft(psi)*kin)
        rho=np.abs(psi)**2
        if s%50==0 and s>0:
            dpsi=np.fft.ifft(1j*k*np.fft.fft(psi)); j=np.imag(np.conj(psi)*dpsi)   # = rho v
            djdx=np.real(np.fft.ifft(1j*k*np.fft.fft(j)))
            drhodt=(rho-rho_last)/dt                                              # one-step d_t rho
            cont.append(np.max(np.abs(drhodt+djdx))/np.max(np.abs(djdx)+1e-12))
            norms.append(np.sum(rho)*dx); xmean.append(np.sum(x*rho)*dx); ts.append(s*dt)
        rho_last=rho
    return np.array(norms),np.polyfit(ts,xmean,1)[0],np.mean(cont),np.max(cont)
print("="*70); print("BST Stage 38 — is the Born density consistent with the geometric flow?"); print("="*70)
print("\n  (1) free flowing packet, p0=1.0  (expected <x> speed = p0/m = 1.0)")
n,sl,cm,cx=run(lambda x:0*x,p0=1.0)
print(f"    total probability: [min,max] = [{n.min():.10f}, {n.max():.10f}]  (conserved)")
print(f"    continuity residual (rel.): mean={cm:.2e}  max={cx:.2e}  (-> discretization)")
print(f"    Ehrenfest d<x>/dt = {sl:.4f}  (predicted p0/m = 1.0)  -- contact carried by the flow")
print("\n  (2) packet in harmonic well V=0.5*x^2, p0=0  (nontrivial oscillating flow)")
n2,sl2,cm2,cx2=run(lambda x:0.5*x**2,p0=0.0)
print(f"    total probability: [min,max] = [{n2.min():.10f}, {n2.max():.10f}]  (conserved)")
print(f"    continuity residual (rel.): mean={cm2:.2e}  max={cx2:.2e}  (-> discretization)")
print("\n  => rho=|psi|^2 is the conserved density carried by the geometric phase-flow.")
print("  Born slots into the geometric mechanics WITHOUT contradiction (consistency, not derivation).")
