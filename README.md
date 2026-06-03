# Néovolt Grid+ — Prototype & dossier de cadrage

Réponse de l'équipe projet au programme **Néovolt Grid+** : moderniser l'exploitation
des données du réseau de distribution d'énergie de Néovolt (≈600 000 points de
livraison, infrastructure critique), en posant les fondations d'une **plateforme data
sécurisée, prédictive et pilotée**.

> Mission de **cadrage + prototypage sur 1 semaine**. On ne livre pas un système en
> production : on livre un **prototype crédible** et un **dossier de décision** pour le
> comité de pilotage.

## 🚀 Collaborateurs : faire tourner le projet en local
➡️ **Suivez le [Guide d'installation](GUIDE-INSTALLATION.md)** (clone, environnement Python,
récupération des données, lancement). Démo Windows en double-clic : `demarrer-demo.bat`.

> ⚠️ Les données CSV ne sont **pas** dans le dépôt (volumineuses + RGPD) : récupérez le
> dossier `donnees/` auprès de l'équipe / via OneDrive (voir le guide, étape 3).

## Cas d'usage prioritaires (périmètre du prototype)
1. **Détection d'anomalies / fraude** sur les relevés de compteurs (gisement ROI, enjeu éthique).
2. **Prévision de consommation** à un horizon utile à l'achat d'énergie (anticipation des pics).

Le tout porté par une **chaîne de données** (ingestion → stockage → API → restitution),
**sécurisée** (analyse de risque, SIEM, conformité RGPD/NIS 2) et **pilotée** (business
case, gouvernance, conduite du changement).

## Structure du dépôt
```
neovolt-grid-plus/
├── docs/                     # Tronc commun : cadrage, archi, gouvernance, éthique, exec summary EN
├── data/                     # Données (raw NON versionnées — RGPD ; voir data/README.md)
├── scripts/                  # Scripts partagés (diagnostic qualité, nettoyage...)
├── volet-cpid-pilotage/      # Chef de projet IT & Data  (business case, RACI, pilotage)
├── volet-analyst/            # Data Analyst              (EDA, segmentation, NLP, dashboards)
├── volet-datascience/        # Data Scientist            (prévision, détection fraude, MLOps)
├── volet-ild-dataeng/        # Ingénierie Logiciel & Data Eng (pipeline, API, Docker)
├── volet-cyber/              # Cybersécurité             (risque, audit, SIEM, runbook, conformité)
└── livrables-individuels/    # Journaux de bord, notes réflexives, éval par les pairs
```

## Démarrage rapide
```bash
# 1. Environnement Python (reproductible)
python -m venv .venv
.venv\Scripts\activate            # Windows ;  source .venv/bin/activate sous Linux/Mac
pip install -r requirements.txt

# 2. Pointer vers les données (par défaut ../donnees)
set NEOVOLT_DATA=C:\chemin\vers\donnees   # optionnel

# 3. Diagnostic qualité des données
python scripts/01_exploration_qualite.py
```

## Données
Les CSV bruts **ne sont pas versionnés** (volumineux + données personnelles de
consommation = RGPD). Voir [data/README.md](data/README.md). Source : dossier `donnees/`
fourni avec l'examen.

## Documents clés
- [Note de cadrage](docs/00-note-de-cadrage.md) — reformulation du besoin, périmètre, objectifs, risques
- [Diagnostic qualité des données](docs/diagnostic-qualite-donnees.md) — état des lieux chiffré (généré)

## Usage de l'IA
L'assistance IA (Claude) est utilisée pour accélérer la production ; chaque choix est
compris et défendable par l'équipe. Voir l'annexe déclarative dans le dossier projet.
