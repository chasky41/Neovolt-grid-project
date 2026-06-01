# Volet Data Analyst — Faire parler les données

**Rôle :** transformer les montagnes de relevés en décisions. Les décideurs de Néovolt
ne lisent pas des tables SQL : ils lisent des **tableaux de bord** et écoutent **l'histoire
des données**. Visualisations lisibles par un non-spécialiste, honnêtes, recommandations
qui découlent des données.

## Ce que produit ce volet
| Script | Sortie | Pour |
|---|---|---|
| `analyse_descriptive.py` | 5 figures + [analyse-descriptive.md](../docs/analyse-descriptive.md) | saisonnalité, segments, météo, segmentation |
| `nlp_reclamations.py` | 2 figures + [analyse-reclamations.md](../docs/analyse-reclamations.md) | thèmes & satisfaction (NLP) |
| `dashboard.py` | 3 dashboards HTML interactifs | exploitation / finance / relation client |

## Conclusions clés (data storytelling)

**1. La consommation est fortement saisonnière.** Pic en **janvier 2025**, creux en juin.
Au niveau du réseau, la consommation est **corrélée négativement à la température (-0,32 ;
-0,47 pour les logements chauffés à l'électricité)**. ➜ *justifie* la prévision (volet Data
Scientist) pour anticiper les pics et optimiser l'achat d'énergie.
> ⚠️ Finesse analytique : au niveau du **relevé individuel**, la corrélation est ~0 — la
> variance de taille entre clients (industriel vs particulier) masque l'effet météo. Le bon
> niveau d'analyse pour un gestionnaire de réseau est l'**agrégat journalier**.

**2. Quatre profils de clients** (segmentation KMeans) : gros consommateurs pro/industriels
(profil plat, creux le week-end), logements à fort chauffage électrique (ratio hiver/été ×2,9),
petits résidentiels, et pros moyens. ➜ utile pour cibler les offres et la prévision par profil.

**3. Les réclamations révèlent 3 douleurs majeures** (3 000 réclamations, satisfaction
**2,45/5**, **53 % d'insatisfaits**) :
- **Facturation** (28 %, satisfaction 2,00/5) — thème n°1, le plus pénalisant.
- **Coupures/pannes** (26 %, 2,05/5) — à relier aux incidents réseau.
- **Compteurs** (25 %, 2,20/5).
- **Données/RGPD** (15 %, 445 réclamations) — signal de conformité pour le DPO.

## Recommandations
1. **Plan d'action facturation** (régularisations, transparence des estimations) : c'est le
   levier n°1 de satisfaction.
2. **Croiser réclamations « coupure » × incidents réseau** par zone (cohérence terrain).
3. **Suivre les réclamations RGPD** comme indicateur de conformité (lien DPO / éthique).
4. **Prévision de consommation par profil** pour soulager le réseau aux pics hivernaux.

## Exécuter
```bash
python scripts/02_nettoyage.py            # prérequis : conso_enrichie.csv
python volet-analyst/analyse_descriptive.py
python volet-analyst/nlp_reclamations.py
python volet-analyst/dashboard.py          # -> 3 HTML dans volet-analyst/dashboards/
```
Les dashboards HTML sont **autonomes** (Plotly embarqué) : double-clic = ouverture dans le
navigateur, même hors ligne (idéal pour la vidéo de démonstration). Ils n'exposent que des
**agrégats** (aucun PDL individuel) → conformes RGPD.

## Outils
Python (pandas, scikit-learn pour KMeans/TF-IDF), seaborn/matplotlib (figures), **Plotly**
(dashboards interactifs — alternative légère et versionnable à Power BI, explicitement
autorisée par le sujet). Les tables KPI agrégées (`dashboards/kpi_*.csv`) sont prêtes à
importer dans Power BI / Tableau si l'équipe préfère.
