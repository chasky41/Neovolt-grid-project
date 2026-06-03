# Guide d'installation — faire tourner le projet en local (pour les collaborateurs)

Ce guide explique comment installer et exécuter le prototype **Néovolt Grid+** sur votre
machine, à partir d'un clone du dépôt. Comptez ~10 minutes.

---

## 1. Pré-requis (à installer une fois)
- **Python 3.11** — https://www.python.org/downloads/ (cocher **« Add Python to PATH »** à l'installation).
- **Git** — https://git-scm.com/downloads
- *(Optionnel)* **Docker Desktop** — seulement si vous voulez lancer l'API en conteneur.

Vérifier dans un terminal :
```bash
python --version      # doit afficher 3.11.x
git --version
```

## 2. Cloner le dépôt
```bash
git clone https://github.com/chasky41/Neovolt-grid-project.git
cd Neovolt-grid-project
```

## 3. ⚠️ Récupérer les données (IMPORTANT — elles ne sont PAS dans le dépôt)
Les fichiers CSV de données **ne sont pas versionnés** (volumineux + données personnelles =
RGPD). Il faut donc récupérer le dossier **`donnees/`** (les 10 fichiers CSV) **auprès de
l'équipe / via OneDrive**, puis le placer ainsi :

```
un-dossier-parent/
├── Neovolt-grid-project/     <- le dépôt cloné
└── donnees/                  <- À PLACER ICI (à côté du dépôt)
    ├── clients.csv
    ├── compteurs.csv
    ├── releves_consommation.csv
    └── ... (les 10 fichiers)
```

> Le dossier `donnees/` doit être **à côté** du dépôt cloné (c'est le chemin par défaut).
> Sinon, indiquez son emplacement avec une variable d'environnement :
> - Windows : `set NEOVOLT_DATA=C:\chemin\vers\donnees`
> - Mac/Linux : `export NEOVOLT_DATA=/chemin/vers/donnees`

## 4. Créer l'environnement Python et installer les dépendances
```bash
python -m venv .venv

# Activer l'environnement :
.venv\Scripts\activate            # Windows
# source .venv/bin/activate       # Mac / Linux

pip install -r requirements.txt
```

## 5. Lancer le projet

### Le plus simple (Windows) — double-clic
- **`demarrer-demo.bat`** : nettoie les données, construit la base, génère les modèles et
  ouvre les tableaux de bord. Attendre « PRET POUR LA DEMO ».
- **`lancer-api.bat`** : lance l'API (http://127.0.0.1:8000/docs).
- **`lancer-docker.bat`** / **`arreter-docker.bat`** : version conteneur (Docker requis).
- **`generer-pdf.bat`** : génère les PDF de documentation.

### En ligne de commande (toutes plateformes)
```bash
# 1) Préparer les données + l'entrepôt
python scripts/02_nettoyage.py
python volet-ild-dataeng/build_warehouse.py

# 2) Modèles et analyses
python volet-datascience/detection_fraude.py
python volet-analyst/analyse_descriptive.py
python volet-analyst/nlp_reclamations.py
python volet-analyst/dashboard.py
python volet-cpid-pilotage/business_case.py
python volet-cyber/analyse_journaux.py

# 3) Lancer l'API (depuis le dossier api, car le dossier parent a des tirets)
cd volet-ild-dataeng/api
uvicorn main:app --port 8000        # puis ouvrir http://127.0.0.1:8000/docs
```

## 6. Où trouver les résultats
- **Tableaux de bord** : `volet-analyst/dashboards/*.html` (ouvrir dans un navigateur).
- **API** : http://127.0.0.1:8000/docs (documentation interactive).
- **Rapports** : dossier `docs/` (qualité, fraude, SIEM, analyses, business case…).
- **Données nettoyées** : `data/processed/` et `donnees_nettoyees_separees/`.

## 7. Structure du projet (rappel)
```
docs/                  Cadrage, architecture, éthique/RGPD, executive summary, dossier
scripts/               Nettoyage des données, génération de PDF
volet-ild-dataeng/     Pipeline, entrepôt, API, Docker
volet-datascience/     Détection de fraude (modèle)
volet-analyst/         Analyses, NLP, dashboards
volet-cyber/           SIEM, analyse de risque, audit, runbook
volet-cpid-pilotage/   Business case, plan projet, gouvernance, pilotage
livrables-individuels/ Modèles de journal de bord, note réflexive, éval par les pairs
```

## 8. Problèmes fréquents
| Problème | Solution |
|---|---|
| `FileNotFoundError` / dossier `donnees` introuvable | Placer `donnees/` à côté du dépôt, ou définir `NEOVOLT_DATA` (étape 3). |
| `Permission denied` sur un `.csv` | Le fichier est ouvert dans Excel → le fermer, relancer. |
| `ModuleNotFoundError` | L'environnement n'est pas activé → refaire l'étape 4. |
| L'API ne démarre pas | Vérifier d'avoir lancé `build_warehouse.py` (la base doit exister). |
| `.bat` bloqué par Windows | Clic droit → Propriétés → « Débloquer », ou « Exécuter quand même ». |

---
Questions ? Contacter l'équipe. Bonne installation 🚀
