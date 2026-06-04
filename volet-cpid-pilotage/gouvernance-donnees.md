# Plan de gouvernance des données — Néovolt Grid+ (volet Chef de projet)

## Objectif

L'objectif de la gouvernance des données est de définir clairement les responsabilités, les règles de qualité, les droits d'accès et les modalités de conservation des données utilisées dans le projet Néovolt Grid+.

Cette gouvernance vise à garantir la fiabilité des analyses, la conformité réglementaire et la sécurité des informations exploitées dans le cadre de la prévision de consommation et du pilotage du réseau.

---

## 1. Domaines de données et responsabilités

| Domaine      | Données                                         | Propriétaire métier | Responsable technique | Sensibilité                 |
| ------------ | ----------------------------------------------- | ------------------- | --------------------- | --------------------------- |
| Clients      | Informations clients, segments                  | Service Client      | DSI                   | Données personnelles (RGPD) |
| Compteurs    | Identifiants compteurs, puissance souscrite     | Exploitation Réseau | DSI                   | Données personnelles        |
| Consommation | Relevés de consommation journaliers ou horaires | Exploitation Réseau | Pôle Données          | Données sensibles           |
| Météo        | Température, conditions climatiques             | Exploitation Réseau | Pôle Données          | Faible                      |
| Réseau       | Incidents, équipements, postes                  | Exploitation Réseau | Pôle Données          | Interne                     |
| Prévisions   | Résultats du modèle de prévision                | Exploitation Réseau | Pôle Données          | Interne                     |

---

## 2. Matrice RACI

*R = Réalise, A = Responsable / Approuve, C = Consulté, I = Informé*

| Activité                                  | DSI | Pôle Données | DPO | RSSI | Métier | Direction |
| ----------------------------------------- | --- | ------------ | --- | ---- | ------ | --------- |
| Définition de la gouvernance              | A   | R            | C   | C    | C      | I         |
| Qualité des données                       | A   | R            | I   | I    | C      | I         |
| Gestion des accès                         | C   | R            | C   | A    | C      | I         |
| Conformité RGPD                           | I   | C            | A/R | C    | I      | I         |
| Sécurité des données                      | C   | C            | C   | A/R  | I      | I         |
| Durées de conservation                    | C   | R            | A   | C    | C      | I         |
| Utilisation des données et des prévisions | C   | C            | C   | C    | A      | I         |

---

## 3. Politique de qualité des données

Les données utilisées dans le projet font l'objet de contrôles systématiques avant toute exploitation :

* contrôle des valeurs manquantes ;
* contrôle des doublons ;
* contrôle des valeurs aberrantes ;
* vérification de la cohérence des formats ;
* traçabilité des traitements réalisés ;
* documentation et versionnement des règles de qualité.

Les indicateurs de qualité sont suivis tout au long du projet afin de garantir la fiabilité des analyses et du modèle de prévision.

---

## 4. Cycle de vie et conservation

| Type de donnée                    | Durée de conservation                         |
| --------------------------------- | --------------------------------------------- |
| Relevés de consommation détaillés | 36 mois puis agrégation ou anonymisation      |
| Données clients                   | Selon les obligations légales applicables     |
| Données de prévision              | 12 mois                                       |
| Journaux techniques               | 12 mois                                       |
| Données agrégées de pilotage      | Conservation possible à des fins statistiques |

Les principes de minimisation et de limitation de conservation sont appliqués conformément au RGPD.

---

## 5. Gestion des accès

Les accès aux données reposent sur le principe du moindre privilège.

Les profils utilisateurs disposent uniquement des droits nécessaires à leurs missions :

* Service Client : accès aux données clients et indicateurs associés ;
* Exploitation Réseau : accès aux données de consommation et aux prévisions ;
* Data Analyst et Data Scientist : accès aux données nécessaires aux analyses ;
* Direction : accès aux tableaux de bord et indicateurs agrégés ;
* Administrateurs : accès technique sous contrôle de la DSI.

Les accès sensibles sont tracés et revus régulièrement.

---

## 6. Outillage

La gouvernance des données s'appuie sur :

* un dictionnaire de données partagé ;
* la documentation du projet ;
* GitHub pour la traçabilité des évolutions ;
* les contrôles qualité intégrés aux traitements ;
* les tableaux de bord de suivi du projet.

Cette approche permet d'assurer la qualité, la sécurité et la bonne utilisation des données tout au long du cycle de vie du projet Néovolt Grid+.
