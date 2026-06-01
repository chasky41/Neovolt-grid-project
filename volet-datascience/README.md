# Volet Data Scientist — Intelligence de la solution

**Rôle :** là où l'analyste décrit ce qui s'est passé, le data scientist **prédit** et
**détecte ce qui sort de l'ordinaire**. Cas d'usage traité ici : **détection
d'anomalies / fraude** sur les compteurs (cas d'usage cœur du prototype).

## Détection de fraude — `detection_fraude.py`

### Démarche
Seulement **24 fraudes confirmées** sur 700 PDL → trop peu pour de la classification
supervisée. On traite le problème en **détection d'anomalies non supervisée**
(Isolation Forest) : les 24 cas servent à **évaluer**, pas à entraîner.

1. **Feature engineering** : un profil par PDL sur 2 ans (comportement, pas magnitude).
   Variables clés *scale-invariantes* : `ratio_chute` (conso 2ᵉ moitié / 1ʳᵉ — signature
   du sous-comptage), `ratio_puissance` (conso vs puissance souscrite), `pct_zero`,
   `corr_temp` (décorrélation à la température), `conso_moy_rel` (relatif au groupe de pairs).
2. **Isolation Forest** (300 arbres, contamination 6 %) → score d'anomalie.
3. **Règles métier explicables** : chaque suspect est accompagné de **sa raison**.
4. **Score combiné** → liste priorisée des PDL à investiguer.

### Résultats (évaluation sur les 24 fraudes)
| Budget enquête | Fraudes captées | Rappel | Précision | Lift |
|---|---|---|---|---|
| Top-35 (5 %) | 13/24 | 54 % | 37 % | **×10,8** |
| Top-50 (7 %) | 18/24 | **75 %** | 36 % | ×10,5 |
| Top-100 (14 %) | 20/24 | 83 % | 20 % | ×5,8 |

**Average Precision (PR-AUC) = 0,331** vs 0,034 en aléatoire (≈ ×10).
→ En investiguant **5 % des compteurs**, Néovolt capte **plus de la moitié des fraudes** —
~11× plus efficace qu'un contrôle au hasard. Base directe du **ROI** (volet CPID).

### Point clé défendable
Détecter *par rapport au groupe de pairs* (un industriel comparé aux industriels) plutôt
qu'en absolu : sinon le modèle flague les gros consommateurs (= être industriel n'est pas
une fraude). Ce choix a **doublé** la performance (AP 0,186 → 0,331).

### Éthique (à défendre — pèse dans la note)
- Le score est une **aide à la priorisation, pas un verdict** : décision finale **humaine**
  (exigence RGPD sur la décision automatisée). Une **AIPD** est requise avant usage réel.
- **Faux positifs** : un logement vacant / un changement de vie ressemble à une chute de
  conso. Coût d'un faux positif (client accusé à tort) ≠ coût d'un faux négatif.
- **Biais** : vérifier que le modèle ne sur-cible pas un segment (petits foyers).

## Exécuter
```bash
python scripts/02_nettoyage.py            # prérequis : conso_enrichie.csv
python volet-datascience/detection_fraude.py
# -> docs/rapport-detection-fraude.md, figures/evaluation_fraude.png, suspects_priorises.csv
```

## MLOps
- Modèle versionné : `models/isolation_forest.joblib` (graine fixée, reproductible).
- Table de features : `models/features.csv`.
- `random_state=42` partout → expérience rejouable. En cible : MLflow pour le suivi.

## À venir
- [ ] **Prévision de consommation** (série temporelle + météo) pour l'achat d'énergie.
- [ ] Intégration du score de fraude dans l'API (endpoint `/fraude/suspects`, accès restreint).
- [ ] Assistant IA expliquant une anomalie en langage naturel (piste d'innovation).
