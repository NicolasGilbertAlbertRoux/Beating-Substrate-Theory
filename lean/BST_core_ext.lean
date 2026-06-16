/-
  BST_core_ext.lean  (noyau + extensions + robustesse)
  ----------------------------------------------------------------------------
  Lean 4 « core » (AUCUN import, pas de Mathlib).

  HONNÊTETÉ : ce fichier vérifie une COHÉRENCE LOGIQUE INTERNE étant donné des
  définitions. Il n'établit ni vérité empirique, ni physique, ni couche cognitive.
  Les DÉFINITIONS portent le sens ; la PARTIE 3 teste précisément si la définition
  de « persistance » que nous avions choisie (`Separates`) est plus forte que
  celle du manuscrit — et montre qu'elle l'est strictement.

  EXÉCUTION (macOS), sans Mathlib :
    brew install elan-init ; elan default stable ; lean BST_core_ext.lean
  (Les commandes #print axioms en fin de fichier produisent un rapport visible.)
  ----------------------------------------------------------------------------
-/

namespace BST

variable {L O O₁ O₂ R : Type}

/-! ## PARTIE 0 — Noyau -/

@[reducible] def ObsEquiv (obs : L → O) (a b : L) : Prop := obs a = obs b

theorem obsEquiv_refl (obs : L → O) (a : L) : ObsEquiv obs a a := rfl
theorem obsEquiv_symm (obs : L → O) {a b : L}
    (h : ObsEquiv obs a b) : ObsEquiv obs b a := h.symm
theorem obsEquiv_trans (obs : L → O) {a b c : L}
    (h₁ : ObsEquiv obs a b) (h₂ : ObsEquiv obs b c) : ObsEquiv obs a c := h₁.trans h₂

@[reducible] def Limited (obs : L → O) : Prop := ∃ a b : L, a ≠ b ∧ obs a = obs b
@[reducible] def LatentAt (obs : L → O) (a b : L) : Prop := a ≠ b ∧ obs a = obs b

theorem latent_necessity (obs : L → O) (h : Limited obs) :
    ∃ a b : L, LatentAt obs a b :=
  match h with
  | ⟨a, b, hne, hobs⟩ => ⟨a, b, hne, hobs⟩

theorem latent_forced_by_persistence
    (obs₁ : L → O₁) (obs₂ : L → O₂) (a b : L)
    (haliased  : obs₁ a = obs₁ b)
    (hdistinct : obs₂ a ≠ obs₂ b)
    : LatentAt obs₁ a b :=
  ⟨fun h => hdistinct (congrArg obs₂ h), haliased⟩

@[reducible] def Stable (closed persists : Prop) : Prop := closed ∧ persists

theorem closure_persistence_imp_stability {closed persists : Prop}
    (hc : closed) (hp : persists) : Stable closed persists := ⟨hc, hp⟩

/-! ## PARTIE 1 — Hiérarchie de validation et clôture résiduelle -/

structure Validation where
  necessity       : Prop
  nonCheating     : Prop
  persistence     : Prop
  closure         : Prop
  reproducibility : Prop

@[reducible] def Admissible (v : Validation) : Prop :=
  v.necessity ∧ v.nonCheating ∧ v.persistence ∧ v.closure ∧ v.reproducibility

theorem admissible_needs_necessity {v : Validation} (h : Admissible v) : v.necessity := h.1
theorem necessity_gates {v : Validation} (h : ¬ v.necessity) : ¬ Admissible v :=
  fun ha => h ha.1
theorem nonCheating_gates {v : Validation} (h : ¬ v.nonCheating) : ¬ Admissible v :=
  fun ha => h ha.2.1

theorem residual_closure {AllInternalForced HierarchyFixed : Prop}
    (forced : AllInternalForced) (hopen : ¬ HierarchyFixed) :
    AllInternalForced ∧ ¬ HierarchyFixed := ⟨forced, hopen⟩

/-! ## PARTIE 2 — Famille de résolutions : la persistance FORTE (Separates) -/

/-- Persistance FORTE (globale) : la famille distingue toute paire distincte. -/
@[reducible] def Separates (obs : R → L → O) : Prop :=
  ∀ a b : L, (∀ r : R, obs r a = obs r b) → a = b

/-- Sous Separates, le latent n'est jamais absolu (constructif, à vrai contenu). -/
theorem latent_not_absolute (obs : R → L → O) (sep : Separates obs)
    {a b : L} (hne : a ≠ b) : ¬ (∀ r : R, obs r a = obs r b) :=
  fun hall => hne (sep a b hall)

/-- Sous Separates, toute paire distincte est distinguée quelque part (CLASSIQUE). -/
theorem latent_visible_somewhere (obs : R → L → O) (sep : Separates obs)
    {a b : L} (hne : a ≠ b) : ∃ r : R, obs r a ≠ obs r b :=
  Classical.byContradiction fun hnex =>
    hne (sep a b (fun r => Classical.byContradiction (fun hr => hnex ⟨r, hr⟩)))

/-! ## PARTIE 3 — Robustesse : affaiblir la persistance

Persistance FAIBLE, fidèle au manuscrit : une structure DONNÉE (paire a,b) reste
distinguable là où elle apparaît — un simple témoin. -/

/-- Persistance FAIBLE (par paire) : `(a,b)` est distinguée par au moins une résolution. -/
@[reducible] def DistinguishedSomewhere (obs : R → L → O) (a b : L) : Prop :=
  ∃ r : R, obs r a ≠ obs r b

/-- **Nécessité du latent, hypothèse FAIBLE, CONSTRUCTIVE.** Une paire qui persiste
    (témoin) mais est confondue à `r₀` est faite d'états distincts : latente-à-`r₀`,
    réelle. Ne requiert ni `Separates` ni la logique classique — c'est le résultat
    ROBUSTE, fidèle au manuscrit. -/
theorem latent_real_but_hidden (obs : R → L → O) (r₀ : R) {a b : L}
    (hpers : DistinguishedSomewhere obs a b)
    (hmerged : obs r₀ a = obs r₀ b)
    : a ≠ b ∧ obs r₀ a = obs r₀ b :=
  match hpers with
  | ⟨r₁, hr₁⟩ => ⟨fun h => hr₁ (congrArg (obs r₁) h), hmerged⟩

/-- Forte ⟹ faible (pour une paire distincte) : c'est `latent_visible_somewhere`. -/
theorem separates_imp_distinguished (obs : R → L → O) (sep : Separates obs)
    {a b : L} (hne : a ≠ b) : DistinguishedSomewhere obs a b :=
  latent_visible_somewhere obs sep hne

/-! ### Contre-modèle : la réciproque échoue — `Separates` est STRICTEMENT plus forte

Trois états {x,y,z}, une seule résolution qui sépare `x` mais confond `y` et `z`.
La paire (x,y) persiste (faible vraie), pourtant la famille NE sépare PAS (forte fausse). -/

inductive Three | x | y | z

def obsEx : Unit → Three → Bool
  | _, Three.x => true
  | _, Three.y => false
  | _, Three.z => false

/-- Hypothèse FAIBLE satisfaite : (x,y) est distinguée. -/
theorem xy_persists : DistinguishedSomewhere obsEx Three.x Three.y :=
  ⟨(), by decide⟩

/-- Hypothèse FORTE violée : y et z sont confondus partout, alors que y ≠ z. -/
theorem obsEx_not_separates : ¬ Separates obsEx :=
  fun sep => Three.noConfusion (sep Three.y Three.z (fun _ => rfl))

/-- **Conclusion de robustesse.** Il existe un modèle où la persistance FAIBLE
    (par paire) tient sans que la persistance FORTE (Separates) tienne : la seconde
    est donc strictement plus forte. Le résultat-clé (`latent_real_but_hidden`) ne
    dépend que de la première — il est robuste à cet affaiblissement. -/
theorem weak_does_not_imply_strong :
    (DistinguishedSomewhere obsEx Three.x Three.y) ∧ (¬ Separates obsEx) :=
  ⟨xy_persists, obsEx_not_separates⟩

end BST

/-! ## Rapport de vérification (sortie visible : dépendances axiomatiques) -/
#print axioms BST.latent_necessity
#print axioms BST.latent_forced_by_persistence
#print axioms BST.closure_persistence_imp_stability
#print axioms BST.necessity_gates
#print axioms BST.residual_closure
#print axioms BST.latent_not_absolute
#print axioms BST.latent_real_but_hidden
#print axioms BST.latent_visible_somewhere
#print axioms BST.separates_imp_distinguished
#print axioms BST.xy_persists
#print axioms BST.obsEx_not_separates
#print axioms BST.weak_does_not_imply_strong
