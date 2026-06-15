#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 35 — analog gravity: a FLOWING superfluid tilts the cone (acoustic metric); v>c => horizon.
The substrate's superfluid (S33) has a rest frame; a background FLOW v tilts the cone its excitations
feel (Unruh/Volovik acoustic metric) -- effective curved spacetime -> geometry->gravity, mirroring
geometry->quantum. We time-evolve Gross-Pitaevskii (hbar=m=1) with a uniformly flowing condensate
psi0=sqrt(rho0)exp(i v x), seed a small density ripple at k, and extract the two Bogoliubov branches
omega_+/- (parabolic sub-bin interpolation for accuracy).

PRE-REGISTERED & CONFIRMED: rest branch Omega=sqrt(c^2 k^2 + (k^2/2)^2), c=sqrt(g rho0)=1; lab branches
omega_+/- = v*k +/- Omega (TILTED CONE). CONSOLIDATIONS (no free parameter): |(omega_++omega_-)/2k| =
imposed flow v (tilt = flow), and (omega_+ - omega_-)/2 = Bogoliubov Omega(k). v<c: branches OPPOSITE
sign (waves both ways). v>c: SAME sign => no upstream propagation => HORIZON (sonic black hole).
DERIVED not chosen: the acoustic metric emerges from linearizing GP around a flow.

HONEST BOUNDARY: this is KINEMATIC analog gravity (curved-spacetime propagation + horizons), NOT
dynamical Einstein gravity -- the acoustic metric does not obey G_mu_nu = 8 pi T_mu_nu (mass does not
source curvature here). This is the hard limit of ALL analog-gravity programs, not specific to BST.
The quantum<->gravity bridge holds at the kinematic level; Einstein dynamics is not derived. 1D, PBC.
"""
import numpy as np
def bogo(kf_t,k_t,N=1024,L=160.0,g=1.0,rho0=1.0,dt=0.005,steps=24000,eps=0.008):
    x=np.linspace(0,L,N,endpoint=False); dx=L/N
    kg=2*np.pi*np.fft.fftfreq(N,d=dx)
    nf=round(kf_t*L/(2*np.pi)); kf=2*np.pi*nf/L          # quantize flow to ring
    nk=round(k_t*L/(2*np.pi));  k =2*np.pi*nk/L           # quantize probe to ring
    psi=np.sqrt(rho0)*np.exp(1j*kf*x)*(1+eps*np.cos(k*x))
    half=np.exp(-1j*0.5*kg**2*(dt/2)); rec=[]
    for s in range(steps):
        psi=np.fft.ifft(np.fft.fft(psi)*half)
        psi=psi*np.exp(-1j*g*np.abs(psi)**2*dt)
        psi=np.fft.ifft(np.fft.fft(psi)*half)
        rec.append(np.sum((np.abs(psi)**2-rho0)*np.exp(-1j*k*x)))
    A=np.array(rec); A=A-A.mean()
    w=np.fft.fftfreq(len(A),dt)*2*np.pi; P=np.abs(np.fft.fft(A)); df=2*np.pi/(len(A)*dt)
    def refine(i):
        i0=i%len(P); a,b,cc=P[(i0-1)%len(P)],P[i0],P[(i0+1)%len(P)]; den=(a-2*b+cc)
        return w[i0]+(0.5*(a-cc)/den if den!=0 else 0.0)*df
    order=np.argsort(P)[::-1]; peaks=[]
    for idx in order:
        if all(abs(w[idx]-w[j])>2*df for j in peaks): peaks.append(idx)
        if len(peaks)==2: break
    f=sorted([refine(peaks[0]),refine(peaks[1])],reverse=True); return kf,k,f[0],f[1]
print("="*80); print("BST Stage 35 — does a flowing superfluid tilt the cone? (analog gravity)"); print("="*80)
print("\n  c=sqrt(g*rho0)=1.  Predicted: omega_+/- = v*k +/- sqrt(c^2 k^2 + (k^2/2)^2).")
for kf_t,lab in [(0.0,"v=0   (rest: cone symmetric)"),
                 (0.5,"v=0.5 < c (sub-sonic: cone tilts)"),
                 (1.5,"v=1.5 > c (supersonic: HORIZON)")]:
    print(f"\n  --- {lab} ---")
    print(f"  {'k':>7}{'w_+':>9}{'w_-':>9}{'|v_meas|':>11}{'Om_meas':>10}{'Om_pred':>10}{'  branch signs'}")
    for k_t in [0.39,0.79]:
        kf,k,wp,wm=bogo(kf_t,k_t)
        vmeas=abs((wp+wm)/(2*k)); Om=(wp-wm)/2; Omp=np.sqrt(k**2+(k**2/2)**2)
        signs="opposite (both ways)" if wp*wm<0 else "SAME -> HORIZON"
        print(f"  {k:>7.3f}{wp:>9.4f}{wm:>9.4f}{vmeas:>11.4f}{Om:>10.4f}{Omp:>10.4f}   {signs}")
print("\n  CONSOLIDATION: |v_meas| = imposed flow (tilt=flow, no fit); Om_meas = Bogoliubov Om_pred.")
print("  v>c => both branches same sign => no upstream propagation => sonic horizon.")
print("  BOUNDARY: kinematic analog gravity only; NOT Einstein dynamics (no G=8piT).")
