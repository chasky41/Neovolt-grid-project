# Données — Néovolt Grid+

Les fichiers CSV bruts **ne sont pas versionnés dans Git** :
- volumétrie (relevés de consommation = ~513 000 lignes) ;
- **données personnelles de consommation = données à caractère personnel (RGPD)** : on
  ne diffuse pas ces données dans un dépôt de code (minimisation, maîtrise de la circulation).

## Où placer les données
Placer les 10 fichiers fournis dans `data/raw/`, **ou** laisser le dossier `donnees/` fourni
par l'examen à côté du projet (chemin par défaut `../donnees`).

Surcharge possible via variable d'environnement :
```bash
set NEOVOLT_DATA=C:\chemin\vers\donnees   # Windows
export NEOVOLT_DATA=/chemin/vers/donnees  # Linux/Mac
```

## Inventaire des fichiers
| Fichier | Lignes | Contenu |
|---|---|---|
| `clients.csv` | 700 | Référentiel clients (segment, foyer, surface, commune) |
| `compteurs.csv` | 700 | Référentiel points de livraison (puissance, chauffage, type compteur) |
| `releves_consommation.csv` | 512 986 | Relevés quotidiens 2024-2025 (cœur du projet) |
| `releves_horaires_echantillon.csv` | 21 600 | Échantillon de relevés au pas horaire |
| `meteo.csv` | 5 848 | Températures par zone et par jour |
| `incidents_reseau.csv` | 420 | Incidents réseau (type, durée, PDL impactés) |
| `reclamations.csv` | 3 000 | Réclamations clients en texte libre + satisfaction |
| `journaux_securite.csv` | 47 824 | Journaux d'accès / sécurité (mars→mai 2026) |
| `actifs_si.csv` | 28 | Inventaire des actifs du SI (criticité, exposition) |
| `cas_fraude_confirmes.csv` | 24 | Fraudes confirmées (vérité terrain) |

> Données **réalistes donc imparfaites** : valeurs manquantes, négatives, aberrantes,
> doublons. Leur nettoyage et leur interprétation font partie du travail (voir le
> [diagnostic qualité](../docs/diagnostic-qualite-donnees.md)).
