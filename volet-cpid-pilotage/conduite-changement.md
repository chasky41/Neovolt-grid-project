# Plan de conduite du changement — Néovolt Grid+ (volet Chef de projet)

La meilleure solution échoue si les utilisateurs ne se l’approprient pas. Néovolt passe d’un fonctionnement reposant sur des fichiers dispersés à une solution data partagée, prédictive et sécurisée. Il s’agit donc d’un changement de pratiques, de pilotage et de culture de la donnée.

## 1. Parties prenantes : attentes, craintes, leviers

| Acteur                        | Attente                                                                           | Crainte                                        | Levier d'adhésion                                                     |
| ----------------------------- | --------------------------------------------------------------------------------- | ---------------------------------------------- | --------------------------------------------------------------------- |
| Exploitation réseau           | Anticiper les pics de consommation et mieux organiser les interventions           | Outil trop technique ou éloigné du terrain     | Co-construction des indicateurs, démonstrations avec des cas concrets |
| Direction financière          | Suivre les gains attendus et maîtriser les coûts du programme                     | Dépenses sans retour mesurable                 | Business case, suivi du ROI et indicateurs de valeur                  |
| Relation client               | Mieux comprendre certaines variations de consommation et traiter les réclamations | Mauvaise interprétation des données client     | Données expliquées, indicateurs lisibles, validation humaine          |
| Data Analyst / Data Scientist | Disposer de données fiables et exploitables                                       | Données de mauvaise qualité ou mal documentées | Dictionnaire de données, règles qualité, accès clarifiés              |
| RSSI / DSI                    | Plateforme sécurisée et maîtrisée                                                 | Nouvelle surface d’exposition technique        | Sécurité dès la conception, gestion des accès, traçabilité            |
| DPO                           | Traitement licite et proportionné des données                                     | Usage excessif des données personnelles        | Minimisation, anonymisation/agrégation, gouvernance RGPD              |
| Direction générale            | Vision claire de l’avancement et de la valeur produite                            | Projet difficile à piloter                     | Tableau de bord COPIL, jalons et indicateurs synthétiques             |

## 2. Démarche d’accompagnement

La conduite du changement s’appuie sur une démarche progressive :

* **Sensibiliser** : expliquer pourquoi Néovolt met en place une solution de prévision et de pilotage par la donnée.
* **Impliquer** : associer les métiers à la définition des indicateurs et à la validation des résultats.
* **Former** : proposer des sessions courtes sur la lecture des tableaux de bord, des prévisions et des indicateurs.
* **Accompagner** : identifier des référents métiers capables d’aider les utilisateurs au quotidien.
* **Améliorer** : recueillir les retours utilisateurs afin d’ajuster les tableaux de bord et les modèles.

## 3. Anticiper les résistances

| Résistance                                       | Réponse proposée                                                                                                  |
| ------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------- |
| « Le modèle va décider à notre place »           | La solution reste un outil d’aide à la décision : les équipes métiers conservent la validation finale.            |
| « Les fichiers Excel suffisent »                 | Les tableaux de bord partagés permettent de centraliser les indicateurs et d’éviter les versions contradictoires. |
| « Les prévisions ne seront pas fiables »         | Les performances sont suivies avec des métriques objectives comme le MAPE, le MAE et le RMSE.                     |
| « Le projet est trop technique »                 | Les restitutions sont conçues pour des décideurs non techniques avec des indicateurs simples et lisibles.         |
| « Les données personnelles sont trop sensibles » | Les accès sont limités, tracés et les données sont agrégées autant que possible.                                  |

## 4. Plan de communication et déploiement

* Déploiement progressif sur un périmètre pilote avant généralisation.
* Points réguliers de suivi avec les métiers et le comité de pilotage.
* Documentation accessible sur le dépôt projet et dans le dossier final.
* Démonstration du prototype pour montrer concrètement la valeur produite.
* Communication des premiers résultats obtenus sur la prévision de consommation.

## 5. Indicateurs d’adoption

| Indicateur                                       | Objectif                              |
| ------------------------------------------------ | ------------------------------------- |
| Taux d’utilisation des tableaux de bord          | Mesurer l’adoption par les métiers    |
| Nombre de retours utilisateurs                   | Identifier les axes d’amélioration    |
| Nombre de prévisions consultées                  | Suivre l’usage du modèle de prévision |
| Satisfaction des utilisateurs internes           | Mesurer l’acceptation de la solution  |
| Nombre de décisions appuyées par les indicateurs | Évaluer la valeur métier créée        |

## 6. Lien avec les évolutions futures

La détection d’anomalies et de fraudes pourra être intégrée dans une phase ultérieure, une fois le socle data fiabilisé et le modèle de prévision stabilisé. Cette évolution nécessitera un accompagnement renforcé, car elle implique des risques d’interprétation, de faux positifs et de traitement de données sensibles.
