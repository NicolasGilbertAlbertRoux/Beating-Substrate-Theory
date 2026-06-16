/-
  BST_coherence.lean   (RAFFINEMENT FORMEL SÉPARÉ — exploratoire)
  ----------------------------------------------------------------------------
  Lean 4 « core » (AUCUN import, pas de Mathlib).

  CADRE. BST v1.0 (BST_core_ext.lean) reste complète et inchangée. Ce fichier
  est un raffinement SÉPARÉ. Objectif : tester si la « persistance » peut être
  formulée non plus comme DISTINGUABILITÉ (séparation), mais comme COHÉRENCE
  inter-résolutions (recollement, à la faisceau) — pour rejoindre plus
  fidèlement la phrase centrale du manuscrit :
        « ce qui persiste, c'est la cohérence, pas la forme ».

  STATUT. Proposition de modélisation, exploratoire. Le manuscrit ne définit pas
  formellement la persistance ; « persistance = recollement » est une lecture
  fidèle PROPOSÉE, à valider, non un fait établi.

  RÉSULTAT. La cohérence (recollement) ne se réduit PAS à la distinguabilité
  (séparation) : les deux notions sont logiquement INDÉPENDANTES (deux
  contre-modèles ci-dessous). Donc le noyau v1.0, qui formalisait la persistance
  comme séparation, ne capturait qu'une moitié de la cohérence.

  EXÉCUTION (macOS) : brew install elan-init ; elan default stable ;
                      lean BST_coherence.lean
  ----------------------------------------------------------------------------
-/

namespace BST.Coherence

/-- Un *système de formes sur un recouvrement à deux pièces*. `G` = formes sur le
    tout (⊤) ; `A`, `B` = formes sur les deux pièces ; `rA`, `rB` = restrictions.
    (Recouvrement à intersection vide : toute famille locale `(a,b)` est compatible.) -/
structure Cover where
  G  : Type
  A  : Type
  B  : Type
  rA : G → A
  rB : G → B

/-- La restriction conjointe d'une forme globale vers ses deux formes locales. -/
def restrict (c : Cover) (g : c.G) : c.A × c.B := (c.rA g, c.rB g)

/-- **Séparation** (= distinguabilité, la persistance de v1.0) : une forme globale
    est entièrement déterminée par ses formes locales. -/
def Separated (c : Cover) : Prop :=
  ∀ g g' : c.G, restrict c g = restrict c g' → g = g'

/-- **Recollement** (= cohérence) : toute famille locale compatible `(a,b)`
    s'assemble en une forme globale. C'est une condition d'EXISTENCE. -/
def Glues (c : Cover) : Prop :=
  ∀ (a : c.A) (b : c.B), ∃ g : c.G, restrict c g = (a, b)

/-! ### Contre-modèle 1 : séparé mais NE recolle PAS
`G=A=B=Bool`, restrictions identité. Une forme globale est déterminée par ses
restrictions (séparé), mais la famille locale `(true, false)` ne se recolle pas
(aucun `g` n'est à la fois `true` et `false`). -/

def boolCover : Cover where
  G := Bool; A := Bool; B := Bool; rA := id; rB := id

theorem boolCover_separated : Separated boolCover :=
  fun _ _ h => congrArg Prod.fst h

theorem boolCover_not_glues : ¬ Glues boolCover :=
  fun glue =>
    match glue true false with
    | ⟨_, hg⟩ =>
        Bool.noConfusion ((congrArg Prod.fst hg).symm.trans (congrArg Prod.snd hg))

/-! ### Contre-modèle 2 : recolle mais N'est PAS séparé
`G=Bool`, `A=B=Unit`. Les restrictions oublient tout : la seule famille locale
`((),())` se recolle (par `true`), mais `true` et `false` ont les mêmes
restrictions sans être égaux (non séparé). -/

def collapseCover : Cover where
  G := Bool; A := Unit; B := Unit; rA := fun _ => (); rB := fun _ => ()

theorem collapseCover_glues : Glues collapseCover :=
  fun a b => ⟨true, by cases a; cases b; rfl⟩

theorem collapseCover_not_separated : ¬ Separated collapseCover :=
  fun sep => Bool.noConfusion (sep true false rfl)

/-! ### Conclusion : cohérence ⧸⟹⧸ distinguabilité (indépendance) -/

/-- **La cohérence ne se réduit pas à la distinguabilité.** Recollement et
    séparation sont logiquement indépendants : un modèle séparé peut ne pas
    recoller, et un modèle qui recolle peut n'être pas séparé. La persistance
    formalisée en v1.0 (séparation) ne capturait donc qu'une moitié de ce que le
    manuscrit appelle cohérence. -/
theorem coherence_not_reducible_to_distinguishability :
    (Separated boolCover ∧ ¬ Glues boolCover)
  ∧ (Glues collapseCover ∧ ¬ Separated collapseCover) :=
  ⟨⟨boolCover_separated, boolCover_not_glues⟩,
   ⟨collapseCover_glues, collapseCover_not_separated⟩⟩

/-! ### Illustration positive : « la forme varie, l'organisation persiste »
`G=Bool×Bool`, `A=B=Bool`, restrictions = projections. La forme globale
`(true,false)` a des formes locales DIFFÉRENTES (`true` sur A, `false` sur B),
et pourtant c'est UNE seule organisation globale. La forme varie ; l'unité
(la cohérence des restrictions) est ce qui persiste. -/

def prodCover : Cover where
  G := Bool × Bool; A := Bool; B := Bool; rA := Prod.fst; rB := Prod.snd

/-- La même organisation a des formes distinctes selon la résolution. -/
theorem prodCover_form_varies :
    prodCover.rA (true, false) ≠ prodCover.rB (true, false) :=
  fun h => Bool.noConfusion h

end BST.Coherence

/-! ## Rapport de vérification (dépendances axiomatiques) -/
#print axioms BST.Coherence.boolCover_separated
#print axioms BST.Coherence.boolCover_not_glues
#print axioms BST.Coherence.collapseCover_glues
#print axioms BST.Coherence.collapseCover_not_separated
#print axioms BST.Coherence.coherence_not_reducible_to_distinguishability
#print axioms BST.Coherence.prodCover_form_varies
