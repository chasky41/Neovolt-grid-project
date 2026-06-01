# Volet ILD — Ingénierie Logiciel & Data Engineering

**Rôle dans Néovolt Grid+ :** les fondations. La chaîne qui ingère les relevés, les
fiabilise, les stocke et les **expose par une API** aux autres volets (Analyst, Data
Scientist, dashboards). Sans ces fondations, les analyses et les modèles restent dans
un notebook isolé.

## Chaîne de données (prototype)

```
CSV bruts (donnees/)
   │  scripts/02_nettoyage.py        ← qualité : doublons, négatifs, aberrants, manquants
   ▼
data/processed/releves_propres.csv + conso_enrichie.csv
   │  volet-ild-dataeng/build_warehouse.py
   ▼
data/processed/neovolt.db  (SQLite — schéma étoile : faits + dimensions + tables métier)
   │  volet-ild-dataeng/api/main.py
   ▼
API FastAPI (REST + Swagger /docs)  ← consommée par dashboards, modèles, applis
```

> **Choix assumés** — SQLite + FastAPI pour un prototype **qui tourne** en zéro
> installation. La cible industrielle vise **PostgreSQL hébergé en UE** (souveraineté),
> une ingestion par lots/flux (Airflow/Kafka) et un déploiement conteneurisé. Le code
> (pandas + SQL standard) est **portable** vers PostgreSQL → réversibilité, pas de lock-in.
> Le **SCADA reste isolé** : aucune connexion directe.

## Reproduire de bout en bout

```bash
# Depuis la racine du projet (neovolt-grid-plus/)
python -m venv .venv
.venv\Scripts\activate                 # Windows
pip install -r requirements.txt

# 1) Nettoyage + enrichissement   (génère data/processed/*.csv + rapport)
python scripts/02_nettoyage.py

# 2) Construction de l'entrepôt    (génère data/processed/neovolt.db)
python volet-ild-dataeng/build_warehouse.py

# 3) Lancer l'API  (se placer DANS api/ car le dossier parent a des tirets)
cd volet-ild-dataeng/api
..\..\.venv\Scripts\uvicorn.exe main:app --reload --port 8000
# -> http://127.0.0.1:8000/docs   (documentation interactive Swagger)

# 4) Tests de l'API (smoke test, sans serveur)
..\..\.venv\Scripts\python.exe test_smoke.py
```

## Endpoints

| Méthode | Route | Description | Consommateur |
|---|---|---|---|
| GET | `/health` | État API + entrepôt (période, volumétrie) | supervision |
| GET | `/zones` | Zones + nb de PDL | tous |
| GET | `/pdl/{id}` | Fiche PDL (compteur + client) | relation client |
| GET | `/pdl/{id}/consommation` | Série quotidienne d'un PDL (+ flags qualité) | Data Scientist |
| GET | `/consommation/par-zone` | Conso agrégée par zone/jour | dashboard exploitation |
| GET | `/qualite` | Indicateurs qualité (flags) | gouvernance |
| GET | `/fraude` | Cas de fraude confirmés (données sensibles) | Data Scientist |
| GET | `/incidents` | Synthèse incidents réseau | dashboard exploitation |

## Sécurité (à venir — coordination volet Cyber)
- Authentification/autorisation sur les endpoints (les données conso sont personnelles).
- L'endpoint `/fraude` expose des données sensibles → accès restreint + journalisation.
- Conteneurisation (Docker) + scan de dépendances dans la CI (DevSecOps).

## Statut
- [x] Pipeline de nettoyage documenté + rapport avant/après
- [x] Entrepôt SQLite (8 tables, index)
- [x] API FastAPI (8 endpoints) + smoke test 9/9
- [ ] Conteneurisation Docker + docker-compose (Postgres cible)
- [ ] Authentification + intégration des résultats des modèles (prévision/fraude)
