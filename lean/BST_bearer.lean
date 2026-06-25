/-
  BST_bearer.lean   (RAFFINEMENT FORMEL SÉPARÉ — exploratoire)
  ----------------------------------------------------------------------------
  Lean 4 « core » (AUCUN import, pas de Mathlib).  BST v1.0 reste close.

  CORRECTION ASSUMÉE. Le fichier précédent montrait que la valeur (niveau 3) est
  INDÉPENDANTE du mécanisme (niveau 2). Il ne montrait PAS qu'elle est « donnée »
  ou « reçue » : c'était une surinterprétation. Le statut ontologique de la valeur
  reste ouvert (brute, relationnelle, portée, ou autre).

  QUESTION (N. Roux). Y a-t-il une différence FORMALISABLE entre :
    (a) une valeur posée comme paramètre externe ;
    (b) une entité capable de PORTER, maintenir, transformer ou abandonner cette valeur ?

  RÉPONSE. Oui. Un *porteur* est une IDENTITÉ PERSISTANTE individuée indépendamment
  de la valeur, à travers laquelle la valeur peut changer. C'est l'identité/persistance
  déjà présente dans le noyau (« ce qui persiste, c'est la cohérence, pas la forme »).

  CE QUE CELA ÉTABLIT (et pas) :
   • Établi : le porteur ≠ la valeur-paramètre. Un porteur transforme sa valeur en
     restant le même (transformation, non remplacement) ; et son identité est
     indépendante de sa valeur (mêmes valeurs, porteurs distincts).
   • NON établi : que le porteur ENGENDRE/FONDE la valeur. Le critère d'identité du
     porteur (`id`) est lui-même POSÉ, non dérivé de la valeur ; et la capacité de
     transformer s'internalise (dynamique sur l'espace des valeurs). Le porteur
     PORTE une signification qu'il n'AUTORISE pas. L'irréductible reste la
     non-dérivabilité de la valeur (statut : Posé), non un pouvoir auto-fondateur.

  EXÉCUTION : brew install elan-init ; elan default stable ; lean BST_bearer.lean
  ----------------------------------------------------------------------------
-/

namespace BST.Bearer

abbrev Route := Bool
abbrev Value := Route → Bool          -- une valuation (niveau 3)

/-- Un *porteur* : un critère d'identité persistant `id` (POSÉ, indépendant de la
    valeur) et une valeur portée à chaque étape `valAt` (qui peut changer). -/
structure Bearer where
  id    : Nat
  valAt : Nat → Value

/-- Transformation (et non remplacement) : le MÊME porteur porte des valeurs
    différentes selon l'étape. -/
@[reducible] def transforms (b : Bearer) (t₁ t₂ : Nat) : Prop := b.valAt t₁ ≠ b.valAt t₂

/-- Un porteur qui transforme effectivement sa valeur tout en restant un seul porteur. -/
def b0 : Bearer where
  id := 0
  valAt := fun n => match n with | 0 => (fun _ => true) | _ => (fun _ => false)

/-- Le même porteur `b0` porte `true` à l'étape 0, `false` à l'étape 1 : la valeur
    a changé, le porteur est resté le même. -/
theorem b0_transforms : transforms b0 0 1 :=
  fun h => Bool.noConfusion (congrFun h true)

/-- Un autre porteur, de valeurs IDENTIQUES à `b0`, mais d'identité distincte. -/
def b1 : Bearer where
  id := 1
  valAt := b0.valAt

theorem same_values : b1.valAt = b0.valAt := rfl
theorem different_bearers : b1.id ≠ b0.id := by decide

/-- **Le porteur n'est pas la valeur-paramètre.** (1) Le même porteur transforme sa
    valeur en restant le même (transformation). (2) Deux porteurs de valeurs
    identiques restent distincts : l'identité du porteur est indépendante de sa
    valeur. Un paramètre nu n'a ni l'une ni l'autre propriété. -/
theorem bearer_distinct_from_parameter :
    (transforms b0 0 1) ∧ (b1.valAt = b0.valAt ∧ b1.id ≠ b0.id) :=
  ⟨b0_transforms, same_values, different_bearers⟩

/-! ### Lecture honnête
  Le résidu que vous pressentiez est réel et FORMALISABLE : c'est le porteur =
  identité persistante individuée indépendamment de la valeur portée. C'est la
  catégorie identité/persistance déjà dans le noyau, vue ici comme support de la
  valeur.

  Mais notez ses limites, sans quoi on glisse encore :
   • le critère d'identité `id` est POSÉ — le porteur requiert qu'on pose une
     identité par-delà la valeur ; il ne la dérive pas ;
   • « transformer » la valeur est une dynamique sur l'espace des valeurs : cela
     s'internalise (règle sur (porteur, valeur)) ; ce n'est pas un pouvoir nouveau ;
   • ce qui demeure irréductible n'est pas le porteur (descriptible) mais la
     NON-DÉRIVABILITÉ de la valeur — son origine/sa signification — statut : Posé.

  En une phrase : le porteur PORTE une signification qu'il n'AUTORISE pas. C'est une
  caractérisation réelle de l'« agent » comme identité persistante porteuse de
  valeur — sobre, dans le programme, et non une volonté se fondant elle-même.
  (La lecture « porteur = identité persistante » est la plus naturelle déjà offerte
  par le programme ; elle n'exclut pas qu'une autre structure — relationnelle ou
  encore non identifiée — caractérise le résidu autrement.) -/

end BST.Bearer

/-! ## Rapport de vérification (dépendances axiomatiques) -/
#print axioms BST.Bearer.b0_transforms
#print axioms BST.Bearer.different_bearers
#print axioms BST.Bearer.bearer_distinct_from_parameter
