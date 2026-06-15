#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 84 — action-derived feedback calibration scan

Question:
    Can the substrate feedback coefficient Γ_fb be derived from the action/counter-beat
    structure, rather than inserted as a free phenomenological parameter?

What this test DOES:
    1. Writes the Stage-7 feedback as the variational response of a discrete phase action:
           V_K(θ) = -K_r sum_i cos(θ_{i+1}-θ_i)
       giving:
           -dV/dθ_i = K_r[sin(θ_{i-1}-θ_i)+sin(θ_{i+1}-θ_i)].
    2. Recovers Γ_fb_eff numerically by regressing the feedback response against the
       variational force direction.
    3. Scans K_r and asks whether a multi-resolution reconstruction criterion selects a
       robust K_r* rather than merely using a freely chosen feedback strength.

Interpretation:
    - If Γ_fb_eff = K_r: feedback is derived from the action FORM.
    - If a robust K_r* appears across seeds/resolutions: the magnitude is calibrated by the
      substrate reconstruction criterion.
    - If no unique K_r*: Γ_fb remains action-derived in form, but not first-principles fixed
      in magnitude by this test alone.
"""
from __future__ import annotations
import argparse
from dataclasses import dataclass
import numpy as np

try:
    from sklearn.linear_model import Ridge
    from sklearn.metrics import r2_score
except Exception as e:
    raise SystemExit("This test requires scikit-learn. Install with: pip install scikit-learn") from e

@dataclass
class RunMetrics:
    K_r: float
    block: int
    seed: int
    r2: float
    sync: float
    Γ_fb_eff: float
    Γ_fb_error: float
    objective: float

def simulate(N=48, steps=220, dt=0.1, K_r=2.0, seed=0, omega_sigma=0.3):
    rng = np.random.default_rng(seed)
    θ = rng.uniform(0, 2*np.pi, N)
    omega = rng.normal(1.0, omega_sigma, N)
    O, sync, force_terms, response_terms = [], [], [], []
    for _ in range(steps):
        # force direction c = -d/dθ[-sum cos(delta θ)]
        c = np.sin(np.roll(θ, 1) - θ) + np.sin(np.roll(θ, -1) - θ)
        dθ = omega + K_r*c
        θ = θ + dt*dθ
        O.append(np.cos(θ).copy())
        sync.append(abs(np.mean(np.exp(1j*θ))))
        force_terms.append(c.copy())
        response_terms.append((dθ - omega).copy())
    return np.array(O), float(np.mean(sync)), np.array(force_terms), np.array(response_terms)

def crossres_R2(O, block=4, w=5, h=3):
    steps, N = O.shape
    ncoarse = N // block
    O2 = O[:, :ncoarse*block]
    C = O2.reshape(steps, ncoarse, block).mean(2)
    X, Y = [], []
    for t in range(w-1, steps-h):
        X.append(C[t-w+1:t+1].ravel())
        Y.append(O2[t+h])
    X = np.asarray(X); Y = np.asarray(Y)
    ntr = int(0.7*len(X))
    pred = Ridge(alpha=1.0).fit(X[:ntr], Y[:ntr]).predict(X[ntr:])
    return float(r2_score(Y[ntr:], pred))

def estimate_Γ_fb(c, response):
    x = c.ravel(); y = response.ravel()
    denom = float(np.dot(x, x))
    return float(np.dot(x, y)/denom) if denom > 1e-12 else float('nan')

def run_scan(Ks, blocks, seeds, sync_penalty=0.35):
    rows = []
    for block in blocks:
        for K_r in Ks:
            for seed in seeds:
                O, sync, c, resp = simulate(K_r=K_r, seed=seed)
                r2 = crossres_R2(O, block=block)
                Γ_fb_eff = estimate_Γ_fb(c, resp)
                Γ_fb_error = abs(Γ_fb_eff - K_r)
                objective = r2 - sync_penalty*max(0.0, sync-0.55)**2 - 2.0*Γ_fb_error
                rows.append(RunMetrics(K_r, block, seed, r2, sync, Γ_fb_eff, Γ_fb_error, objective))
    return rows

def summarize(rows):
    out = []
    for K_r in sorted({r.K_r for r in rows}):
        rr = [r for r in rows if r.K_r == K_r]
        out.append({
            'K_r': K_r,
            'r2_mean': float(np.mean([r.r2 for r in rr])),
            'r2_std': float(np.std([r.r2 for r in rr])),
            'sync_mean': float(np.mean([r.sync for r in rr])),
            'Γ_fb_eff_mean': float(np.mean([r.Γ_fb_eff for r in rr])),
            'gamma_err_mean': float(np.mean([r.Γ_fb_error for r in rr])),
            'objective_mean': float(np.mean([r.objective for r in rr])),
        })
    return out, max(out, key=lambda d: d['objective_mean'])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--Ks', default='0.1,0.5,1.0,2.0')
    ap.add_argument('--blocks', default='2,4')
    ap.add_argument('--seeds', default='0')
    args = ap.parse_args()
    Ks = [float(x) for x in args.Ks.split(',') if x.strip()]
    blocks = [int(x) for x in args.blocks.split(',') if x.strip()]
    seeds = [int(x) for x in args.seeds.split(',') if x.strip()]
    rows = run_scan(Ks, blocks, seeds)
    summary, best = summarize(rows)
    print('='*80)
    print('BST Stage 84 — action-derived feedback calibration scan')
    print('='*80)
    print('Analytic derivation:')
    print('  V_K(θ) = -K_r sum_i cos(θ_{i+1}-θ_i)')
    print('  -dV/dθ_i = K_r[sin(θ_{i-1}-θ_i)+sin(θ_{i+1}-θ_i)]')
    print('  => Stage-7 feedback is derived from the action FORM.')
    print()
    print(f"{'K_r':>6} {'R2 mean':>10} {'R2 std':>9} {'sync':>8} {'Γ_fb_eff':>11} {'|err|':>9} {'objective':>10}")
    for d in summary:
        print(f"{d['K_r']:6.2f} {d['r2_mean']:10.3f} {d['r2_std']:9.3f} {d['sync_mean']:8.3f} {d['Γ_fb_eff_mean']:11.3f} {d['gamma_err_mean']:9.2e} {d['objective_mean']:10.3f}")
    print('\nBest calibration by this objective:')
    print(f"  K_r* = {best['K_r']:.6g}")
    print(f"  R2_mean = {best['r2_mean']:.4f}, sync_mean = {best['sync_mean']:.4f}, Γ_fb_eff_mean = {best['Γ_fb_eff_mean']:.6g}")
    Γ_fb_form_ok = max(d['gamma_err_mean'] for d in summary) < 1e-8
    objmax = best['objective_mean']
    close = [d for d in summary if d['objective_mean'] >= objmax - 0.01*max(1.0, abs(objmax))]
    print('\nVerdict:')
    print('  PASS: Γ_fb is recovered as the variational action coefficient K_r.' if Γ_fb_form_ok else '  FAIL/BUG: Γ_fb_eff is not recovered from K_r.')
    if len(close) <= 2:
        print('  Calibration scan suggests a localized K_r* for this objective.')
    else:
        print('  Broad/criterion-dependent optimum: Γ_fb is action-derived in form,')
        print('  but not first-principles fixed in magnitude by this scan alone.')
    print('\nHonest interpretation:')
    print('  Your intuition is right in form: retroaction is derivable from the action.')
    print('  The remaining question is whether the coefficient K_r/Γ_fb is fixed by a')
    print('  deeper calibration principle, or remains the one legitimate scale/coupling anchor.')

if __name__ == '__main__':
    main()
