# -*- coding: utf-8 -*-
"""
BST Appendix Stage KG01 — the DYNAMIC geometric route to magnetism (trio test).
Question (open after S23/S24): the static steric comb cannot give like-pole repulsion. Can a
DYNAMIC deformable geometry coupled to flux give the magnetic signature (like-REPEL, opposite-attract,
LONG-range)? Pre-registered controls: scalar geometry vs vorticity structure (S59).

RESULT (honest, functional 2D toy -- NOT a measurement of nature):
  - SCALAR (height-like) deformation, long-range: like-pole ATTRACT (gravity-like sign). NOT magnetism.
  - VORTICITY (S59, flux=circulation, B=curl): like-pole REPEL, opposite attract, range ~1/r = MAGNETIC.
  => the magnetic signature lives in the VECTOR/VORTICITY structure (S59), NOT a scalar geometric
     deformation. This QUALIFIES the route and EXPLAINS the comb's failure (it was scalar-steric, no curl).
  OPEN (sharpened, not closed): the vortex long-range (~1/r velocity far-field) is still the "assumed"
     long-range. Deriving long-range from purely LOCAL rules (the local->nonlocal motif) remains open.
"""
import numpy as np
N=192; L=48.0; dx=L/N
x=(np.arange(N)-N/2)*dx; X,Y=np.meshgrid(x,x,indexing='ij')
k=2*np.pi*np.fft.fftfreq(N,d=dx); KX,KY=np.meshgrid(k,k,indexing='ij'); K2=KX**2+KY**2
def gauss(x0,y0,w=1.2): return np.exp(-((X-x0)**2+(Y-y0)**2)/(2*w**2))

# scalar mediator: (-grad^2+mu^2)h=S ; interaction energy U=-integral(S_A h_B) (source coupling -S*phi)
def Uint_scalar(r,mu,like):
    sB=1.0 if like else -1.0
    hB=np.real(np.fft.ifft2(np.fft.fft2(sB*gauss(r/2,0))/(K2+mu**2)))
    return -float(np.sum(gauss(-r/2,0)*hB)*dx*dx)

# vorticity (S59): two flux tubes (vortices). U_int = integral(v_A . v_B) (kinetic cross term)
def vortex_v(x0,y0,G,core=1.0):
    dX=X-x0; dY=Y-y0; r2=dX**2+dY**2+core**2
    return -G/(2*np.pi)*dY/r2, G/(2*np.pi)*dX/r2
def Uint_vortex(r,like):
    GB=1.0 if like else -1.0
    vAx,vAy=vortex_v(-r/2,0,1.0); vBx,vBy=vortex_v(r/2,0,GB)
    return float(np.sum(vAx*vBx+vAy*vBy)*dx*dx)

rs=[6,9,12,16,20]
fs=lambda U:"REPEL" if (U[-1]-U[0])<0 else "attract"
print("="*70+"\nBST Appendix Stage KG01 -- dynamic geometric route to magnetism\n"+"="*70)
print("\nSCALAR deformable geometry (height), long-range mu=0.12:")
lk=[Uint_scalar(r,0.12,True) for r in rs]; op=[Uint_scalar(r,0.12,False) for r in rs]
print("  U(like):",["%6.2f"%u for u in lk]," => like poles",fs(lk),"(gravity sign)")
print("  U(opp) :",["%6.2f"%u for u in op])
print("\nVORTICITY (S59, flux=circulation):")
lk=[Uint_vortex(r,True) for r in rs]; op=[Uint_vortex(r,False) for r in rs]
sl=np.polyfit(np.log(rs),np.log(np.abs(lk)),1)[0]
print("  U(like):",["%6.3f"%u for u in lk]," => like poles",fs(lk),"(MAGNETIC sign)")
print("  U(opp) :",["%6.3f"%u for u in op]," => opposite",fs(op))
print("  long-range: |U| ~ r^%.2f"%sl)
print("\nVERDICT: magnetic signature (like-repel + long-range) = the VORTICITY/vector structure (S59),")
print("not a scalar geometric deformation (=> gravity sign). Comb failed because scalar-steric (no curl).")
print("OPEN: long-range still from the vortex far-field (assumed), not yet derived from local rules.")
