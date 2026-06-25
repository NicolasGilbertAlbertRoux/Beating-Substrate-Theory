/-
  BST_motivation.lean   (RAFFINEMENT FORMEL SÉPARÉ — exploratoire)
  ----------------------------------------------------------------------------
  Lean 4 « core » (AUCUN import, pas de Mathlib).  BST v1.0 reste close.

  QUESTION (N. Roux). Trois niveaux :
    (1) routes possibles ; (2) fonction de sélection ; (3) motivation/orientation
    qui rend la sélection signifiante. Le compatibilisme internalise (1) et (2).
    Existe-t-il un modèle où la sélection est ENTIÈREMENT définie, mais où la
    motivation n'est représentée QUE comme un axiome externe ?

  RÉPONSE. Oui — et c'est nécessairement le cas, par le fossé être/devoir-être :
  aucun mécanisme n'entraîne une valeur. Ici, `sel` (niveau 2) est une fonction
  totale ; `val` (niveau 3) est un CHAMP externe que rien dans `sel` ne détermine.

  CE QUE CELA ÉTABLIT (et pas) :
   • Établi : la motivation NE SE RÉDUIT PAS à la sélection (niveaux 2 ≠ 3).
     La valeur est sous-déterminée par le comportement, et la sélection peut
     diverger de la valeur (akrasie). C'est la 1re moitié de votre thèse.
   • NON établi : que l'agent ENGENDRE ou FONDE cette valeur. `val` est un POSÉ
     externe — un donné, pas un pouvoir auto-fondateur. L'irréductibilité de la
     motivation est l'irréductibilité du DONNÉ, non la naissance d'une volonté
     se causant elle-même. « Transformer » `val` pour une raison rouvre la
     régression / l'obstruction diagonale déjà démontrée ailleurs.

  EXÉCUTION : brew install elan-init ; elan default stable ; lean BST_motivation.lean
  ----------------------------------------------------------------------------
-/

namespace BST.Motivation

/-- Niveau 1 — routes possibles. -/
abbrev Route := Bool

/-- Un agent : une SÉLECTION (niveau 2, fonction totale, entièrement définie) et
    une VALUATION (niveau 3, ce qui est tenu pour digne). `val` est un champ que
    l'on doit FOURNIR de l'extérieur : rien dans `sel` ne le calcule. -/
structure Agent where
  sel : Route            -- niveau 2 : la route effectivement sélectionnée
  val : Route → Bool     -- niveau 3 : la route tenue pour digne (axiome externe)

/-! ### Akrasie : sélectionner ≠ tenir-pour-digne
Un agent peut sélectionner une route qu'il ne tient pas pour digne. Donc la
sélection n'est pas « la poursuite de ce qui est valorisé » : (2) et (3) divergent. -/

def akratic : Agent := { sel := true, val := fun r => !r }

theorem akrasia_possible : akratic.val akratic.sel = false := rfl
-- la route choisie (true) n'est pas tenue pour digne (val true = !true = false)

/-! ### Sous-détermination : même sélection, valeurs opposées
Deux agents au comportement de sélection IDENTIQUE, mais à valuation contraire.
Donc la valeur n'est pas une fonction de la sélection : (3) est libre de (2). -/

def agentA : Agent := { sel := true, val := fun _ => true }
def agentB : Agent := { sel := true, val := fun _ => false }

theorem same_selection : agentA.sel = agentB.sel := rfl
theorem different_value : agentA.val ≠ agentB.val :=
  fun h => Bool.noConfusion (congrFun h true)

/-- **La motivation ne se réduit pas à la sélection.** La sélection ne détermine
    pas la valeur (même `sel`, `val` opposées) et la sélection peut diverger de la
    valeur (akrasie). La motivation (niveau 3) n'entre donc que comme champ externe. -/
theorem motivation_not_reducible_to_selection :
    (agentA.sel = agentB.sel ∧ agentA.val ≠ agentB.val)
  ∧ (akratic.val akratic.sel = false) :=
  ⟨⟨same_selection, different_value⟩, akrasia_possible⟩

/-! ### Mais la valeur reste un DONNÉ, pas un pouvoir
`val` est un champ fourni de l'extérieur. Le modèle ne contient AUCUNE opération
par laquelle l'agent engendrerait sa propre `val` : il la reçoit. « Assumer » `val`
serait une attitude de plus (un autre champ posé) ; « transformer » `val` pour une
raison appellerait une méta-valuation (régression) ou serait arbitraire, et la
version auto-fondatrice est exactement l'impossibilité diagonale déjà démontrée
(`no_universal_self_representation`). L'irréductibilité prouvée ici est donc celle
du donné — non celle d'une volonté se fondant elle-même. -/

end BST.Motivation

/-! ## Rapport de vérification (dépendances axiomatiques) -/
#print axioms BST.Motivation.akrasia_possible
#print axioms BST.Motivation.different_value
#print axioms BST.Motivation.motivation_not_reducible_to_selection
