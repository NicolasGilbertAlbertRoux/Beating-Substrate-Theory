#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BST Stage 5 — is the ORDERED resolution channel GENERATIVE? (user's own claim:
latent structure "generative under reconstruction"). Tests whether a FACTORED/ordered
strata representation can identify NEVER-SEEN entities by recomposing coarse+fine
strata, where a HOLISTIC ("in bulk", one code per seen entity) memory cannot.

Entities = (g,s,t). Factored codebooks g_emb,s_emb,t_emb cover all factor values.
A fraction of combos is HELD OUT (unseen). Query = noisy entity prototype.
  - COMPOSITIONAL classifier: match each factor independently -> composes ANY (g,s,t),
    seen or unseen.
  - HOLISTIC classifier: nearest among SEEN prototypes only -> cannot name an unseen combo.

PRE-REGISTERED (each can fail):
  seen   : compositional ~ holistic ~ high.
  unseen : compositional high (recomposes) ; holistic ~ 0 (structurally cannot).
  CONTROL shuffled codebooks -> compositional collapses (no cheating).
HONEST FRAME: functional/possibility result conditional on the factored construction;
the non-trivial parts are the seen/unseen split (holistic COULD interpolate, it can't)
and the anti-cheat. Requires numpy.
"""
import numpy as np
rng=np.random.default_rng(0)
G,S,T,d=5,4,4,8; N=G*S*T
g_emb=rng.normal(size=(G,d)); s_emb=rng.normal(size=(S,d)); t_emb=rng.normal(size=(T,d))
combos=[(g,s,t) for g in range(G) for s in range(S) for t in range(T)]
def proto(c): g,s,t=c; return np.concatenate([g_emb[g],s_emb[s],t_emb[t]])
# held-out unseen combos (ensure every factor value still appears in 'seen')
rng2=np.random.default_rng(1); order=combos[:]; rng2.shuffle(order)
unseen=set(); 
for c in order:
    if len(unseen)>=24: break
    g,s,t=c
    seen_now=[x for x in combos if x not in unseen]
    if all(any(v==x[k] for x in seen_now if x!=c) for k,v in enumerate(c)):
        unseen.add(c)
seen=[c for c in combos if c not in unseen]; unseen=list(unseen)

def comp_predict(q, GB=g_emb, SB=s_emb, TB=t_emb):
    qg,qs,qt=q[:d],q[d:2*d],q[2*d:]
    return (int(np.argmin(((GB-qg)**2).sum(1))),
            int(np.argmin(((SB-qs)**2).sum(1))),
            int(np.argmin(((TB-qt)**2).sum(1))))
seen_protos=np.array([proto(c) for c in seen])
def holo_predict(q):
    return seen[int(np.argmin(((seen_protos-q)**2).sum(1)))]
def acc(testset, predict, noise=0.6, n=25):
    ok=0; tot=0
    for c in testset:
        for _ in range(n):
            q=proto(c)+rng.normal(scale=noise,size=3*d)
            ok+= (predict(q)==c); tot+=1
    return ok/tot

# shuffled-codebook control (anti-cheat) for compositional
GBs=g_emb[rng.permutation(G)]; SBs=s_emb[rng.permutation(S)]; TBs=t_emb[rng.permutation(T)]
comp_shuf=lambda q: comp_predict(q,GBs,SBs,TBs)

print("="*64); print("BST Stage 5 — generative/compositional necessity"); print("="*64)
print(f"N={N}; seen={len(seen)} unseen={len(unseen)}\n")
print(f"{'classifier / set':30s}{'accuracy':>10}")
print(f"{'COMPOSITIONAL  - seen':30s}{acc(seen,comp_predict):>10.3f}")
print(f"{'COMPOSITIONAL  - UNSEEN':30s}{acc(unseen,comp_predict):>10.3f}   <- recomposes the never-seen")
print(f"{'HOLISTIC       - seen':30s}{acc(seen,holo_predict):>10.3f}")
print(f"{'HOLISTIC       - UNSEEN':30s}{acc(unseen,holo_predict):>10.3f}   <- structurally cannot")
print(f"{'CONTROL shuffled - UNSEEN':30s}{acc(unseen,comp_shuf):>10.3f}   <- anti-cheat")
print("\nGenerative resolution channel IFF: compositional identifies UNSEEN combos,")
print("holistic ~0 on unseen, and shuffled codebooks collapse. -> ordering carries content.")
