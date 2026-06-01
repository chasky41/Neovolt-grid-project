# Plan de conduite du changement — Néovolt Grid+ (volet Chef de projet)

La meilleure plateforme échoue si personne ne l'utilise. Néovolt passe de **fichiers Excel
personnels** à une plateforme partagée, prédictive et sécurisée : c'est un changement de
**pratiques** et de **culture**, pas seulement d'outils.

## 1. Parties prenantes : attentes, craintes, leviers
| Acteur | Attente | Crainte | Levier d'adhésion |
|---|---|---|---|
| Exploitation réseau | Anticiper les pics, voir les incidents | Outil « hors-sol » | Co-construction des dashboards, données terrain |
| Direction financière | ROI démontré, pertes réduites | Dépenser sans gain | Business case chiffré, suivi du ROI réel |
| Relation client | Mieux traiter les réclamations | Détection de fraude qui accuse à tort | Humain dans la boucle, dashboard relation client |
| RSSI | Plateforme sécurisée et auditée | Nouvelle surface d'attaque | Sécurité by design, audit, SIEM |
| DPO | Traitement licite et proportionné | Exploitation abusive des données | AIPD, minimisation, gouvernance |
| Représentants du personnel | Transparence sur l'usage des données | Surveillance / déshumanisation | Communication, pas de notation individuelle des agents |

## 2. Démarche (inspirée ADKAR)
- **Conscience** : partager le diagnostic (pertes fraude, satisfaction 2,45/5, incident sécu réel).
- **Envie** : montrer le bénéfice concret par métier (moins de pertes, moins d'incidents subis).
- **Savoir** : formations courtes ciblées par rôle (lecture des dashboards, workflow d'enquête fraude).
- **Capacité** : accompagnement terrain, référents (« champions ») dans chaque direction.
- **Renforcement** : suivi des usages, quick wins valorisés, boucle de feedback.

## 3. Anticiper les résistances
| Résistance | Réponse |
|---|---|
| « On perd la main, c'est la machine qui décide » | Décision **assistée** : le modèle priorise, l'humain tranche (fraude). |
| « Mes fichiers Excel marchaient » | Migration accompagnée, dashboards qui font gagner du temps, pas de perte d'autonomie d'analyse. |
| « C'est de la surveillance des employés » | Charte d'usage, transparence, finalité = réseau & fraude, pas le contrôle des agents. |
| « Encore un projet qui va échouer » | Jalons visibles, quick wins (fraude) dès M+3, communication régulière. |

## 4. Plan de communication & déploiement
- **Déploiement progressif** : pilote sur une zone/direction avant généralisation (réduit le risque).
- Comité de pilotage mensuel (dashboard de pilotage), points d'étape par jalon.
- Communication interne à chaque quick win ; documentation et support accessibles.

## 5. Indicateurs d'adoption (suivis dans le dashboard de pilotage)
- Taux d'utilisation des dashboards par direction.
- Délai moyen de traitement d'une alerte fraude (workflow adopté ?).
- Satisfaction des utilisateurs internes ; nombre de référents actifs.
