#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 58 — Kleinert curvature sector: γ_PPN=1 / full Einstein (CONDITIONAL, an added field).
A spin-2 curvature field DECOUPLED from elastic c_T (so it can travel at c, escaping the S57 stability
bound), with the trace-reversed coupling box h_mn = -16piG (T_mn - 1/2 eta_mn T). For a static mass the
trace-reversed source has S_00 = S_11 = S_22 = S_33 = rho/2 (all EQUAL) -> spatial curvature equals temporal
-> γ_PPN = 1 -> full Einstein light bending (factor 1+γ_PPN = 2 = 4GM/bc^2), vs a scalar (γ_PPN=0, half).
Being light-speed, Weinberg-Deser then forces universal coupling => a genuine graviton.
HONEST RESERVE: standard linearized GR + Kleinert's defect-curvature identification (established). It is an
ADDED sector beyond the minimal substrate -> status CONDITIONAL: "Einstein gravity emerges IF the Kleinert
curvature field is adjoined", NOT forced by the elastic substrate alone. S57 explains exactly why it must be
added (the elastic spin-2 mode is sub-luminal in any stable medium).
"""
import numpy as np
# Kleinert curvature sector (CONDITIONAL: an ADDED field, decoupled from elastic c_T, free to travel at c).
# A spin-2 field with the trace-reversed coupling box h_mn = -16piG (T_mn - 1/2 eta_mn T). For a static
# mass, does it source the SPATIAL potential equally to the temporal one (h_ij = h_00 => γ_PPN=1 => full
# Einstein light bending), unlike a scalar (γ_PPN=0, half)? eta=diag(-1,1,1,1).
eta=np.diag([-1.,1,1,1]); rho=1.0
T=np.zeros((4,4)); T[0,0]=rho                      # static dust: only T_00
Ttr=np.einsum('ab,ab->',np.linalg.inv(eta),T)      # trace T = eta^{mn} T_mn
S=T-0.5*eta*Ttr                                     # trace-reversed source (the spin-2/graviton source)
print("="*72); print("BST Stage 58 — Kleinert curvature sector: does the spin-2 source give γ_PPN=1?"); print("="*72)
print(f"\n  static mass, trace-reversed source S_mn = T_mn - 1/2 eta_mn T  (trace T = {Ttr:+.2f} rho):")
print(f"    S_00 = {S[0,0]:+.3f} rho   S_11 = {S[1,1]:+.3f} rho   S_22 = {S[2,2]:+.3f}   S_33 = {S[3,3]:+.3f}")
γ_PPN_tensor = S[1,1]/S[0,0]
print(f"  => spatial/temporal source ratio γ_PPN = S_11/S_00 = {γ_PPN_tensor:.3f}  (all four EQUAL => γ_PPN=1)")
# scalar comparison: a scalar couples to the trace only -> sources h_00, no spatial h_ij
print(f"\n  scalar mediator (couples to trace T only): sources h_00, but h_ii = 0  => γ_PPN = 0")
print(f"\n  light-bending factor (1+γ_PPN):  tensor/Kleinert = {1+γ_PPN_tensor:.1f} (EINSTEIN)   scalar = 1.0 (HALF)")
print(f"  deflection alpha = (1+γ_PPN) * 2GM/(b c^2):  tensor = 4GM/bc^2 (Einstein)   scalar = 2GM/bc^2")
print("\n  => the trace-reversed spin-2 source sets all four diagonal potentials EQUAL -> spatial curvature")
print("  equals temporal -> γ_PPN=1, full Einstein light bending. The curvature field, decoupled from c_T,")
print("  CAN be light-speed (escaping the S57 stability bound) and Weinberg-Deser then forces universal")
print("  coupling = a genuine graviton. HONEST: this is standard linearized GR + Kleinert's defect-curvature")
print("  identification (established). It is an ADDED sector beyond the minimal substrate -> status CONDITIONAL")
print("  ('Einstein gravity emerges IF the Kleinert curvature field is adjoined'), NOT forced by elasticity alone.")
