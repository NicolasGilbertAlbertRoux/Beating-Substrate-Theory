# BST Lean Formalization

This directory contains the formal verification artifacts associated with Beating Substrate Theory (BST).

The purpose of these files is not to reproduce physical experiments or numerical simulations, but to verify the logical consistency of selected conceptual structures appearing in the theory.

⸻

## Files

**BST_core_ext.lean**

Core formalization of:

- latent necessity;
- persistence;
- closure;
- stability;
- observable/latent distinction;
- anti-cheating constraints.

Most results are constructive and require no additional axioms.

**BST_coherence.lean**

Extended formalization of persistence as cross-resolution coherence.

This file establishes that:

- distinguishability (separation);
- coherence (gluing);

are logically independent notions.

It provides formally verified counterexamples showing that coherence cannot be reduced to distinguishability.

⸻

## Scope

The Lean formalization verifies logical consequences of explicit definitions.

It does not establish empirical validity, physical correctness, or experimental confirmation.

As throughout BST, a distinction is maintained between:

- demonstrated formal results;
- calibrated quantities;
- open questions.

⸻

## Running

Example:

```bash
lean BST_core_ext.lean
lean BST_coherence.lean
```

The output reports theorem verification status and axiom dependencies.