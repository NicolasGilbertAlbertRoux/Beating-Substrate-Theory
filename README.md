# Beating Substrate Theory — Reproducible Scripts

This repository contains the reproducible numerical and algorithmic scripts associated with **Beating Substrate Theory**.

Canonical repository URL:

```text
https://github.com/NicolasGilbertAlbertRoux/Beating-Substrate-Theory.git
```

## Scope

The repository contains the executable reproduction layer of the framework:

- canonical stages `stage001` through `stage086`;
- memory / latent reconstruction controls;
- supplementary checks for closure, observable equivalence, gauge-structure compatibility, resolution invariance, and topological selection.

The manuscript itself is not included in this repository at this stage.

## Structure

```text
Beating-Substrate-Theory/
├── README.md
├── LICENSE
├── requirements.txt
├── reproduce.py
├── scripts/
└── results/
    └── summaries/
```

`results/summaries/` is the canonical output location for generated result files.  
The canonical BSF-derived stage scripts do not generate persistent files. Supplementary and control scripts may generate CSV, JSON, or PNG summaries under `results/summaries/`.

Generated result files are ignored by Git by default. They can be regenerated with `reproduce.py`.

## Installation

```bash
pip install -r requirements.txt
```

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

## Validation status

Functional reproduction has been confirmed by a complete local run reporting `103/103 script(s) ran cleanly`.

Qualitative interpretation remains governed by the manuscript: numerical scripts reproduce numerical or algorithmic checks; conceptual results must remain traceable through definitions, dependency structure, and explicit argumentation.

## Repository hygiene

Do not commit:

- `__pycache__/`;
- `.DS_Store`;
- generated files under `results/summaries/`;
- transient audit notes.
