##  Éléments MLOps

Dans le cadre de ce prototype, plusieurs éléments MLOps simples ont été prévus :

- le code est versionné avec Git ;
- le notebook documente les différentes étapes de l’expérimentation ;
- les métriques sont exportées dans un fichier `metrics_us6.txt` ;
- les prédictions sont exportées dans un fichier `predictions_us6.csv` ;
- les fichiers générés sont placés dans `data/output`.

Dans une mise en production, il faudrait également prévoir :
- la sauvegarde du modèle entraîné ;
- le suivi de la dérive des données ;
- le suivi régulier du MAPE ;
- un réentraînement périodique du modèle ;
- une supervision métier des prévisions critiques.