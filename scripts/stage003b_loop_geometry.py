#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 3b — monopole LOOP GEOMETRY (the user's straight->spiral prediction).
Per-loop radius of gyration Rg vs loop length L. Exponent nu (Rg ~ L^nu):
  straight/extended -> nu ~ 1 ; random-walk -> nu ~ 0.5 ; winding/spiral -> small nu.
DISCIPLINE: first VALIDATE the periodic-Rg metric on synthetic line vs random-walk
sets (must recover nu~1 and nu~0.5). Only then measure real monopole loops.
HONEST CAVEAT: on a small lattice the large/percolating loop's Rg saturates at the
box size (finite-size), so the *large-loop* spiral regime needs a bigger lattice.
"""
import numpy as np
def shift(a,axis,s): return np.roll(a,-s,axis=axis)
def eps4(a,b,c,d):
    idx=(a,b,c,d)
    if len(set(idx))!=4: return 0
    s=1
    for i in range(4):
        for j in range(i+1,4):
            if idx[i]>idx[j]: s=-s
    return s

def periodic_Rg(coords, L):
    """coords: (n,4) integer site coords on a periodic L^4 lattice. Returns Rg (circular)."""
    if len(coords)<2: return 0.0
    tot=0.0
    for d in range(4):
        a=2*np.pi*coords[:,d]/L
        C=np.cos(a).mean(); S=np.sin(a).mean(); R=np.sqrt(C*C+S*S)
        tot+= (L/(2*np.pi))**2 * (-2.0*np.log(max(R,1e-9)))   # wrapped-normal variance est.
    return float(np.sqrt(tot))

# ---------- validate metric on synthetic sets ----------
def fit_nu(Ls, Rgs):
    Ls=np.array(Ls,float); Rgs=np.array(Rgs,float); m=(Ls>0)&(Rgs>0)
    return float(np.polyfit(np.log(Ls[m]), np.log(Rgs[m]),1)[0])
BOX=24; rng=np.random.default_rng(0)
line_L=[]; line_Rg=[]
for n in [6,10,16,24,40,64,100]:
    c=np.zeros((n,4),int); c[:,0]=np.arange(n)%BOX
    line_L.append(n); line_Rg.append(periodic_Rg(c,BOX))
rw_L=[]; rw_Rg=[]
for n in [6,10,16,24,40,64,100,160]:
    step=rng.integers(0,4,n); sign=rng.choice([-1,1],n); c=np.zeros((n,4),int); pos=np.zeros(4,int)
    for i in range(n):
        pos=pos.copy(); pos[step[i]]+=sign[i]; c[i]=pos%BOX
    rw_L.append(n); rw_Rg.append(periodic_Rg(c,BOX))
print("METRIC VALIDATION (synthetic):")
print(f"  straight line : nu = {fit_nu(line_L,line_Rg):.2f}  (expect ~1.0)")
print(f"  random walk   : nu = {fit_nu(rw_L,rw_Rg):.2f}  (expect ~0.5)")

# ---------- real monopole loops ----------
def mc(L,beta,n_therm=140,eps=0.5,seed=0):
    rng=np.random.default_rng(seed); θ=rng.uniform(-np.pi,np.pi,(4,L,L,L,L))
    def staple(mu):
        A=np.zeros((L,L,L,L),dtype=complex)
        for nu in range(4):
            if nu==mu: continue
            f=shift(θ[nu],mu,1)-shift(θ[mu],nu,1)-θ[nu]
            b=-shift(shift(θ[nu],mu,1),nu,-1)-shift(θ[mu],nu,-1)+shift(θ[nu],nu,-1)
            A+=np.exp(1j*f)+np.exp(1j*b)
        return A
    for _ in range(n_therm):
        for mu in range(4):
            A=staple(mu); R=np.abs(A); psi=np.angle(A)
            prop=θ[mu]+rng.uniform(-eps,eps,(L,L,L,L))
            dS=-beta*(R*np.cos(prop+psi)-R*np.cos(θ[mu]+psi))
            mm=rng.random((L,L,L,L))<np.exp(-dS); θ[mu]=np.where(mm,prop,θ[mu])
    return θ
def monopole_currents(θ):
    L=θ.shape[1]; n={}
    for mu in range(4):
        for nu in range(mu+1,4):
            tp=θ[mu]+shift(θ[nu],mu,1)-shift(θ[mu],nu,1)-θ[nu]
            n[(mu,nu)]=np.round(tp/(2*np.pi)).astype(int)
    def nf(r,s):
        if r==s: return np.zeros((L,)*4,int)
        return n[(r,s)] if r<s else -n[(s,r)]
    m=[]
    for mu in range(4):
        acc=np.zeros((L,)*4)
        for nu in range(4):
            for r in range(4):
                for s in range(4):
                    e=eps4(mu,nu,r,s)
                    if e: acc=acc+0.5*e*(shift(nf(r,s),nu,1)-nf(r,s))
        m.append(np.round(acc).astype(int))
    return m
def loops(m,L):
    parent=list(range(L**4))
    def find(a):
        while parent[a]!=a: parent[a]=parent[parent[a]]; a=parent[a]
        return a
    def union(a,b):
        ra,rb=find(a),find(b)
        if ra!=rb: parent[ra]=rb
    def idx(c): return (((c[0]*L+c[1])*L+c[2])*L+c[3])
    occ={}  # site index -> coords for occupied sites
    links=0
    for mu in range(4):
        nz=np.argwhere(m[mu]!=0)
        for x in nz:
            x=tuple(int(v) for v in x); y=list(x); y[mu]=(y[mu]+1)%L; y=tuple(y)
            ix=idx(x); iy=idx(y); union(ix,iy)
            occ[ix]=x; occ[iy]=y; links+=abs(int(m[mu][x]))
    comps={}
    for ix,c in occ.items():
        r=find(ix); comps.setdefault(r,[]).append(c)
    out=[]
    for r,cs in comps.items():
        out.append((len(cs), periodic_Rg(np.array(cs),L)))   # (size in sites, Rg)
    return out

print("\nREAL monopole loops (L=8):")
for beta,lab in [(0.8,"confined"),(1.6,"Coulomb")]:
    th=mc(8,beta); m=monopole_currents(th); lp=loops(m,8)
    lp=[(s,rg) for (s,rg) in lp if s>=4]            # ignore trivial
    if len(lp)<5: print(f"  beta={beta} ({lab}): too few loops"); continue
    sizes=np.array([s for s,_ in lp]); rgs=np.array([rg for _,rg in lp])
    sat=0.7*periodic_Rg(np.array([[i%8,0,0,0] for i in range(8)]),8)  # ~saturation scale
    sub=sizes< np.percentile(sizes,80)              # drop the few largest (finite-size saturated)
    nu=fit_nu(sizes[sub],rgs[sub]) if sub.sum()>=4 else float('nan')
    print(f"  beta={beta} ({lab}): n_loops={len(lp)}  max_size={sizes.max()}  "
          f"nu(non-saturated)={nu:.2f}  (null random-walk=0.50)")
print("\nReading: nu>0.5 => loops straighter than random walk; nu~0.5 => random-walk-like;")
print("size-dependent drop (small straight->large winding) needs a BIGGER lattice (3c).")
