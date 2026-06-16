# Beating Substrate Theory — Reproducible Scripts

This repository contains the reproducible numerical and algorithmic scripts associated with **Beating Substrate Theory**.

Canonical repository URL:

```text
https://github.com/NicolasGilbertAlbertRoux/Beating-Substrate-Theory.git
```

⸻

## Scope

The repository contains the executable reproduction layer of Beating Substrate Theory (BST), together with formal verification artifacts and theorem documentation.

Included components:

- canonical stages stage001 through stage086;
- memory and latent reconstruction controls;
- supplementary checks for closure, observable equivalence, gauge-structure compatibility, resolution invariance, and topological selection;
- Lean 4 formal verification artifacts;
- theorem compendia (French and English).

The main BST manuscript is maintained separately and is not included in this repository.

⸻

## Structure

```text
Beating-Substrate-Theory/
├── README.md
├── LICENSE
├── requirements.txt
├── reproduce.py
├── scripts/
├── results/
│   └── summaries/
├── lean/
│   ├── BST_core_ext.lean
│   ├── BST_coherence.lean
│   └── README.md
└── theorem_compendium/
    ├── RECUEIL_theoremes_BST.tex
    ├── RECUEIL_theoremes_BST.pdf
    ├── COMPENDIUM_theorems_BST.tex
    └── COMPENDIUM_theorems_BST.pdf
```

results/summaries/ is the canonical output location for generated result files.

Canonical BSF-derived stage scripts do not generate persistent files. Supplementary and control scripts may generate CSV, JSON, or PNG summaries under results/summaries/.

Generated result files are ignored by Git by default and can be regenerated with reproduce.py.

⸻

## Installation

```bash
pip install -r requirements.txt
```

⸻

## Reproduction

Run all canonical stages, controls, and supplementary checks:

```bash
python reproduce.py --quiet --timeout 30
```

Run only the canonical stage chain:

```bash
python reproduce.py --quiet --timeout 30 --canonical-only
```

A successful full run should report:

```text
103/103 script(s) ran cleanly.
```

⸻

## Validation status

Functional reproduction has been confirmed through a complete execution of the repository reporting:

```text
103/103 script(s) ran cleanly.
```

In addition, selected conceptual structures have been formally verified using Lean 4.

The repository therefore contains three complementary validation layers:

- reproducible numerical and algorithmic scripts;
- theorem documentation and dependency tracking;
- formal verification of selected logical structures.

Interpretation of physical, informational, and cognitive claims remains governed by the BST manuscript and theorem compendia.

⸻

## Formal Verification

BST includes a formal verification layer implemented in Lean 4.

The formalization is located in:

```text
lean/
```

and currently contains:

- BST_core_ext.lean
- BST_coherence.lean

These files verify selected logical properties of the framework, including:

- latent necessity;
- persistence;
- closure;
- stability;
- observable/latent relations;
- coherence across resolutions.

The Lean artifacts are intended as consistency checks on formal definitions and do not constitute empirical validation of the physical theory.

⸻

## Theorem Compendium

The repository also includes a theorem compendium documenting the status of all major BST results.

Files are located in:

```text
theorem_compendium/
```

Available versions:

- French: RECUEIL_theoremes_BST
- English: COMPENDIUM_theorems_BST

The compendium provides:

- theorem statements;
- status classification;
- dependencies;
- links to simulations and formal verification artifacts when applicable.

⸻

## Repository hygiene

Do not commit:

- `__pycache__/`;
- `.DS_Store`;
- generated files under `results/summaries/`;
- transient audit notes.
