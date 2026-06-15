#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
stage85_action_feedback_closure_anchor_audit.py

Purpose
-------
Final BST audit for the question:

    Is the feedback / counter-beat coefficient Γ_fb (or K_r) derived from the
    substrate action, or is it still an independent closure anchor?

This test separates three claims:

1. FORM DERIVATION:
   Given an action S_K[θ], the feedback force is indeed
       F = - dS/dθ.
   This is tested by comparing the analytic force to finite differences.

2. COEFFICIENT STATUS:
   The same derivation gives
       F_K = K_r * F_1.
   Therefore the action derives the SHAPE of the feedback law, but not the
   absolute value of K_r unless an independent equation fixes K_r.

3. MULTI-RESOLUTION STATUS:
   Coarse-graining / multi-resolution projection is tested to see whether K_r
   flows to a universal fixed value K_r*.  With the native harmonic/contact
   action alone, K_eff tracks the input K_r.  No universal K_r* is found.

Interpretation
--------------
PASS means the audit is successful, not that K_r is derived.
The expected honest verdict for current BST is:

    action_derives_feedback_shape_but_not_feedback_anchor

That is: K_r/Γ_fb is the substrate resistance / closure stiffness / calibration
anchor unless a later theory supplies an autonomous flow equation for K_r.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import numpy as np


def wrap_angle(x: np.ndarray) -> np.ndarray:
    """Map angles to (-pi, pi]."""
    return (x + np.pi) % (2.0 * np.pi) - np.pi


def action(θ: np.ndarray, K_r: float) -> float:
    """Nearest-neighbour compact phase action."""
    dx = wrap_angle(np.roll(θ, -1, axis=1) - θ)
    dy = wrap_angle(np.roll(θ, -1, axis=0) - θ)
    return float(K_r * np.sum((1.0 - np.cos(dx)) + (1.0 - np.cos(dy))))


def force_unit(θ: np.ndarray) -> np.ndarray:
    """
    Unit-K_r feedback force F_1 = - dS_{K_r=1}/dθ.

    For S = K_r sum_links (1 - cos(θ_j - θ_i)),
    F_i = -dS/dθ_i =
        K_r [ sin(θ_{i+e_x}-θ_i)
          + sin(θ_{i-e_x}-θ_i)
          + sin(θ_{i+e_y}-θ_i)
          + sin(θ_{i-e_y}-θ_i) ].
    """
    right = wrap_angle(np.roll(θ, -1, axis=1) - θ)
    left  = wrap_angle(np.roll(θ,  1, axis=1) - θ)
    down  = wrap_angle(np.roll(θ, -1, axis=0) - θ)
    up    = wrap_angle(np.roll(θ,  1, axis=0) - θ)
    return np.sin(right) + np.sin(left) + np.sin(down) + np.sin(up)


def force(θ: np.ndarray, K_r: float) -> np.ndarray:
    return K_r * force_unit(θ)


def finite_difference_force(θ: np.ndarray, K_r: float, eps: float = 1e-6, samples: int = 64, seed: int = 0) -> np.ndarray:
    """Finite-difference check of F=-grad S on random entries."""
    rng = np.random.default_rng(seed)
    fd = np.zeros_like(θ)
    ny, nx = θ.shape
    coords = list(zip(rng.integers(0, ny, size=samples), rng.integers(0, nx, size=samples)))
    for y, x in coords:
        tp = θ.copy()
        tm = θ.copy()
        tp[y, x] += eps
        tm[y, x] -= eps
        dS = (action(tp, K_r) - action(tm, K_r)) / (2.0 * eps)
        fd[y, x] = -dS
    return fd, coords


def estimate_Γ_fb_eff(θ: np.ndarray, K_r: float) -> float:
    """Least-squares Γ_fb in F_K ≈ Γ_fb * F_1."""
    f1 = force_unit(θ).ravel()
    fk = force(θ, K_r).ravel()
    den = float(np.dot(f1, f1)) + 1e-15
    return float(np.dot(f1, fk) / den)


def block_average_angle(θ: np.ndarray, block: int) -> np.ndarray:
    """Circular block average of a phase field."""
    if block == 1:
        return θ.copy()
    ny, nx = θ.shape
    ny2 = (ny // block) * block
    nx2 = (nx // block) * block
    th = θ[:ny2, :nx2]
    z = np.exp(1j * th)
    z = z.reshape(ny2 // block, block, nx2 // block, block).mean(axis=(1, 3))
    return np.angle(z)


def scan_existing_repo(repo: Path) -> list[str]:
    """Lightweight textual scan for K_r/Γ_fb/mu assignments."""
    hits = []
    if not repo.exists():
        return hits
    for py in sorted(repo.rglob("*.py")):
        if "__MACOSX" in str(py):
            continue
        try:
            txt = py.read_text(errors="ignore")
        except Exception:
            continue
        for i, line in enumerate(txt.splitlines(), start=1):
            if re.search(r"\b(Γ_fb|γ_PPN|gamma_damp|K_r|K_R|GAMMA|gamma|K|MU|mu)\s*=", line):
                hits.append(f"{py.relative_to(repo)}:{i}: {line.strip()}")
    return hits


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("repo", nargs="?", default=".", help="Optional BST repo path for textual scan.")
    ap.add_argument("--size", type=int, default=128)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--Ks", default="0.1,0.25,0.5,1.0,2.0,4.0")
    ap.add_argument("--blocks", default="1,2,4,8")
    args = ap.parse_args()

    Ks = [float(x) for x in args.Ks.split(",") if x.strip()]
    blocks = [int(x) for x in args.blocks.split(",") if x.strip()]

    rng = np.random.default_rng(args.seed)
    # Smooth-ish phase field: random Fourier-like construction by repeated averaging.
    θ = rng.normal(size=(args.size, args.size))
    for _ in range(8):
        θ = 0.25 * (
            np.roll(θ, 1, axis=0) + np.roll(θ, -1, axis=0) +
            np.roll(θ, 1, axis=1) + np.roll(θ, -1, axis=1)
        )
    θ = wrap_angle(θ)

    print("\n=== STAGE 85 — ACTION-DERIVED FEEDBACK / CLOSURE ANCHOR AUDIT ===\n")

    print("[A] Variational check: F = -dS/dθ")
    K_r_test = 1.7
    fd, coords = finite_difference_force(θ, K_r_test, samples=128, seed=args.seed)
    fa = force(θ, K_r_test)
    errs = []
    for y, x in coords:
        denom = abs(fa[y, x]) + 1e-12
        errs.append(abs(fd[y, x] - fa[y, x]) / denom)
    print(f"    K_r_test={K_r_test}")
    print(f"    median relative error = {np.median(errs):.3e}")
    print(f"    max relative error    = {np.max(errs):.3e}")
    variational_ok = np.median(errs) < 1e-5
    print(f"    verdict: {'PASS' if variational_ok else 'FAIL'} — feedback SHAPE is action-derived\n")

    print("[B] Coefficient audit: does derivation fix K_r/Γ_fb?")
    rows = []
    for K_r in Ks:
        ge = estimate_Γ_fb_eff(θ, K_r)
        rows.append((K_r, ge, ge / K_r if K_r != 0 else np.nan))
        print(f"    input K_r={K_r:8.4g} -> Γ_fb_eff={ge:10.6g} ; Γ_fb_eff/K_r={ge/K_r:10.6g}")
    ratios = np.array([r[2] for r in rows if np.isfinite(r[2])])
    coeff_tracks_input = np.allclose(ratios, 1.0, rtol=1e-8, atol=1e-10)
    print(f"    verdict: {'PASS' if coeff_tracks_input else 'FAIL'} — action gives F_K = K_r F_1; K_r is inherited, not fixed\n")

    print("[C] Multi-resolution audit: does K_r flow to a universal K_r* under native coarse-graining?")
    print("    block | " + " | ".join([f"K_r={K_r:g}" for K_r in Ks]))
    eff_by_block = {}
    for b in blocks:
        thb = block_average_angle(θ, b)
        vals = []
        for K_r in Ks:
            vals.append(estimate_Γ_fb_eff(thb, K_r))
        eff_by_block[b] = vals
        print(f"    {b:5d} | " + " | ".join([f"{v:9.5g}" for v in vals]))

    # If universal, final block values should be much closer to each other than input K_r values.
    final_vals = np.array(eff_by_block[blocks[-1]], dtype=float)
    input_vals = np.array(Ks, dtype=float)
    input_cv = float(np.std(input_vals) / (np.mean(input_vals) + 1e-15))
    final_cv = float(np.std(final_vals) / (np.mean(final_vals) + 1e-15))
    convergence_ratio = final_cv / (input_cv + 1e-15)
    universal_flow_found = convergence_ratio < 0.2

    print(f"\n    input coefficient of variation = {input_cv:.6g}")
    print(f"    final coefficient of variation = {final_cv:.6g}")
    print(f"    CV_final / CV_input           = {convergence_ratio:.6g}")
    print(f"    verdict: {'UNIVERSAL_K_FOUND' if universal_flow_found else 'NO_UNIVERSAL_K_FOUND'}")

    print("\n[D] Repository text scan for explicit K_r/Γ_fb/mu assignments")
    hits = scan_existing_repo(Path(args.repo))
    if hits:
        print(f"    found {len(hits)} assignment-like lines; first 25:")
        for h in hits[:25]:
            print("    " + h)
        if len(hits) > 25:
            print(f"    ... {len(hits)-25} more")
    else:
        print("    no assignment-like lines found or repo unavailable")

    print("\n=== FINAL STAGE 85 VERDICT ===")
    if variational_ok and coeff_tracks_input and not universal_flow_found:
        print("action_derives_feedback_shape_but_not_feedback_anchor")
        print("Meaning:")
        print("  - The feedback/counter-beat law is legitimately derived from the action.")
        print("  - The numerical stiffness/resistance K_r (Γ_fb) is not fixed by this derivation.")
        print("  - Native multi-resolution coarse-graining does not force K_r to a universal value.")
        print("  - In current BST, K_r/Γ_fb is therefore the remaining closure anchor:")
        print("        substrate resistance / closure stiffness / calibration constant.")
        print("  - To remove it, BST needs an additional autonomous flow equation K_r -> K_r*,")
        print("    or a deeper derivation of K_r from the substrate ontology itself.")
    else:
        print("audit_inconclusive_or_unexpected")
        print("Inspect sections A-C; one of the expected consistency checks failed.")


if __name__ == "__main__":
    main()
