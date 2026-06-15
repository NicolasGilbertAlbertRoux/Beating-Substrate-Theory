#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
"""
BST canonical supplementary script: bst_metrics

Category: shared metrics utility

Lexicon alignment:
- observable and latent are reconstruction statuses, not separate ontologies;
- memory is persistence of reconstructive traces;
- selection reduces reconstruction possibilities;
- arbitration resolves or orients remaining admissible possibilities;
- closure denotes dynamical coherence across evolution and/or resolution.

This script is retained as a supplementary control for the final BST repository.
It is not part of the canonical BST stage001-stage086 chain unless explicitly
called by reproduce.py.
"""

import numpy as np


def dominance(target_score: float, competitor_scores: np.ndarray) -> float:
    """Return target score minus the strongest non-target score."""
    if competitor_scores.size == 0:
        raise ValueError("competitor_scores must not be empty")
    return float(target_score - np.max(competitor_scores))


def recovered(target_score: float, competitor_scores: np.ndarray) -> int:
    """Return 1 if the target strictly beats all non-target candidates."""
    return int(dominance(target_score, competitor_scores) > 0.0)


def recovery_rate(recovered_values: np.ndarray) -> float:
    """Return empirical mean recovery rate."""
    if recovered_values.size == 0:
        raise ValueError("recovered_values must not be empty")
    return float(np.mean(recovered_values))
