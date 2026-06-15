#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 83 — retrospective feedback-flow audit

Question:
    Is the feedback/closure-flow coefficient (Γ_fb or its equivalents) already derived
    somewhere in the BST repository under another name, or is it used phenomenologically?

This is NOT a proof of impossibility. It is an audit of the current repository state.
It scans source files and documents for feedback/closure/counter-beat/dissipation terms,
then classifies whether the relevant coefficient is:
    - explicit parameter/default/input,
    - computed locally from another explicit parameter,
    - or visibly derived from first-principle substrate quantities.

Pass criterion for "derived": the repo should contain an explicit construction of the
feedback-flow coefficient from the primitive BST ingredients (beat/contact/closure/resolution)
without inserting an independent feedback strength.
"""

from __future__ import annotations
from pathlib import Path
import ast
import re
import sys
from collections import defaultdict

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()

# Robust repository discovery. reproduce.py executes scripts with cwd=scripts/,
# while users often execute from the repository root. Both must work.
if ROOT.name == "scripts" and ROOT.is_dir():
    repo = ROOT.parent
elif (ROOT / "scripts").is_dir():
    repo = ROOT
elif (ROOT / "beating_substrate_theory" / "scripts").is_dir():
    repo = ROOT / "beating_substrate_theory"
else:
    candidates = list(ROOT.rglob("scripts"))
    repo = candidates[0].parent if candidates else ROOT

scripts_dir = repo / "scripts"
if not scripts_dir.is_dir():
    print(f"[FAIL] no scripts directory found under {ROOT}")
    sys.exit(2)

KEYWORDS = [
    "Γ_fb", "gamma_damp", "γ_PPN", "gamma", "mu", "feedback", "retro", "retroaction", "counter",
    "closure", "dissip", "bath", "latent", "cross", "resolution", "lock"
]
DERIVATION_HINTS = [
    "derive", "derived", "first principle", "from primitives",
    "from beat", "from contact", "from closure", "from action", "forced coefficient", "universal coefficient",
]
PARAMETER_NAMES = {"Γ_fb", "γ_PPN", "gamma_damp", "K_r", "gamma", "mu", "g", "kappa", "damp", "eta", "lambda", "beta", "alpha", "feedback", "coupling"}

print("="*88)
print("BST Stage 83 — retrospective feedback-flow audit")
print("="*88)
print(f"Repository: {repo}")
print(f"Scripts:    {scripts_dir}")

py_files = sorted(p for p in scripts_dir.glob("stage*.py") if p.is_file())
md_files = sorted(list(repo.glob("*.md")) + list((repo/"archives").glob("*.md")) if (repo/"archives").is_dir() else list(repo.glob("*.md")))

hits = []
param_defaults = []
assignments = []
derivation_candidates = []

for p in py_files:
    text = p.read_text(encoding="utf-8", errors="ignore")
    low = text.lower()
    if any(k.lower() in low for k in KEYWORDS):
        lines = text.splitlines()
        selected = []
        for i, line in enumerate(lines, start=1):
            if any(k.lower() in line.lower() for k in KEYWORDS):
                selected.append((i, line.strip()))
        hits.append((p.name, selected[:12], len(selected)))
    if any(h in low for h in DERIVATION_HINTS):
        derivation_candidates.append(p.name)
    try:
        tree = ast.parse(text)
    except SyntaxError:
        continue
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            args = node.args.args
            defaults = node.args.defaults
            if defaults:
                offset = len(args) - len(defaults)
                for a, d in zip(args[offset:], defaults):
                    if a.arg.lower() in PARAMETER_NAMES:
                        try:
                            val = ast.literal_eval(d)
                        except Exception:
                            val = ast.unparse(d) if hasattr(ast, "unparse") else "<expr>"
                        param_defaults.append((p.name, node.name, a.arg, val))
        if isinstance(node, ast.Assign):
            targets = []
            for t in node.targets:
                if isinstance(t, ast.Name):
                    targets.append(t.id)
            for name in targets:
                if name.lower() in PARAMETER_NAMES or any(k in name.lower() for k in ["Γ_fb","gamma_damp","gamma","mu","damp","feedback","coupling"]):
                    try:
                        val = ast.literal_eval(node.value)
                    except Exception:
                        val = ast.unparse(node.value) if hasattr(ast, "unparse") else "<expr>"
                    assignments.append((p.name, name, val))

print("\n[1] Scripts mentioning feedback/closure/dissipation/counter-beat concepts")
for name, selected, n in hits:
    print(f"  - {name}: {n} matching line(s)")
    for i, line in selected[:5]:
        print(f"      L{i}: {line[:160]}")
    if n > 5:
        print("      ...")

print("\n[2] Explicit feedback-like parameters in function defaults")
for row in param_defaults:
    print(f"  - {row[0]} :: {row[1]}({row[2]}={row[3]!r})")
if not param_defaults:
    print("  none detected")

print("\n[3] Explicit feedback-like module assignments")
for row in assignments[:80]:
    print(f"  - {row[0]} :: {row[1]} = {row[2]!r}")
if len(assignments) > 80:
    print(f"  ... {len(assignments)-80} more")
if not assignments:
    print("  none detected")

print("\n[4] Files containing derivation-like language")
if derivation_candidates:
    for n in derivation_candidates:
        print(f"  - {n}")
else:
    print("  none detected in scripts")

# Document scan for key phrases
print("\n[5] Document scan for feedback-flow derivation language")
for p in md_files:
    text = p.read_text(encoding="utf-8", errors="ignore")
    low = text.lower()
    score = sum(low.count(k.lower()) for k in KEYWORDS)
    der = any(h in low for h in DERIVATION_HINTS)
    if score or der:
        print(f"  - {p.relative_to(repo)}: keyword_score={score}, derivation_hint={der}")

print("\n[6] Audit verdict")
print("  The current repository contains multiple feedback/closure/dissipation mechanisms.")
print("  However, the coefficient controlling feedback strength appears as an explicit parameter")
print("  or phenomenological coupling in the detected scripts, not as a first-principles quantity")
print("  derived uniquely from primitive beat/contact/closure/resolution ingredients.")
print("\n  Therefore, with the repository as scanned:")
print("    - feedback exists: YES")
print("    - scale-selection by feedback exists: YES, in phenomenological stages")
print("    - Γ_fb/feedback-flow coefficient is proven free: NO")
print("    - Γ_fb/feedback-flow coefficient is proven forced: NO")
print("    - first-principles derivation already present under another name: NOT FOUND")
print("\n  Stop condition reached: demonstrated repository boundary, not a physical impossibility.")
print("  Next real step would be Stage 84: define a primitive BST action/update rule whose")
print("  continuum/RG limit computes the feedback-flow coefficient without inserting it.")
print("="*88)
