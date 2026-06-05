# Néovolt Grid+ — Prototype & dossier de cadrage

Réponse de l'équipe projet au programme **Néovolt Grid+** : moderniser l'exploitation des données du réseau de distribution d'énergie de Néovolt (≈ 600 000 points de livraison, infrastructure critique), en posant les fondations d'une plateforme data sécurisée, prédictive et pilotée.

Mission de cadrage et de prototypage sur une semaine. Nous ne livrons pas un système en production : nous livrons un prototype crédible et un dossier de décision destiné au comité de pilotage.

## 🚀 Collaborateurs : faire tourner le projet en local

➡️ Suivez le **Guide d'installation** (clone du dépôt, environnement Python, récupération des données, lancement des scripts).

Démo Windows en double-clic : `demarrer-demo.bat`.

⚠️ Les données CSV ne sont pas présentes dans le dépôt (volumineuses + contraintes RGPD). Récupérez le dossier `donnees/` auprès de l'équipe ou via OneDrive (voir le guide d'installation, étape 3).

---

# Cas d'usage prioritaires (périmètre du prototype)

### 1. Prévision de consommation

Prévoir la consommation énergétique à partir des données historiques et météorologiques afin d'anticiper les pics de consommation et d'améliorer la planification énergétique.

### 2. Détection d'anomalies / fraude (perspective d'évolution)

Une analyse exploratoire a été menée afin d'étudier le potentiel de détection d'anomalies sur les relevés de compteurs. Cette piste est considérée comme une évolution future du programme.

L'ensemble est porté par une chaîne de données complète :

**Ingestion → Nettoyage → Stockage → API → Restitution**

avec des dimensions transverses :

* Sécurité (analyse de risque, SIEM, audit)
* Conformité (RGPD, NIS 2)
* Gouvernance des données
* Pilotage du programme

---

# Structure du dépôt

```text
neovolt-grid-project/
├── docs/                     # Tronc commun : cadrage, architecture, gouvernance, éthique, executive summary
├── data/                     # Données (raw non versionnées — RGPD)
├── scripts/                  # Scripts partagés (diagnostic qualité, nettoyage...)
├── volet-cpid-pilotage/      # Chef de projet IT & Data (business case, gouvernance, pilotage)
├── volet-analyst/            # Data Analyst (EDA, segmentation, NLP, dashboards)
├── volet-datascience/        # Data Scientist (prévision de consommation, analyse critique, MLOps)
├── volet-ild-dataeng/        # Ingénierie Logiciel & Data Engineering (pipeline, API, Docker)
├── volet-cyber/              # Cybersécurité (analyse de risque, audit, SIEM, conformité)
└── livrables-individuels/    # Journaux de bord, notes réflexives, évaluations par les pairs
```

---

# Démarrage rapide

```bash
# 1. Environnement Python
python -m venv .venv

# Activation
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux / Mac

pip install -r requirements.txt

# 2. Emplacement des données (optionnel)
set NEOVOLT_DATA=C:\chemin\vers\donnees

# 3. Diagnostic qualité
python scripts/01_exploration_qualite.py
```

---

# Données

Les CSV bruts ne sont pas versionnés dans le dépôt :

* volume important ;
* données de consommation à caractère personnel ;
* contraintes RGPD.

Voir `data/README.md`.

Source : dossier `donnees/` fourni dans le cadre de l'examen.

---

# Documents clés

* Note de cadrage
* Architecture cible
* Dossier projet
* Executive Summary (anglais)
* Rapport de qualité des données
* Business Case
* Rapport SIEM
* Dashboards d'analyse

---

# Usage de l'IA

L'assistance IA (Claude et ChatGPT) a été utilisée pour accélérer certaines productions.

Tous les choix méthodologiques, techniques et organisationnels ont été relus, vérifiés et validés par l'équipe projet.

Chaque membre est en mesure d'expliquer et de défendre les travaux réalisés lors de la soutenance.

Voir l'annexe déclarative d'usage de l'IA dans le dossier projet.

