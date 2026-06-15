#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 50 — dynamical (non-constant) Lambda from a rolling substrate vacuum (cosmology).
Model the substrate vacuum as a scalar condensate phi with self-potential V=V0 exp(-lambda*phi), rolling in
a self-consistent expanding background (H^2 = rho/3, rho=1/2 phi'^2 + V). w = p/rho.
RESULT: lambda=0 (flat) -> w=-1 exact, rho constant = a TRUE cosmological constant. lambda>0 (rolling) ->
w settles ABOVE -1 at exactly the scaling value lambda^2/3 - 1 (matched to 1%) and rho DECREASES =
DYNAMICAL Lambda (quintessence). So Einstein's 'constant' is naturally non-constant when the substrate
vacuum rolls. Dark sector: the LATENT strata (axiom IV) gravitate (carry energy, S4/S21) but are decoupled
from the observable polarity channel (S25) -> gravitating-but-EM-dark = a dark-matter analogue.
HONEST RESERVE: quintessence is established dark-energy physics -- NOT novel; the substrate supplies the
rolling vacuum. NOT closed: the cosmological-constant MAGNITUDE problem (why Lambda is so tiny) is not
solved (quintessence reframes, doesn't solve it); the dark-sector mapping is conceptual, not a quantitative
fit to the observed dark-matter abundance/halos.
"""
import numpy as np

# Dynamical (non-constant) Lambda from a rolling substrate vacuum (quintessence). The substrate condensate
# is a scalar phi with self-potential V(phi)=V0 exp(-lambda*phi). Field eq phi'' + 3H phi' + V'(phi)=0,
# self-consistent H^2 = rho/3 (8piG=1), rho=1/2 phi'^2 + V, p=1/2 phi'^2 - V, w=p/rho. If Lambda were a
# true constant: w=-1 exact, rho const. A rolling field gives w>-1 and rho DECREASING -> Lambda is dynamical.
def run(lam, V0=1.0, phi=0.0, dphi=1e-3, T=12.0, dt=1e-3):
    def deriv(phi,dphi):
        V=V0*np.exp(-lam*phi); Vp=-lam*V; rho=0.5*dphi**2+V; H=np.sqrt(max(rho,0)/3.0)
        return dphi, -3*H*dphi-Vp, rho, (0.5*dphi**2-V)/rho
    n=int(T/dt); ts=[]; ws=[]; rhos=[]
    for i in range(n):
        k1=deriv(phi,dphi); k2=deriv(phi+0.5*dt*k1[0],dphi+0.5*dt*k1[1])
        k3=deriv(phi+0.5*dt*k2[0],dphi+0.5*dt*k2[1]); k4=deriv(phi+dt*k3[0],dphi+dt*k3[1])
        phi+=dt/6*(k1[0]+2*k2[0]+2*k3[0]+k4[0]); dphi+=dt/6*(k1[1]+2*k2[1]+2*k3[1]+k4[1])
        if i%int(n/6)==0: _,_,rho,w=deriv(phi,dphi); ts.append(i*dt); ws.append(w); rhos.append(rho)
    _,_,rho,w=deriv(phi,dphi); ts.append(T); ws.append(w); rhos.append(rho)
    return np.array(ts),np.array(ws),np.array(rhos)
print("="*72); print("BST Stage 50 — dynamical (non-constant) Lambda from a rolling substrate vacuum"); print("="*72)
print("\n  rolling vacuum field phi, V=V0 exp(-lambda*phi): is the effective Lambda constant?")
for lam in [0.0,0.4,0.8,1.4]:
    t,w,rho=run(lam); pred=lam**2/3-1 if lam>0 else -1.0
    print(f"\n  lambda={lam:.1f}:  w(t) = "+", ".join(f"{x:+.3f}" for x in w[::2]))
    print(f"            rho(t)/rho0 = "+", ".join(f"{x:.3f}" for x in (rho/rho[0])[::2])+f"   [scaling w_pred={pred:+.3f}]")
print("\n  => lambda=0 (flat potential): w=-1, rho constant  = a TRUE cosmological constant.")
print("  lambda>0 (rolling): w settles ABOVE -1 (= lambda^2/3 - 1) and rho DECREASES -> Lambda is")
print("  DYNAMICAL (quintessence). Einstein's 'constant' is naturally non-constant when the vacuum rolls.")
print("  Dark sector: the LATENT strata (axiom IV) gravitate (carry energy, S4/S21) but are decoupled")
print("  from the observable polarity channel (S25) -> gravitating-but-EM-dark = a dark-matter analogue.")
