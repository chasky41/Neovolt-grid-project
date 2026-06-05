# Rapport — Prévision de consommation (volet Data Scientist)

## 1. Objectif

Développer un modèle capable d'anticiper la consommation énergétique à partir des données historiques de consommation et des données météorologiques.

L'objectif est d'aider Néovolt à :

* anticiper les pics de consommation ;
* améliorer la planification énergétique ;
* optimiser les achats d'énergie ;
* fournir une aide à la décision aux équipes métier.

## 2. Préparation des données

Les données de consommation ont été enrichies avec des informations météorologiques et temporelles.

Les traitements réalisés comprennent :

* suppression des doublons ;
* traitement des valeurs manquantes ;
* identification des valeurs aberrantes ;
* enrichissement par les données météo ;
* création de variables calendaires.

Après nettoyage, **98,46 % des relevés sont exploitables**.

## 3. Feature Engineering

Création de variables explicatives utilisées pour l'apprentissage :

* température moyenne ;
* mois ;
* saison ;
* jour de la semaine ;
* consommation historique ;
* tendances de consommation ;
* variables météo agrégées.

Ces variables permettent de capturer les comportements saisonniers ainsi que l'influence des conditions météorologiques sur la demande énergétique.

## 4. Modèles évalués

Plusieurs approches de Machine Learning ont été comparées :

* Régression Linéaire ;
* Ridge Regression ;
* Random Forest Regressor.

Chaque modèle a été entraîné puis évalué sur un jeu de test indépendant.

## 5. Évaluation des performances

Les performances ont été mesurées à l'aide des indicateurs :

* MAE (Mean Absolute Error) ;
* RMSE (Root Mean Squared Error) ;
* MAPE (Mean Absolute Percentage Error) ;
* R² (Coefficient de détermination).

Le modèle retenu présente les meilleures performances globales et atteint un **MAPE inférieur à 10 %**, ce qui est satisfaisant pour un cas d'usage de prévision énergétique.

## 6. Résultats

Le modèle permet :

* d'anticiper les pics de consommation ;
* d'améliorer la planification énergétique ;
* de faciliter les décisions liées aux achats d'énergie ;
* d'améliorer le pilotage opérationnel du réseau.

Les prévisions produites peuvent être intégrées aux tableaux de bord décisionnels afin de fournir une vision prospective de l'activité.

## 7. Artefacts produits (MLOps)

* `prediction_conso.ipynb`
* `predictions.csv`
* `analyse_critique.md`
* `mlops.md`
* `requirements.txt`

Les scripts et notebooks sont versionnés dans Git afin d'assurer la reproductibilité des résultats.

## 8. Limites

* Les performances dépendent de la qualité des données historiques.
* Certaines variables métier potentiellement pertinentes ne sont pas disponibles dans les données fournies.
* Le modèle a été entraîné sur un échantillon représentatif mais limité par rapport à un déploiement réel à l'échelle des 600 000 points de livraison.
* Les résultats obtenus constituent une démonstration de faisabilité dans le cadre du prototype.

## 9. Éthique

Le modèle fournit une **aide à la décision** et non une décision automatique.

Les prévisions doivent être interprétées par les équipes métier avant toute action opérationnelle.

Les principes de minimisation des données, de transparence et de gouvernance définis dans le projet sont respectés.

## 10. Perspectives

Une évolution future du programme pourrait intégrer des mécanismes de détection d'anomalies ou de fraude reposant sur le même socle de données.

Cette évolution nécessiterait des données supplémentaires, un historique plus important de cas confirmés et une analyse d'impact spécifique avant toute mise en production.
