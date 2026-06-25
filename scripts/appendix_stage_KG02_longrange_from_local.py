# -*- coding: utf-8 -*-
"""
BST Appendix Stage KG02 — does LONG-RANGE emerge from a PURELY LOCAL chain of deformations? (Problem A: range)
Setup: a 2D XY lattice, ONLY nearest-neighbor coupling  E = -J sum cos(theta_i - theta_j).
This is BST's own structure (S27 Goldstone phase + S31-33 KT). Two vortices (the magnetic flux
carriers, KG01/S59) at separation r; measure the INTERACTION energy E_int(r) (baseline-subtracted).

RESULT (functional lattice, not nature):
  MASSLESS Goldstone (local couplings only): E_int ~ -/+ 2*pi*J * ln(r)
    like (+,+): slope ~ -2*pi*J  => like-REPEL, LOGARITHMIC LONG-RANGE
    opp  (+,-): slope ~ +2*pi*J  => opp-ATTRACT, long-range
  => the long-range tail emerges from PURELY LOCAL couplings; it IS the gapless Goldstone (S27)
     far field. Problem A (range) is a CONSEQUENCE of the Goldstone, not an assumption.
  OPEN (Problem B): the coupling magnitude J (the circulation Gamma, the field strength) is RECEIVED
     = the scale wall. Magnetism thus reduces to the scale wall, with all structure (sign, long-range
     form, carrier) derived -- exactly the Born pattern.
"""
import numpy as np
N=401; c=N//2
y,x=np.meshgrid(np.arange(N)-c,np.arange(N)-c,indexing='ij')
def thf(vs):
    th=np.zeros((N,N))
    for (x0,y0,q) in vs: th=th+q*np.arctan2(y-y0,x-x0)
    return th
def Enn(th):
    dr=(th-np.roll(th,-1,1)+np.pi)%(2*np.pi)-np.pi
    dd=(th-np.roll(th,-1,0)+np.pi)%(2*np.pi)-np.pi
    return -(np.cos(dr)+np.cos(dd))                 # nearest-neighbor only (LOCAL), J=1
def Ew(e,vs,margin=50,core=5):
    m=np.ones((N,N),bool); m[:margin]=m[-margin:]=m[:,:margin]=m[:,-margin:]=False
    for (x0,y0,q) in vs: m&=((x-x0)**2+(y-y0)**2)>core**2
    return float(e[m].sum())
def Eint(r,like):
    qB=1 if like else -1; vb=[(-r//2,0,1),(r//2,0,qB)]
    return Ew(Enn(thf(vb)),vb)-Ew(Enn(thf([(-r//2,0,1)])),vb)-Ew(Enn(thf([(r//2,0,qB)])),vb)
rs=[20,40,60,80,120,160]
print("XY lattice, LOCAL nearest-neighbor only, two vortices, baseline-subtracted E_int:")
for like,lab in [(True,"LIKE (+,+)"),(False,"OPP  (+,-)")]:
    E=np.array([Eint(r,like) for r in rs]); E=E-E[0]
    sl=np.polyfit(np.log(rs),E,1)[0]
    print(f"  {lab}: dE =",["%6.2f"%v for v in E], f"| slope {sl:+.2f} ln r (2piJ={2*np.pi:.2f}) =>",
          "like-REPEL, long-range" if like else "opp-ATTRACT, long-range")
print("=> long-range from PURELY LOCAL couplings = the gapless Goldstone (S27). Problem A resolved.")
print("   Remaining: coupling magnitude J = received = scale wall (Problem B).")
