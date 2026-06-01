# Rapport de nettoyage des données — Néovolt Grid+

_Source brute : `C:\Users\DEll\Desktop\sujet-examenS2\donnees`_

## 1. Relevés de consommation

- Lignes brutes : **512,986**
- Règle 1 — doublons exacts supprimés : **1,286** ; conflits (id_pdl,date) résolus par médiane : **0**
- Lignes après déduplication : **511,700**
- Règle 2 — valeurs négatives mises à NaN (erreur capteur) : **1,032**
- Règle 3 — relevés à 0 conservés et flagués (vacance possible) : **637**
- Règle 4 — aberrants hauts flagués (médiane + 10·MAD, **par PDL**) : **2,118** (non supprimés : une conso élevée peut être légitime pour un industriel)
- Règle 5 — relevés manquants (NaN, dont négatifs convertis) conservés et signalés : **7,870** (1.54%)

**Taux de relevés directement exploitables : 98.46%**

## 2. Enrichissement (jointures)

- Jointure compteur : 0 relevés sans compteur correspondant
- Jointure client : sur id_client
- Jointure météo (zone, date) : 0 relevés sans météo
- Variables calendaires ajoutées : annee, mois, jour_semaine, weekend
- Table enrichie : **511,700 lignes × 24 colonnes**

## 3. Fichiers produits

- `data/processed/releves_propres.csv` (511,700 lignes)
- `data/processed/conso_enrichie.csv` (511,700 lignes, table d'analyse)
