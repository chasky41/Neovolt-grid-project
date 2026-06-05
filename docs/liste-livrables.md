# Liste des livrables & checklist de dépôt — Néovolt Grid+

## 1. Livrables collectifs (un dépôt par groupe)

### Dossier projet (PDF)

| Élément                     | Fichier                                                        |
| --------------------------- | -------------------------------------------------------------- |
| Dossier projet intégré      | [dossier-projet.md](dossier-projet.md) → **à exporter en PDF** |
| Note de cadrage             | [00-note-de-cadrage.md](00-note-de-cadrage.md)                 |
| Architecture cible          | [01-architecture-cible.md](01-architecture-cible.md)           |
| Executive summary (anglais) | [executive-summary-EN.md](executive-summary-EN.md)             |
| Éthique / RGPD / AIPD       | [ethique-rgpd-aipd.md](ethique-rgpd-aipd.md)                   |
| Annexe usage de l'IA        | [annexe-usage-ia.md](annexe-usage-ia.md)                       |

### Productions techniques par volet

| Volet            | Dossier                                         | Contenu clé                                                    |
| ---------------- | ----------------------------------------------- | -------------------------------------------------------------- |
| ILD              | [volet-ild-dataeng/](../volet-ild-dataeng/)     | pipeline, entrepôt, API, Docker, smoke test                    |
| Data Scientist   | [volet-datascience/](../volet-datascience/)     | prévision de consommation, évaluation, analyse critique, MLOps |
| Data Analyst     | [volet-analyst/](../volet-analyst/)             | analyses, NLP, 3 dashboards interactifs                        |
| Cyber            | [volet-cyber/](../volet-cyber/)                 | SIEM, EBIOS, audit, runbook, conformité                        |
| CPID             | [volet-cpid-pilotage/](../volet-cpid-pilotage/) | business case, plan, gouvernance, pilotage                     |
| Rapports générés | [docs/](.)                                      | diagnostic qualité, nettoyage, SIEM, analyses                  |

### Vidéos & support (à produire — voir scripts)

* [ ] Vidéo de **démonstration** (5-10 min) — produit en action → **OneDrive** (lien dans le dossier)
* [ ] Vidéo de **soutenance** (20-30 min, chaque membre parle, visage visible) → **OneDrive**
* [ ] **Support de présentation** (slides)

> Les CSV bruts, l'entrepôt `.db`, les modèles et les dashboards HTML sont volumineux et/ou
> contiennent des données personnelles : **non versionnés** → à déposer sur **OneDrive** et à
> régénérer via les scripts. Voir [data/README.md](../data/README.md).

## 2. Livrables individuels (un par apprenant)

* [ ] Journal de bord individuel → modèle : [livrables-individuels/](../livrables-individuels/)
* [ ] Note réflexive (1-2 pages)
* [ ] Fiche d'évaluation par les pairs (confidentielle)

## 3. Checklist de dépôt (avant vendredi 5 juin 23h59 — heure de Paris)

* [ ] Dossier projet (PDF) déposé dans Teams > Devoirs
* [ ] Executive summary en anglais inclus dans le dossier
* [ ] Productions techniques déposées ou liens fournis et accessibles
* [ ] Vidéo de démonstration déposée (ou lien OneDrive)
* [ ] Vidéo de soutenance déposée (chaque membre intervient, visage visible)
* [ ] Support de présentation déposé
* [ ] Annexe déclarative d'usage de l'IA incluse
* [ ] Journal de bord individuel de chaque membre déposé
* [ ] Note réflexive individuelle de chaque membre déposée
* [ ] Fiches d'évaluation par les pairs déposées
* [ ] Accès donnés à **[jbanka@esic.fr](mailto:jbanka@esic.fr)** (OneDrive **et** dépôt de code)
* [ ] Liste de tous les livrables et liens récapitulée dans le dossier projet

## 4. Comment générer un PDF du dossier

Depuis les `.md` (ex. avec VS Code + extension Markdown PDF, ou Pandoc) :

```bash
pandoc docs/dossier-projet.md -o dossier-projet.pdf
```


