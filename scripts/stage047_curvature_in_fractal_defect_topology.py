#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 47 — the curvature/spin lives in the (fractal) defect topology, not added to the substrate.
Exploring the user's two ideas for where a spin-2 / curvature comes from: (idea 2) it lives in the
TOPOLOGY of the flux skeletons (the vortex/defect network), and (idea 1) it can traverse the resolutions
along a FRACTAL path. Both are correct and concrete here.

IDEA 2 (exact geometry): a disclination IS a point of Gaussian curvature (S45, the cone). By Gauss-Bonnet
the integral of K over a region = the enclosed sum of deficits, so K = coarse-grained DISCLINATION DENSITY
(Kleinert). Curvature is carried by the defect/flux-skeleton topology, not by the smooth substrate.
IDEA 1 (measured): if the defects are distributed on a FRACTAL (critical, S31) set, the curvature field
is SCALE-INVARIANT -- same structure at every resolution. Curvature power-spectrum slope: FRACTAL (2D
Cantor dust, dim 1.262) = -2.21 (power law, scale-invariant -> traverses resolutions); UNIFORM (Poisson)
= -0.31 (flat/white -> no scale traversal).

HONEST: this is the SOURCE geometry -- WHERE the curvature/spin lives (the fractal flux topology) -- which
the user located correctly, complementing S45 (one defect = exact curvature) and S31 (criticality=fractal).
It is NOT the propagating spin-2 graviton DYNAMICS (S46 boundary stands): the user's idea resolves the
'where', not yet the 'how it propagates'. Slopes are illustrative (depend on smearing/fractal details);
the robust result is the qualitative contrast fractal(power-law) vs uniform(white).
"""
import numpy as np
N=256; rng=np.random.default_rng(0)
def smear(points, sigma=2.0):
    K=np.zeros((N,N))
    for (px,py) in points:
        K[int(px*N)%N,int(py*N)%N]+=1.0
    f=np.fft.fft2(K); kx=np.fft.fftfreq(N); KX,KY=np.meshgrid(kx,kx)
    return np.real(np.fft.ifft2(f*np.exp(-2*(np.pi*sigma)**2*(KX**2+KY**2))))
def cantor_coords(level):
    c=[0.0]
    for k in range(level):
        c=[x for v in c for x in (v, v+2.0/3.0**(k+1))]
    return np.array(c)
cx=cantor_coords(5); pts_fractal=[(x,y) for x in cx for y in cx]
n=len(pts_fractal); pts_uniform=list(zip(rng.random(n),rng.random(n)))
def radial_spectrum(K):
    P=np.abs(np.fft.fft2(K-K.mean()))**2
    ky=np.fft.fftfreq(N)*N; KX,KY=np.meshgrid(ky,ky); kr=np.sqrt(KX**2+KY**2)
    kb=np.arange(2,40); Pr=np.array([P[(kr>=kk)&(kr<kk+1)].mean() for kk in kb]); return kb,Pr
print("="*72); print("BST Stage 47 — curvature lives in the (fractal) defect topology"); print("="*72)
print(f"\n  {n} disclinations.  2D Cantor-dust fractal dim (theory) = {2*np.log(2)/np.log(3):.3f}")
for label,pts in [("FRACTAL (critical/Cantor)",pts_fractal),("UNIFORM (Poisson)",pts_uniform)]:
    kb,Pr=radial_spectrum(smear(pts)); m=(kb>=3)&(kb<=20)&np.isfinite(Pr)&(Pr>0)
    print(f"  {label:>26}: curvature power-spectrum slope = {np.polyfit(np.log(kb[m]),np.log(Pr[m]),1)[0]:+.2f}")
print("\n  Gauss-Bonnet: integral K dA = sum of deficits (curvature = defect density) -- exact geometry.")
print("  => fractal defects -> scale-invariant (power-law) curvature traversing resolutions (idea 1);")
print("  curvature carried by the flux-skeleton TOPOLOGY (idea 2). SOURCE geometry, not graviton dynamics.")
