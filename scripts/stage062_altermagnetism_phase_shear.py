#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 62 (lead 2) — three magnetic orders incl. altermagnetism (2024) from phase + crystal shear.
H(k)=eps(k) I + Delta(k) s_z. Ferro: Delta const (s-wave, net M). Antiferro: Delta=0 (M=0, degenerate).
Altermagnet: Delta = Delta_AM (cos kx - cos ky) (d-wave) -> net M=0 BUT spin-split bands with the sign
reversal Delta(pi/2,0) = -Delta(0,pi/2) -- the 2024 signature. The d-wave term is the staggered phase order
COUPLED to the crystal shear anisotropy: cos kx - cos ky IS the spin-2 traceless symmetry (S43/S54). So the
substrate carries all THREE magnetic orders, the third (altermagnetism, experimentally confirmed 2024) for
free from its existing phase + shear sectors.
HONEST RESERVE: standard altermagnet model (established 2024); substrate supplies the ingredients, nothing
novel. It does NOT explain the Standard-Model gauge groups or the three fermion generations -- magnetic-order
classification (Landau symmetry breaking) is unrelated to SU(3)xSU(2)xU(1) or generations; "3 orders <-> 3
generations" is numerology unless forced. NULL on gauge groups/generations; genuine POSITIVE on altermagnetism.
"""
import numpy as np
# Lead 2: does the substrate naturally produce the THREE magnetic orders, incl. altermagnetism (2024)?
# Minimal model H(k)=eps(k) I + Delta(k) s_z. Ferro: Delta=const (s-wave, net M). Antiferro: Delta=0
# (staggered -> spin-degenerate, M=0). Altermagnet: Delta=Delta_AM (cos kx - cos ky) (d-wave) -> M=0 but
# spin-split bands. The d-wave term is the staggered phase order COUPLED to the crystal shear anisotropy
# (the spin-2 traceless structure, S43/S54): cos kx - cos ky is exactly the d-wave/shear symmetry.
n=200; kx=np.linspace(-np.pi,np.pi,n); KX,KY=np.meshgrid(kx,kx)
def splitting(kind):
    if kind=="ferro":    return np.full_like(KX,0.4)             # s-wave: constant
    if kind=="antiferro":return np.zeros_like(KX)                # degenerate
    if kind=="alter":    return 0.4*(np.cos(KX)-np.cos(KY))      # d-wave (shear/spin-2 symmetry)
print("="*72); print("BST Stage 62 — three magnetic orders incl. altermagnetism from phase + crystal shear"); print("="*72)
print(f"\n  spin splitting Delta(k) = E_up - E_down over the Brillouin zone:")
print(f"  {'order':>12}{'net M = <Delta>':>18}{'spin-split? var':>18}{'Delta(pi/2,0)':>15}{'Delta(0,pi/2)':>15}")
ihalf=np.argmin(np.abs(kx-np.pi/2)); izero=np.argmin(np.abs(kx-0))
for kind in ["ferro","antiferro","alter"]:
    D=splitting(kind); M=D.mean(); var=D.var()
    d1=D[izero,ihalf]; d2=D[ihalf,izero]
    print(f"  {kind:>12}{M:>18.4f}{var:>18.4f}{d1:>15.3f}{d2:>15.3f}")
print("\n  => ferro: net M != 0, splitting constant (s-wave).  antiferro: M=0, no splitting.")
print("     altermagnet: net M = 0 (mean splitting zero) BUT bands ARE spin-split (variance>0), with the")
print("     d-wave sign reversal Delta(pi/2,0) = -Delta(0,pi/2) -- the 2024 signature. It arises from the")
print("     staggered phase order coupled to the crystal SHEAR anisotropy (cos kx - cos ky = the spin-2")
print("     traceless symmetry, S43/S54). The substrate carries all THREE orders, the third for free.")
print("\n  HONEST: this is the standard altermagnet model (established 2024); the substrate supplies the")
print("  ingredients (staggered order + crystal shear), nothing novel. It does NOT explain the Standard-")
print("  Model gauge groups or the three fermion generations -- magnetic-order classification (Landau")
print("  symmetry breaking) is unrelated to SU(3)xSU(2)xU(1) or generations. The '3 orders <-> 3 generations'")
print("  is numerology unless forced. NULL on gauge groups/generations; genuine POSITIVE on altermagnetism.")
