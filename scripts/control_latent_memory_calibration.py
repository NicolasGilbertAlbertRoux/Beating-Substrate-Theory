#!/usr/bin/env python3
from __future__ import annotations
"""
BST supplementary control: latent-memory calibration.

Purpose
-------
Test whether persistent latent memory improves reconstruction under observable
aliasing, while destroyed / shuffled / wrong memory controls collapse. This is a
lightweight repo-ready control aligned with the final BST lexicon.
"""
import json
from pathlib import Path
import numpy as np

OUTDIR = Path("../results/summaries/latent_memory_calibration")
SEED = 4343
N_GROUPS = 32
ALIAS_SIZE = 6
DIM_OBS = 24
DIM_LAT = 48
TRIALS = 256


def unit(x, axis=-1, eps=1e-12):
    n = np.linalg.norm(x, axis=axis, keepdims=True)
    return x / np.maximum(n, eps)


def make_world(rng):
    n = N_GROUPS * ALIAS_SIZE
    groups = np.repeat(np.arange(N_GROUPS), ALIAS_SIZE)
    obs_group = unit(rng.normal(size=(N_GROUPS, DIM_OBS)))
    obs = obs_group[groups]
    latent_memory = unit(rng.normal(size=(n, DIM_LAT)))
    arbitration = unit(np.tanh(2.0 * latent_memory))
    return groups, obs, latent_memory, arbitration


def query_memory(memory, target, group_ids, rng, condition):
    if condition == "coherent_memory":
        return memory[target]
    if condition == "destroyed_memory":
        return unit(rng.normal(size=(DIM_LAT,)))
    if condition == "shuffled_memory":
        return memory[int(rng.integers(0, len(memory)))]
    if condition == "wrong_memory":
        wrong = group_ids[group_ids != target]
        return memory[int(rng.choice(wrong))]
    if condition == "adversarial_memory":
        return unit(-memory[target] + 0.05 * rng.normal(size=(DIM_LAT,)))
    raise ValueError(condition)


def score(memory, arbitration, groups, rng, condition):
    recovered = []
    dominance = []
    for _ in range(TRIALS):
        target = int(rng.integers(0, len(groups)))
        group_ids = np.flatnonzero(groups == groups[target])
        q = query_memory(memory, target, group_ids, rng, condition)
        # calibration: coherent latent memory plus arbitration orientation.
        # Controls must not receive target-specific arbitration leakage.
        if condition == "coherent_memory":
            arb_q = arbitration[target]
        else:
            arb_q = unit(rng.normal(size=arbitration.shape[1]))
        q = unit(0.75 * q + 0.25 * arb_q)
        candidates = unit(0.75 * memory[group_ids] + 0.25 * arbitration[group_ids])
        sims = candidates @ q
        pred = int(group_ids[int(np.argmax(sims))])
        recovered.append(pred == target)
        target_pos = int(np.where(group_ids == target)[0][0])
        target_sim = sims[target_pos]
        sims2 = sims.copy(); sims2[target_pos] = -np.inf
        dominance.append(float(target_sim - np.max(sims2)))
    return float(np.mean(recovered)), float(np.mean(dominance))


def main():
    rng = np.random.default_rng(SEED)
    groups, obs, memory, arbitration = make_world(rng)
    conditions = ["coherent_memory", "destroyed_memory", "shuffled_memory", "wrong_memory", "adversarial_memory"]
    results = {}
    for condition in conditions:
        rec, dom = score(memory, arbitration, groups, rng, condition)
        results[condition] = {"recovered": rec, "dominance": dom}

    interpretation = {
        "coherent_recovery": results["coherent_memory"]["recovered"],
        "destroyed_recovery": results["destroyed_memory"]["recovered"],
        "wrong_recovery": results["wrong_memory"]["recovered"],
        "shuffled_recovery": results["shuffled_memory"]["recovered"],
        "adversarial_recovery": results["adversarial_memory"]["recovered"],
    }
    passed = (
        interpretation["coherent_recovery"] > 0.95
        and interpretation["destroyed_recovery"] < 0.35
        and interpretation["wrong_recovery"] < 0.35
        and interpretation["shuffled_recovery"] < 0.35
        and interpretation["adversarial_recovery"] < 0.35
    )
    OUTDIR.mkdir(parents=True, exist_ok=True)
    (OUTDIR / "interpretation.json").write_text(json.dumps({"results": results, "passed": passed}, indent=2), encoding="utf-8")
    for k, v in interpretation.items():
        print(f"{k:28s} {v:.4f}")
    print("[RESULT] Latent-memory calibration control " + ("PASSES." if passed else "FAILS."))
    raise SystemExit(0 if passed else 1)

if __name__ == "__main__":
    main()
