# Analyse descriptive de la consommation — Néovolt Grid+ (volet Data Analyst)

- Base d'analyse : 503,830 relevés exploitables, 700 PDL, 8 zones, du 2024-01-01 au 2025-12-31

## 1. Saisonnalité

- Conso moyenne journalière : **hiver 90.2 kWh** vs **été 74.5 kWh** (ratio ×1.21) → forte saisonnalité, pics hivernaux.
- Pic mensuel : January 2025 (1980 MWh) ; creux : June 2024 (1436 MWh).

## 2. Profils par segment et type de client

- collectivite : 546.0 kWh/j
- entreprise : 273.2 kWh/j
- petit_pro : 53.4 kWh/j
- particulier : 11.2 kWh/j

## 3. Corrélation consommation / température

- Au niveau du relevé individuel : corr = **0.002** → quasi nulle, car la variance de taille entre clients masque l'effet météo (piège classique).
- **Au niveau agrégé du réseau (conso totale/jour vs température/jour) : corr = -0.317** → nettement négative : plus il fait froid, plus le réseau consomme. C'est CE signal qui sert à anticiper les pics.
- Sensibilité moyenne intra-PDL des logements chauffage électrique : -0.465 (négative = chauffage thermosensible).

## 4. Disparités géographiques (par zone)

- Zone la plus consommatrice : **Zone-Industrielle** (370.0 kWh/j) ; la plus faible : Plateau-Est (14.0 kWh/j).

## 5. Segmentation des clients (KMeans sur profils de consommation)

Profils types identifiés (segmentation comportementale) :

| Cluster | Nb PDL | Conso moy (kWh/j) | Ratio hiver/été | Ratio week-end/semaine |
|---|---|---|---|---|
| 0 | 132 | 20.2 | 2.92 | 1.00 |
| 1 | 310 | 10.3 | 1.49 | 1.06 |
| 2 | 53 | 714.4 | 1.15 | 0.55 |
| 3 | 205 | 63.9 | 1.30 | 0.55 |

## Figures & exports produits

- 5 figures dans `volet-analyst/figures/`
- 3 tables d'indicateurs agrégées dans `volet-analyst/dashboards/` (import Power BI / Plotly)
