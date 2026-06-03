# Données nettoyées (un fichier propre par source)

Ce dossier contient une version **nettoyée** de chacun des 10 fichiers d'origine du dossier
`donnees/`. Chaque fichier porte le suffixe `_clean.csv`.

| Fichier nettoyé | Source | Lignes |
|---|---|---|
| actifs_si_clean.csv | actifs_si.csv | 28 |
| clients_clean.csv | clients.csv | 700 |
| compteurs_clean.csv | compteurs.csv | 700 |
| meteo_clean.csv | meteo.csv | 5 848 |
| incidents_reseau_clean.csv | incidents_reseau.csv | 420 |
| reclamations_clean.csv | reclamations.csv | 3 000 |
| journaux_securite_clean.csv | journaux_securite.csv | 47 824 |
| cas_fraude_confirmes_clean.csv | cas_fraude_confirmes.csv | 24 |
| releves_consommation_clean.csv | releves_consommation.csv | 511 700 |
| releves_horaires_echantillon_clean.csv | releves_horaires_echantillon.csv | 21 600 |

## Règles de nettoyage appliquées
- **Espaces superflus** retirés dans les colonnes texte.
- **Doublons** supprimés (lignes identiques + doublons de clé, ex. id_client, id_pdl).
- **Valeurs impossibles mises à vide** : consommations négatives, surfaces ou puissances <= 0,
  notes de satisfaction hors 1-5, durées négatives.
- **Dates validées** (format vérifié).
- **Météo** : lignes où la température min > max corrigées (échange).
- **L'information manquante n'est jamais inventée** : on laisse vide et on le signale
  (exemple : `nb_personnes_foyer` manquant pour 274 clients).

Le détail chiffré, fichier par fichier, est dans **RAPPORT-NETTOYAGE-COMPLET.md**.

## Régénérer ce dossier
```
.venv\Scripts\python.exe scripts\03_nettoyage_complet.py
```

> Note RGPD : certains de ces fichiers contiennent des données personnelles
> (consommation, clients). Ils ne sont pas versionnés dans Git ; pour les partager,
> passer par OneDrive (comme demandé dans le sujet pour les fichiers volumineux).
