## Prévision de consommation

## Objectif

Développer un modèle de prévision de consommation électrique à partir des données historiques et météorologiques.

## Données utilisées

- releves_consommation.csv
- meteo.csv

## Démarche

- Chargement des données
- Nettoyage des valeurs manquantes
- Agrégation par date et zone
- Jointure avec les données météo
- Création de variables temporelles
- Entraînement de plusieurs modèles
- Comparaison des performances

## Modèles testés

- Baseline J-7
- Ridge Regression
- Random Forest Regressor

## Métriques utilisées

- MAE
- RMSE
- MAPE
- R²

## Résultat principal

Le modèle Random Forest obtient les meilleures performances avec un MAPE inférieur à 10 %, ce qui répond à l'objectif de prévision défini dans le projet.

## Limites

Le modèle dépend de la qualité des données historiques. Il devra être surveillé dans le temps avant toute mise en production, notamment pour détecter une éventuelle dérive des performances.

## Auteur

Ines SID-OTMANE