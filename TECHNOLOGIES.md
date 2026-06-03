# Technologies & outils utilisés — Néovolt Grid+

Liste complète des technologies, bibliothèques et outils utilisés dans le projet, avec leurs
versions (relevées sur l'environnement de développement).

## Langage & exécution
| Techno | Version | Usage |
|---|---|---|
| **Python** | 3.11.0 | Langage principal (pipeline, modèles, API, analyses) |
| **R** (base) | — | Nettoyage des données côté équipe (`read.csv`, `na.omit`, `as.Date`) |

## Gestion de version & collaboration
| Techno | Version | Usage |
|---|---|---|
| **Git** | 2.45.2 | Versionnage, historique de commits |
| **GitHub** | — | Hébergement du dépôt, collaboration |

## Manipulation & analyse de données
| Techno | Version | Usage |
|---|---|---|
| **pandas** | 3.0.3 | Lecture/nettoyage/agrégation des données |
| **NumPy** | 2.4.6 | Calcul numérique |
| **SciPy** | 1.17.1 | Fonctions scientifiques/statistiques |

## Machine Learning & statistiques
| Techno | Version | Usage |
|---|---|---|
| **scikit-learn** | 1.5.2 | **Isolation Forest** (détection de fraude), **KMeans** (segmentation), **TF-IDF** (NLP), StandardScaler |
| **statsmodels** | 0.14.4 | Statistiques / séries temporelles |
| **joblib** | 1.5.3 | Sauvegarde du modèle entraîné (`.joblib`) |

## Visualisation & tableaux de bord
| Techno | Version | Usage |
|---|---|---|
| **Plotly** | 5.24.1 | **Dashboards interactifs** (HTML autonomes) |
| **Matplotlib** | 3.10.9 | Graphiques pour les rapports |
| **seaborn** | 0.13.2 | Graphiques statistiques |
| **Power BI** | — | Import des exports CSV agrégés (alternative décideurs) |

## API & backend
| Techno | Version | Usage |
|---|---|---|
| **FastAPI** | 0.136.3 | Construction de l'API REST |
| **Uvicorn** | 0.48.0 | Serveur ASGI qui exécute l'API |
| **Starlette** | 1.2.1 | Socle web de FastAPI (corrigé pour CVE) |
| **Pydantic** | 2.13.4 | Validation des données de l'API |

## Base de données
| Techno | Version | Usage |
|---|---|---|
| **SQLite** | (module `sqlite3` intégré à Python) | Entrepôt du prototype (`neovolt.db`) |
| **PostgreSQL** | — | Base **cible** pour l'industrialisation (souveraineté UE) |

## Conteneurisation & déploiement
| Techno | Version | Usage |
|---|---|---|
| **Docker** | 27.2.0 | Conteneurisation de l'API |
| **Docker Compose** | v2.29.2 | Orchestration locale (API + base cible) |

## Sécurité & DevSecOps
| Techno | Version | Usage |
|---|---|---|
| **pip-audit** | — | Scan de vulnérabilités des dépendances (3 CVE trouvées & corrigées) |
| **EBIOS Risk Manager** | — | Méthode d'analyse de risque |
| **Logique SIEM** | — | Analyse des journaux de sécurité (détection d'attaque) |
| **OWASP ZAP / Nmap** | — | Outils d'audit recommandés (cadre éthique, périmètre projet) |

## Documentation & génération de PDF
| Techno | Version | Usage |
|---|---|---|
| **Markdown** | 3.10.2 | Rédaction des rapports |
| **xhtml2pdf** | 0.2.17 | Génération des PDF |
| **reportlab** | 4.5.1 | Moteur PDF (sous xhtml2pdf) |
| **pandoc** | 3.9.0.2 | Conversion de documents (alternative PDF) |
| **Mermaid** | — | Schémas d'architecture (dans le Markdown) |

## Méthodes & concepts mobilisés
- **Détection d'anomalies non supervisée** (Isolation Forest)
- **Segmentation** par clustering (KMeans)
- **NLP** : vectorisation TF-IDF + catégorisation par thèmes
- **Séries temporelles** (saisonnalité, corrélation météo)
- **EBIOS / ISO 27001** (analyse de risque, conformité)
- **RGPD / NIS 2** (conformité, AIPD, minimisation)
- **MLOps** (versioning du modèle, reproductibilité, `random_state` fixé)

## Scripts utilitaires
- **Scripts Windows `.bat`** : `demarrer-demo.bat`, `lancer-api.bat`, `lancer-docker.bat`,
  `arreter-docker.bat`, `generer-pdf.bat` (lancement en double-clic).

---
*Versions relevées via `pip list` (environnement `.venv`) et les commandes `--version` des outils.*
