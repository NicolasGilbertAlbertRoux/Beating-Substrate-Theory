#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 4 — is a HIERARCHY of latent strata functionally NECESSARY? (extends latent reconstruction controls)
Tests the user's resolution-channel axiom: identity reconstruction under MULTI-LEVEL
aliasing should require MULTIPLE latent strata; a single stratum is insufficient.

Setup (synthetic, latent-identity-control style): N entities in a hierarchy coarse(g) x sub(s) x ent(t).
Observable resolves only the COARSE level (entities in a group alias). Latent strata:
z1 resolves subgroup, z2 resolves entity. Reconstruct identity by nearest-prototype.

PRE-REGISTERED (each control CAN fail):
  acc(obs only)        ~ 1/(S*T)  (chance within coarse group)
  acc(obs+z1)          ~ 1/T      (chance within subgroup) -- single stratum insufficient
  acc(obs+z1+z2)       >> single  (hierarchy resolves identity)
  acc(SHUFFLED latent) ~ obs-only (anti-cheat: shuffled strata carry no identity)
  acc(NULL latent)     ~ obs-only
Result = necessity of a hierarchy IFF multi >> single AND shuffled/null collapse to
obs-only. HONEST FRAME: a functional-necessity/possibility result (like latent reconstruction controls), NOT a
claim the universe is multi-strata. Requires numpy.
"""
import numpy as np
rng=np.random.default_rng(0)
G,S,T,d = 5,4,4,8           # 5 coarse groups x 4 subgroups x 4 entities = N=80
N=G*S*T
ents=[(g,s,t) for g in range(G) for s in range(S) for t in range(T)]
coarse=rng.normal(size=(G,d)); sub=rng.normal(size=(G,S,d)); ent=rng.normal(size=(G,S,T,d))
def proto(e):
    g,s,t=e; return np.concatenate([coarse[g], sub[g,s], ent[g,s,t]])   # [obs|z1|z2]
P=np.array([proto(e) for e in ents])                                    # memory prototypes
SL=slice(0,d); Z1=slice(d,2*d); Z2=slice(2*d,3*d)

def accuracy(feat_mask, memory, n_query=25, noise=0.6):
    correct=0; total=0
    for i,e in enumerate(ents):
        for _ in range(n_query):
            q=proto(e)+rng.normal(scale=noise,size=3*d)
            dq=q*feat_mask; dM=memory*feat_mask
            j=int(np.argmin(((dM-dq)**2).sum(1)))
            correct+= (j==i); total+=1
    return correct/total

mask=lambda *sls: np.concatenate([ (np.ones(d) if sl else np.zeros(d)) for sl in sls ])
m_obs   = mask(1,0,0); m_s1=mask(1,1,0); m_s12=mask(1,1,1)
# shuffled latent memory: permute z1,z2 across entities (obs untouched)
perm=rng.permutation(N); Mshuf=P.copy(); Mshuf[:,d:]=P[perm,d:]
# null latent memory: random z1,z2
Mnull=P.copy(); Mnull[:,d:]=rng.normal(size=(N,2*d))

print("="*64); print("BST Stage 4 — hierarchy-of-strata necessity (latent-identity-control style)"); print("="*64)
print(f"N={N} (G={G} x S={S} x T={T}); chance=1/N={1/N:.3f}\n")
print(f"{'condition':28s}{'accuracy':>10}  expectation")
print(f"{'obs only':28s}{accuracy(m_obs,P):>10.3f}  ~1/(S*T)={1/(S*T):.3f}")
print(f"{'obs + z1 (single stratum)':28s}{accuracy(m_s1,P):>10.3f}  ~1/T={1/T:.3f} (insufficient)")
print(f"{'obs + z1 + z2 (hierarchy)':28s}{accuracy(m_s12,P):>10.3f}  >> single (resolves)")
print(f"{'CONTROL shuffled latent':28s}{accuracy(m_s12,Mshuf):>10.3f}  ~obs-only (anti-cheat)")
print(f"{'CONTROL null latent':28s}{accuracy(m_s12,Mnull):>10.3f}  ~obs-only")
print("\nNecessity of a HIERARCHY iff: hierarchy >> single > obs, AND shuffled/null")
print("collapse to ~obs-only (strata carry genuine identity, no cheating).")
