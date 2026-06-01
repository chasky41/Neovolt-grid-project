# Rapport — Détection d'anomalies / fraude (volet Data Scientist)

## 1. Feature engineering (1 profil par PDL)

- 700 PDL profilés, 10 variables explicatives
- Variables : conso_moy/med/cv, pct_zero/manquant/aberrant, ratio_puissance, corr_temp, trend, ratio_chute (conso 2e moitié / 1re moitié)

- Vérité terrain : 24 fraudes / 700 PDL (taux de base 3.43%)

## 2. Modèle — Isolation Forest (non supervisé)

- IsolationForest(n_estimators=300, contamination=0.06, random_state=42)
- Score = -decision_function (normalisé plus bas), trié décroissant = priorité d'enquête

## 3. Règles métier explicables (transparence de la décision)

- Indicateurs : chute durable (sous-comptage), ratio conso/puissance, % jours à zéro,
  décorrélation à la température. Chaque suspect est accompagné de SA raison.

## 4. Évaluation sur les 24 fraudes confirmées

- **Average Precision (PR-AUC) : 0.331** (vs 0.034 en aléatoire)

| Top-N investigués | Fraudes captées | Rappel | Précision | Lift vs aléatoire |
|---|---|---|---|---|
| 25 (4%) | 8/24 | 33% | 32% | ×9.3 |
| 35 (5%) | 13/24 | 54% | 37% | ×10.8 |
| 50 (7%) | 18/24 | 75% | 36% | ×10.5 |
| 70 (10%) | 19/24 | 79% | 27% | ×7.9 |
| 100 (14%) | 20/24 | 83% | 20% | ×5.8 |

- Figure : `volet-datascience/figures/evaluation_fraude.png`

## 5. Artefacts produits (MLOps)

- `suspects_priorises.csv` : 700 PDL triés par suspicion + raison explicable
- `models/isolation_forest.joblib` : modèle versionné
- `models/features.csv` : table de features (reproductibilité de l'expérience)

## 6. Top 10 des PDL à investiguer en priorité

| Rang | PDL | Type | Score | Connu fraude | Raison |
|---|---|---|---|---|---|
| 1 | PDL-000242 | industriel | 0.1987 | OUI | profil atypique (modèle) |
| 2 | PDL-000445 | professionnel | 0.1963 | — | conso décorrélée de la température |
| 3 | PDL-000556 | professionnel | 0.1957 | — | profil atypique (modèle) |
| 4 | PDL-000526 | industriel | 0.1706 | — | profil atypique (modèle) |
| 5 | PDL-000645 | residentiel | 0.1662 | OUI | profil atypique (modèle) |
| 6 | PDL-000194 | professionnel | 0.1633 | — | profil atypique (modèle) |
| 7 | PDL-000003 | residentiel | 0.1627 | — | profil atypique (modèle) |
| 8 | PDL-000604 | residentiel | 0.1602 | — | profil atypique (modèle) |
| 9 | PDL-000596 | residentiel | 0.159 | — | profil atypique (modèle) |
| 10 | PDL-000555 | professionnel | 0.1575 | OUI | conso décorrélée de la température |

## 7. Limites & éthique (à défendre)

- Le score est une **aide à la priorisation**, pas un verdict : décision finale humaine (exigence RGPD sur la décision automatisée).
- Risque de **faux positifs** : un logement vacant ou un changement de vie (télétravail, déménagement) ressemble à une chute de conso. Coût d'un faux positif (client accusé à tort) ≠ coût d'un faux négatif (fraude manquée).
- **Biais** : vérifier que le modèle ne sur-cible pas un segment (ex. petits foyers). Une AIPD est requise avant tout usage réel.
- 24 labels seulement : l'évaluation est indicative, pas une garantie de performance en réel.
