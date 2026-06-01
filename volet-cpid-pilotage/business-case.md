# Business case — Programme Néovolt Grid+ (volet Chef de projet)

> Chiffres calculés (script `business_case.py`), hypothèses explicites et ajustables.

## 1. Coût de la phase 1 (industrialisation du prototype)

| Poste | Coût |
|---|---|
| Équipe data/dev/sécurité (3 profils × 70 j) | 115 500 € |
| Chef de projet (70 j) | 52 500 € |
| Expert architecture/sécurité (25 j) | 18 750 € |
| Prestataire spécialisé (25 j) | 22 500 € |
| Hébergement cloud UE (6 mois) | 21 000 € |
| Licences BI (8 utilisateurs / an) | 9 600 € |
| Licence gouvernance des données (1 an) | 25 000 € |
| Audit de sécurité externe (forfait) | 18 000 € |
| **Sous-total** | **282 850 €** |
| Contingence (15 %) | 42 428 € |
| **TOTAL phase 1** | **325 278 €** |

→ **325 278 €** vs enveloppe **450 000 €** : on tient dans le budget avec **124 722 € de marge** (rassure la DG, qui craint les dérapages).

- Coût d'exploitation récurrent estimé : **76 600 €/an** (cloud + licences), hors équipe run.

## 2. Gain — réduction des pertes sur fraude

- Taux de fraude **observé** : 3.43% (24/700 PDL) → borne basse (seules les fraudes *confirmées* sont connues).
- Consommation médiane : 14.5 kWh/j ≈ 5,285 kWh/an (médiane choisie = prudente, la moyenne est gonflée par les industriels).

Calcul (hypothèses : sous-facturation 35%, prix 0.15 €/kWh, récupération an 1 40%) :
- Fraudes estimées sur le parc : 600,000 × 3.43% = **20,571 PDL**
- Gisement annuel de pertes : **≈ 5 708 016 €**
- **Récupérable dès l'an 1 (détection précoce) : ≈ 2 283 206 €**

*Le modèle capte 54 % des fraudes en investiguant 5 % des compteurs (lift ×10,8) → l'hypothèse de 40 % de récupération an 1 est prudente.*

## 3. Retour sur investissement

- Gain net an 1 (récupéré − exploitation) ≈ **2 206 606 €**
- Investissement phase 1 : 325 278 €
- **Retour sur investissement : ≈ 1.7 mois.**
- Gains additionnels NON chiffrés ici (prudence) : réduction des **achats d'énergie d'équilibrage** (prévision des pics), baisse des **coûts d'incidents**, gain de satisfaction client (facturation).

## 4. Analyse de sensibilité (honnêteté sur les hypothèses)

| Part récupérable an 1 | Gain récupéré | ROI |
|---|---|---|
| 20% | 1 141 603 € | 3.4 mois |
| 30% | 1 712 405 € | 2.3 mois |
| 40% | 2 283 206 € | 1.7 mois |
| 60% | 3 424 810 € | 1.1 mois |

→ Même dans l'hypothèse la plus prudente (20 %), le ROI reste inférieur à un an. La décision est **robuste** aux hypothèses.

## 5. Recommandation de priorisation

**Détection de fraude d'abord, prévision ensuite.** La fraude offre un ROI rapide et mesurable (gisement chiffrable, vérité terrain disponible) qui **finance** la suite ; la prévision (gains réels mais plus diffus) vient en lot 2. Voir le plan de projet.
