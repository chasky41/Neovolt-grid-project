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

## Règles de nettoyage appliquées (méthode `na.omit`, alignée sur l'approche R de l'équipe)
1. **Espaces superflus** retirés dans les colonnes texte.
2. **Doublons** supprimés (lignes identiques).
3. **Types convertis** : dates au format Date, colonnes de mesure en numérique.
4. **Lignes incomplètes supprimées** (`na.omit` / `dropna`) -> fichiers **sans aucune valeur manquante**.
5. **Consommation négative** (impossible physiquement) traitée comme manquante, donc supprimée.

Résultat : chaque fichier est **sans valeur manquante et sans doublon**.

### Conséquences à connaître (transparence)
- `clients` : **700 -> 426 lignes** (274 lignes supprimées car `nb_personnes_foyer` était vide).
- `releves_consommation` : **512 986 -> 503 830 lignes** (1 286 doublons + 7 870 incomplètes,
  dont 1 032 consommations négatives).
- Les autres fichiers étaient déjà complets : inchangés.

> Choix de méthode : on **supprime** les lignes incomplètes (na.omit) plutôt que de les
> garder. Avantage : des fichiers 100 % propres, simples à exploiter. Limite assumée : on
> perd un peu d'information (ex. 274 clients). Méthode cohérente avec le reste de l'équipe.

Le détail chiffré, fichier par fichier, est dans **RAPPORT-NETTOYAGE-COMPLET.md**.

## Régénérer ce dossier
```
.venv\Scripts\python.exe scripts\03_nettoyage_complet.py
```

> Note RGPD : certains de ces fichiers contiennent des données personnelles
> (consommation, clients). Ils ne sont pas versionnés dans Git ; pour les partager,
> passer par OneDrive (comme demandé dans le sujet pour les fichiers volumineux).
