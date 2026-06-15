#!/usr/bin/env python3
from __future__ import annotations
"""BST supplementary control: memory anti-cheat under observable aliasing."""
import json
from pathlib import Path
import numpy as np

OUTDIR = Path("../results/summaries/memory_anticheat")
SEED = 40340
N_GROUPS = 40
ALIAS_SIZE = 5
DIM_OBS = 20
DIM_MEM = 40
TRIALS = 320


def unit(x, axis=-1, eps=1e-12):
    return x / np.maximum(np.linalg.norm(x, axis=axis, keepdims=True), eps)


def make_world(rng):
    n = N_GROUPS * ALIAS_SIZE
    groups = np.repeat(np.arange(N_GROUPS), ALIAS_SIZE)
    obs_group = unit(rng.normal(size=(N_GROUPS, DIM_OBS)))
    obs = obs_group[groups]
    memory = unit(rng.normal(size=(n, DIM_MEM)))
    return groups, obs, memory


def evaluate(mode, groups, obs, memory, rng):
    hits = []
    for _ in range(TRIALS):
        target = int(rng.integers(0, len(groups)))
        cand = np.flatnonzero(groups == groups[target])
        if mode == "coherent_memory":
            q = memory[target]
            scores = memory[cand] @ q
        elif mode == "observable_only":
            q = obs[target]
            scores = obs[cand] @ q
        elif mode == "wrong_memory":
            wrong = int(rng.choice(cand[cand != target]))
            scores = memory[cand] @ memory[wrong]
        elif mode == "destroyed_memory":
            scores = memory[cand] @ unit(rng.normal(size=(DIM_MEM,)))
        elif mode == "shuffled_label_control":
            q = memory[target]
            scores = memory[cand] @ q
            target = int(rng.choice(cand[cand != target]))
        else:
            raise ValueError(mode)
        pred = int(cand[int(np.argmax(scores))])
        hits.append(pred == target)
    return float(np.mean(hits))


def main():
    rng = np.random.default_rng(SEED)
    groups, obs, memory = make_world(rng)
    modes = ["coherent_memory", "observable_only", "wrong_memory", "destroyed_memory", "shuffled_label_control"]
    results = {m: evaluate(m, groups, obs, memory, rng) for m in modes}
    chance = 1.0 / ALIAS_SIZE
    passed = (
        results["coherent_memory"] > 0.95
        and results["observable_only"] <= chance + 0.08
        and results["wrong_memory"] <= chance + 0.12
        and results["destroyed_memory"] <= chance + 0.12
        and results["shuffled_label_control"] <= chance + 0.12
    )
    OUTDIR.mkdir(parents=True, exist_ok=True)
    (OUTDIR / "interpretation.json").write_text(json.dumps({"chance": chance, "results": results, "passed": passed}, indent=2), encoding="utf-8")
    print(f"chance                      {chance:.4f}")
    for k, v in results.items():
        print(f"{k:28s} {v:.4f}")
    print("[RESULT] Memory anti-cheat control " + ("PASSES." if passed else "FAILS."))
    raise SystemExit(0 if passed else 1)

if __name__ == "__main__":
    main()
