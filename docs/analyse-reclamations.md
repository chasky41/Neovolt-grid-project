# Analyse des réclamations clients (NLP) — Néovolt Grid+ (volet Data Analyst)

- 3,000 réclamations, satisfaction moyenne **2.45/5** (médiane 2).
- Part de clients insatisfaits (note ≤ 2) : **53%**.

## 1. Thèmes dominants (catégorisation métier)

| Thème | Nb réclamations | Part | Satisfaction moyenne |
|---|---|---|---|
| facturation | 853 | 28% | 2.00/5 |
| coupure/panne | 771 | 26% | 2.05/5 |
| compteur | 764 | 25% | 2.20/5 |
| donnees/RGPD | 445 | 15% | 2.63/5 |
| relation client | 283 | 9% | 2.89/5 |
| raccordement | 256 | 9% | 3.06/5 |

- **Thème le plus pénalisant : « facturation » (2.00/5)** → priorité relation client.
- Le thème « donnees/RGPD » concerne 445 réclamations : signal de conformité à ne pas négliger (lien volet éthique/DPO).

## 2. Vérification data-driven (TF-IDF + KMeans, k=6)

Top mots-clés par cluster (thèmes émergents) :

- Cluster 0 (1024 récl., satisf 2.87/5) : depuis, nouveau, technicien, raccordement, multiplient, fiabilise
- Cluster 1 (419 récl., satisf 2.77/5) : service, secteur, information, plusieurs, inadmissible, heures
- Cluster 2 (274 récl., satisf 2.07/5) : veux, trop, percu, remboursement, fois, deux
- Cluster 3 (294 récl., satisf 2.01/5) : verifier, euros, montant, rapport, anormalement, habituelle
- Cluster 4 (498 récl., satisf 2.28/5) : consommation, compteur, transmission, rgpd, accord, interroge
- Cluster 5 (491 récl., satisf 1.93/5) : demande, echeancier, regularisation, incomprehensible, detaillees, explications

## 3. Satisfaction par canal

- courrier : 2.41/5 (770 réclamations)
- email : 2.48/5 (742 réclamations)
- espace_client : 2.42/5 (737 réclamations)
- telephone : 2.48/5 (751 réclamations)

## Recommandations (data storytelling)

1. **Agir en priorité sur « facturation »** : c'est le thème le plus corrélé à l'insatisfaction. Un plan d'action ciblé remonterait la satisfaction globale.
2. **Tracer les réclamations RGPD** comme un indicateur de conformité suivi par le DPO.
3. **Relier réclamations « coupure » et incidents réseau** (volet exploitation) pour vérifier que les zones les plus touchées correspondent aux incidents enregistrés.

## Figures produites

- `06_themes_reclamations.png`, `07_satisfaction_par_theme.png`
