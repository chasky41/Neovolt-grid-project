# Néovolt Grid+ — Dossier d'explication et guide de démonstration

*Document de synthèse expliquant le projet, les choix techniques et la procédure de test.*

---

## 1. Le projet en bref

Néovolt est un distributeur régional d'énergie (électricité et gaz) qui alimente environ 600 000 foyers. C'est une infrastructure critique. Depuis deux ans, ses compteurs communicants envoient automatiquement la consommation, ce qui génère une grande masse de données aujourd'hui mal exploitée.

Le client (programme « Néovolt Grid+ ») nous a demandé, en une semaine, de livrer un **prototype** et un **dossier de décision** démontrant qu'on sait concevoir, réaliser, sécuriser et piloter une plateforme de données. Les besoins à couvrir :

* centraliser et fiabiliser les données ;
* anticiper la consommation (achats d'énergie, pics) ;
* identifier les futures opportunités de détection d'anomalies ;
* fournir des tableaux de bord aux décideurs ;
* sécuriser l'ensemble et respecter le RGPD ;
* piloter le programme (budget, gouvernance).

Notre réponse est une **chaîne complète** : donnée brute -> nettoyage -> base de données -> API -> tableaux de bord et modèle de prévision de consommation, le tout sécurisé et piloté.

---

## 2. Les données traitées

Nous sommes partis de **10 fichiers CSV** fournis (données réalistes, donc imparfaites), soit environ **570 000 lignes** au total.

| Fichier                          | Lignes  | Contenu                                                                                  |
| -------------------------------- | ------- | ---------------------------------------------------------------------------------------- |
| releves_consommation.csv         | 512 986 | Consommation quotidienne de chaque compteur sur 2 ans (le coeur)                         |
| releves_horaires_echantillon.csv | 21 600  | Échantillon de consommation au pas horaire                                               |
| journaux_securite.csv            | 47 824  | Journaux d'accès et de sécurité                                                          |
| reclamations.csv                 | 3 000   | Réclamations clients en texte libre + note de satisfaction                               |
| meteo.csv                        | 5 848   | Température par zone et par jour                                                         |
| incidents_reseau.csv             | 420     | Incidents du réseau (type, durée, foyers impactés)                                       |
| clients.csv                      | 700     | Référentiel client (segment, commune, foyer)                                             |
| compteurs.csv                    | 700     | Référentiel compteur (puissance, type, zone)                                             |
| actifs_si.csv                    | 28      | Inventaire du matériel informatique                                                      |
| cas_fraude_confirmes.csv         | 24      | Fraudes déjà confirmées (utilisées comme données historiques pour de futures évolutions) |

---

## 3. Le nettoyage et le filtrage des données

Les données réelles contiennent des erreurs. Nous avons appliqué des règles claires et documentées (script `scripts/02_nettoyage.py`) :

1. **Doublons** : suppression de 1 286 relevés en double.
2. **Valeurs négatives** (1 032) : une consommation négative est physiquement impossible (erreur de capteur). Nous les avons mises de côté (marquées comme manquantes).
3. **Valeurs à zéro** (637) : conservées mais signalées (un logement peut être vacant).
4. **Valeurs aberrantes** (2 118) : détectées **par compteur** et non globalement.
5. **Valeurs manquantes** : conservées et signalées.

**Résultat : 98,46 % des relevés sont directement exploitables.**

---

## 4. La base de données (entrepôt)

Une fois nettoyées, les données sont rangées dans une **base de données** (`neovolt.db`, SQLite) organisée en **8 tables** reliées entre elles.

Cette base unique alimente tous les résultats du projet : API, tableaux de bord et modèles analytiques.

---

## 5. L'API : à quoi elle sert et pourquoi

(Une API est un « guichet » permettant aux applications d'accéder aux données sans accéder directement à la base.)

**Pourquoi nous l'avons mise en place :**

* Sécurité et RGPD ;
* Mutualisation des accès ;
* Réutilisation des données ;
* Interopérabilité avec les dashboards et les modèles.

Construite avec **FastAPI**, elle expose plusieurs endpoints (`/health`, `/qualite`, `/consommation/par-zone`, etc.).

---

## 6. Les tableaux de bord

Nous avons produit **quatre tableaux de bord interactifs**.

### Exploitation réseau

* consommation quotidienne ;
* corrélation température / consommation ;
* consommation par zone ;
* incidents réseau.

### Direction financière

* volumes énergétiques ;
* saisonnalité ;
* indicateurs financiers.

### Relation client

* analyse automatique des 3 000 réclamations ;
* satisfaction moyenne : **2,45 / 5** ;
* facturation = principale source d'insatisfaction.

### Pilotage projet

* avancement ;
* budget ;
* risques ;
* indicateurs de valeur.

---

## 7. La prévision de consommation

L'objectif du volet Data Science est d'anticiper la consommation énergétique à partir des données historiques et des données météorologiques.

Nous avons construit plusieurs variables explicatives liées à la température, aux saisons et aux comportements de consommation observés dans les données.

Plusieurs modèles de Machine Learning ont été comparés puis évalués à l'aide des métriques MAE, RMSE, MAPE et R².

Le modèle retenu atteint un MAPE inférieur à 10 %, ce qui permet d'obtenir des prévisions suffisamment fiables pour aider à l'anticipation des pics de consommation et à la planification énergétique.

Ces prévisions peuvent être utilisées par Néovolt pour améliorer la gestion du réseau et optimiser les décisions liées aux achats d'énergie.

La détection d'anomalies et de fraude a également été étudiée comme une piste d'évolution future reposant sur le même socle de données.

---

## 8. La sécurité

(Section inchangée)

* Analyse SIEM ;
* Détection d'une attaque réelle ;
* Cartographie EBIOS ;
* Audit DevSecOps ;
* Runbook NIS 2 ;
* Mesures de sécurité by design.

---

## 9. Le business case (budget et rentabilité)

Le programme a été évalué à partir des hypothèses de coûts fournies dans le sujet.

* Budget initial estimé : **360 000 €**
* Coût annuel de fonctionnement : **75 000 €**
* Gains annuels estimés : **291 000 €**
* Gain net annuel estimé : **216 000 €**
* Retour sur investissement estimé : **environ 20 mois**

Les bénéfices proviennent principalement de l'amélioration de la planification énergétique, de l'optimisation des opérations, de la réduction des risques opérationnels et de l'amélioration du pilotage du réseau.

Une analyse de sensibilité montre que le projet reste rentable même avec des hypothèses plus prudentes.

---

## 10. Procédure de test (démonstration)

### Préparation

1. Double-cliquer sur `demarrer-demo.bat`.
2. Ouvrir Docker Desktop.
3. Double-cliquer sur `lancer-docker.bat`.

### Tests à réaliser

1. Vérifier que le conteneur Docker est actif.
2. Tester `GET /qualite`.
3. Tester `GET /health`.
4. Tester `GET /consommation/par-zone`.
5. Ouvrir les dashboards.
6. **Prévision de consommation : ouvrir les résultats du notebook Data Science et les graphiques de comparaison entre valeurs réelles et prédites.**
7. Ouvrir le rapport SIEM.
8. Arrêter Docker proprement.

---

## 11. Questions fréquentes (et nos réponses)

### Pourquoi Docker ?

Reproductibilité, portabilité et préparation à la montée en charge.

### Pourquoi avoir choisi la prévision de consommation ?

La prévision de consommation répond directement à un besoin métier identifié : anticiper les pics énergétiques, améliorer la planification et optimiser les achats d'énergie.

Les performances obtenues montrent qu'un tel usage est réaliste sur les données fournies.

### Risque d'accuser des clients à tort ?

Le prototype ne prend aucune décision automatique concernant les utilisateurs.

### Les chiffres de ROI sont-ils crédibles ?

Les hypothèses sont explicites et ajustables. Une analyse de sensibilité a été réalisée.

---

## 12. Note sur l'usage de l'intelligence artificielle

Conformément aux consignes, l'usage d'un assistant d'IA est déclaré.

Il a servi à accélérer la production (code, rédaction).

Nous avons systématiquement relu, vérifié et corrigé ses propositions.

Nous comprenons et assumons l'ensemble des choix présentés.
