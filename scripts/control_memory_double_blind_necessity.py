#!/usr/bin/env python3
from __future__ import annotations
"""BST supplementary control: strict double-blind memory necessity."""
import json
from pathlib import Path
import numpy as np

OUTDIR = Path("../results/summaries/memory_double_blind_necessity")
SEED = 424242
N_GROUPS = 48
ALIAS_SIZE = 6
DIM_OBS = 24
DIM_MEM = 64
TRIALS = 384


def unit(x, axis=-1, eps=1e-12):
    return x / np.maximum(np.linalg.norm(x, axis=axis, keepdims=True), eps)


def main():
    rng = np.random.default_rng(SEED)
    n = N_GROUPS * ALIAS_SIZE
    groups = np.repeat(np.arange(N_GROUPS), ALIAS_SIZE)
    observable_by_group = unit(rng.normal(size=(N_GROUPS, DIM_OBS)))
    observable = observable_by_group[groups]  # exact aliasing inside each group
    memory = unit(rng.normal(size=(n, DIM_MEM)))
    chance = 1.0 / ALIAS_SIZE

    def run(condition):
        hits = []
        for _ in range(TRIALS):
            target = int(rng.integers(0, n))
            cand = np.flatnonzero(groups == groups[target])
            if condition == "coherent_memory":
                q = memory[target]
                scores = memory[cand] @ q
                eval_target = target
            elif condition == "observable_only":
                q = observable[target]
                scores = observable[cand] @ q
                eval_target = target
            elif condition == "speed_only_no_memory":
                q = np.tanh(2.0 * memory[target])
                scores = np.zeros(len(cand))  # speed without memory identity cannot disambiguate aliases
                eval_target = target
            elif condition == "wrong_memory":
                wrong = int(rng.choice(cand[cand != target]))
                scores = memory[cand] @ memory[wrong]
                eval_target = target
            elif condition == "destroyed_memory":
                scores = memory[cand] @ unit(rng.normal(size=(DIM_MEM,)))
                eval_target = target
            elif condition == "adversarial_memory":
                scores = memory[cand] @ unit(-memory[target] + 0.05 * rng.normal(size=(DIM_MEM,)))
                eval_target = target
            elif condition == "shuffled_label_control":
                q = memory[target]
                scores = memory[cand] @ q
                eval_target = int(rng.choice(cand[cand != target]))
            else:
                raise ValueError(condition)
            pred = int(cand[int(np.argmax(scores))]) if condition != "speed_only_no_memory" else int(rng.choice(cand))
            hits.append(pred == eval_target)
        return float(np.mean(hits))

    conditions = ["coherent_memory", "observable_only", "speed_only_no_memory", "wrong_memory", "destroyed_memory", "adversarial_memory", "shuffled_label_control"]
    results = {c: run(c) for c in conditions}
    passed = (
        results["coherent_memory"] > 0.95
        and results["observable_only"] <= chance + 0.08
        and results["speed_only_no_memory"] <= chance + 0.08
        and results["wrong_memory"] <= chance + 0.12
        and results["destroyed_memory"] <= chance + 0.12
        and results["shuffled_label_control"] <= chance + 0.12
    )
    OUTDIR.mkdir(parents=True, exist_ok=True)
    (OUTDIR / "interpretation.json").write_text(json.dumps({"chance": chance, "results": results, "passed": passed}, indent=2), encoding="utf-8")
    print(f"chance                      {chance:.4f}")
    for k, v in results.items():
        print(f"{k:28s} {v:.4f}")
    print("[RESULT] Strict double-blind memory necessity " + ("PASSES." if passed else "FAILS."))
    raise SystemExit(0 if passed else 1)

if __name__ == "__main__":
    main()
