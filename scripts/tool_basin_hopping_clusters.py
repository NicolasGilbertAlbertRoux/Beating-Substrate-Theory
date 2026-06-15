#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST tool — global cluster optimizer (basin hopping) for the STATIC potential.
SUPPORTS Stages 15-17 (emergent architectures / static minima). This is a standalone DIAGNOSTIC TOOL,
not a numbered pre-registered stage: it is meant to be run separately for large N / many restarts, and is
deliberately not imported by the stage scripts. Cross-referenced here for reproducibility.
Finds the lowest-energy arrangement of N nodes, so you can ask "what architectures are the
TRUE static minima at large N?" -- the clean comparison Stage 16/17 lacked (my quick damped
relaxations were unreliable). Run this on your own machine for big N / many restarts.

Two cores you can compare (set CORE below):
  - "soft": YOUR contact potential  U = sum_{i<j} [ -G/d + (k/2) max(0, 2R0-d)^2 ].
            HONEST WARNING: -G/d diverges at d->0 and the soft repulsion is FINITE, so the
            GLOBAL minimum is COLLAPSE (all nodes on a point). Basin hopping WILL find collapse.
            That is the point: it shows the extended cluster is only METASTABLE statically, and
            that a stable extended structure needs the dynamical beat (S14c), not a static min.
  - "lj":   Lennard-Jones  U = sum_{i<j} [ d^-12 - 2 d^-6 ]  (hard core). A reference whose true
            global minima ARE the famous cluster geometries (N=13 icosahedron, etc.) -- use it
            to see the "expected" architectures and contrast with your soft/beating case.

Requires: numpy, scipy.  Reports best energy, mean coordination, and an order signature.
No claim about nature; this characterizes a model potential's minima.
"""
import numpy as np
from scipy.optimize import minimize

CORE = "soft"          # "soft" (your potential) or "lj"
N    = 13              # cluster size
G, k, R0 = 1.0, 3.0, 0.8
HOPS = 200             # basin-hopping iterations (raise for large N)
STEP = 0.6            # perturbation size
SEED = 0

def energy_grad(flat, n):
    X = flat.reshape(n, 3)
    U = 0.0; Gd = np.zeros_like(X)
    for i in range(n):
        r = X[i] - X; d = np.linalg.norm(r, axis=1); d[i] = np.inf; u = r / d[:, None]
        if CORE == "soft":
            U += 0.5 * np.sum(-G / d + 0.5 * k * np.maximum(0.0, 2*R0 - d)**2)
            f = (-G / d**2 + k * np.maximum(0.0, 2*R0 - d))   # dU/dd magnitude along -u
            Gd[i] += np.sum((f)[:, None] * (-u), axis=0)
        else:  # lj
            inv = 1.0 / d
            U += 0.5 * np.sum(inv**12 - 2 * inv**6)
            f = (-12 * inv**13 + 12 * inv**7)
            Gd[i] += np.sum(f[:, None] * (-u), axis=0)
    return U, Gd.ravel()

def local_min(X):
    res = minimize(energy_grad, X.ravel(), args=(len(X),), jac=True, method="L-BFGS-B")
    return res.x.reshape(len(X), 3), res.fun

def basin_hopping(n, hops, step, seed):
    rng = np.random.default_rng(seed)
    X = rng.standard_normal((n, 3)) * 1.2
    X, E = local_min(X); best_X, best_E = X.copy(), E
    for _ in range(hops):
        Xt = X + rng.standard_normal((n, 3)) * step
        Xt, Et = local_min(Xt)
        if Et < E or rng.random() < np.exp(-(Et - E) / 0.5):
            X, E = Xt, Et
            if Et < best_E: best_X, best_E = Xt.copy(), Et
    return best_X, best_E

def signature(X):
    D = np.linalg.norm(X[:, None] - X[None, :], axis=2); np.fill_diagonal(D, np.inf)
    nn = D.min(1); s = np.median(nn); cut = 1.3 * s
    coord = (D < cut).sum(1)
    spread = nn.std() / max(nn.mean(), 1e-9)
    rg = np.sqrt(((X - X.mean(0))**2).sum(1).mean())
    return coord.mean(), spread, rg, s

if __name__ == "__main__":
    print(f"Basin hopping: CORE={CORE}, N={N}, {HOPS} hops")
    X, E = basin_hopping(N, HOPS, STEP, SEED)
    co, sp, rg, s = signature(X)
    print(f"  best energy   : {E:.4f}")
    print(f"  mean coord    : {co:.2f}")
    print(f"  NN regularity : CV={sp:.3f}  (0 = perfectly regular)")
    print(f"  radius of gyr : {rg:.3f}   NN spacing : {s:.3f}")
    if CORE == "soft" and rg < 0.3:
        print("  -> COLLAPSED (rg ~ 0): confirms the soft static potential's global min is a point;")
        print("     a stable EXTENDED cluster requires the dynamical beat, not a static minimum.")
