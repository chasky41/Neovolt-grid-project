# Néovolt Grid+ — Dossier d'explication et guide de démonstration

*Document de synthèse expliquant le projet, les choix techniques et la procédure de test.*

---

## 1. Le projet en bref

Néovolt est un distributeur régional d'énergie (électricité et gaz) qui alimente environ
600 000 foyers. C'est une infrastructure critique. Depuis deux ans, ses compteurs
communicants envoient automatiquement la consommation, ce qui génère une grande masse
de données aujourd'hui mal exploitée.

Le client (programme « Néovolt Grid+ ») nous a demandé, en une semaine, de livrer un
**prototype** et un **dossier de décision** démontrant qu'on sait concevoir, réaliser,
sécuriser et piloter une plateforme de données. Les besoins à couvrir :

- centraliser et fiabiliser les données ;
- anticiper la consommation (achats d'énergie, pics) ;
- détecter tôt les fraudes et anomalies ;
- fournir des tableaux de bord aux décideurs ;
- sécuriser l'ensemble et respecter le RGPD ;
- piloter le programme (budget, gouvernance).

Notre réponse est une **chaîne complète** : donnée brute -> nettoyage -> base de données
-> API -> tableaux de bord et modèle de détection de fraude, le tout sécurisé et chiffré.

---

## 2. Les données traitées

Nous sommes partis de **10 fichiers CSV** fournis (données réalistes, donc imparfaites),
soit environ **570 000 lignes** au total.

| Fichier | Lignes | Contenu |
|---|---|---|
| releves_consommation.csv | 512 986 | Consommation quotidienne de chaque compteur sur 2 ans (le coeur) |
| releves_horaires_echantillon.csv | 21 600 | Échantillon de consommation au pas horaire |
| journaux_securite.csv | 47 824 | Journaux d'accès et de sécurité |
| reclamations.csv | 3 000 | Réclamations clients en texte libre + note de satisfaction |
| meteo.csv | 5 848 | Température par zone et par jour |
| incidents_reseau.csv | 420 | Incidents du réseau (type, durée, foyers impactés) |
| clients.csv | 700 | Référentiel client (segment, commune, foyer) |
| compteurs.csv | 700 | Référentiel compteur (puissance, type, zone) |
| actifs_si.csv | 28 | Inventaire du matériel informatique |
| cas_fraude_confirmes.csv | 24 | Fraudes déjà confirmées (sert de vérité de référence) |

---

## 3. Le nettoyage et le filtrage des données

Les données réelles contiennent des erreurs. Nous avons appliqué des règles claires et
documentées (script `scripts/02_nettoyage.py`) :

1. **Doublons** : suppression de 1 286 relevés en double.
2. **Valeurs négatives** (1 032) : une consommation négative est physiquement impossible
   (erreur de capteur). Nous les avons mises de côté (marquées comme manquantes).
3. **Valeurs à zéro** (637) : conservées mais signalées (un logement peut être vacant).
4. **Valeurs aberrantes** (2 118) : détectées **par compteur** et non globalement. En effet,
   un client industriel consomme beaucoup de façon légitime : un seuil global serait faux.
   Elles sont signalées, pas supprimées.
5. **Valeurs manquantes** : conservées et signalées ; leur traitement éventuel est laissé
   aux modèles.

**Résultat : 98,46 % des relevés sont directement exploitables.** Nous avons ensuite
enrichi ces données en les croisant avec la météo, le type de client et la zone, pour
obtenir une table d'analyse unique. Ce croisement était impossible avant, car les données
vivaient dans des fichiers séparés.

---

## 4. La base de données (entrepôt)

Une fois nettoyées, les données sont rangées dans une **base de données** (un fichier
`neovolt.db`, technologie SQLite) organisée en **8 tables** reliées entre elles : une table
de faits (la consommation) et des tables de référence (compteurs, clients, météo,
incidents, réclamations, fraudes, actifs). C'est cette base unique qui alimente tous nos
résultats (API, tableaux de bord, modèle de fraude).

*Choix assumé :* SQLite pour un prototype simple qui fonctionne sans installation. Pour la
mise en production réelle, la cible est PostgreSQL hébergé dans l'Union européenne (pour la
souveraineté des données). Notre code est portable vers PostgreSQL.

---

## 5. L'API : à quoi elle sert et pourquoi

Une **API** est un « guichet » qui permet à d'autres programmes de demander des données
sans accéder directement à la base. Image simple : au restaurant, le client ne va pas en
cuisine ; il commande au serveur, qui rapporte le plat. Ici, la cuisine est la base de
données, le serveur est l'API.

**Pourquoi nous l'avons mise en place :**

- **Sécurité et RGPD** : les données de consommation sont personnelles. On ne donne pas un
  accès direct à la base ; l'API est une porte unique et contrôlée.
- **Mutualisation** : les tableaux de bord et les modèles récupèrent les données de la même
  façon propre, via l'API.
- **Ne pas rester coincé sur un poste** : sans API, les analyses resteraient dans un fichier
  isolé. L'API ouvre les résultats au reste du système.

Nous l'avons construite avec **FastAPI** (Python). Elle propose 8 points d'accès, par
exemple : état du service (`/health`), qualité des données (`/qualite`), consommation par
zone (`/consommation/par-zone`), historique d'un compteur, cas de fraude (accès restreint).
FastAPI génère aussi une page de documentation interactive (`/docs`) pour tester en direct.

---

## 6. Les tableaux de bord

Nous avons produit **quatre tableaux de bord interactifs**, un par profil de décideur.

**Exploitation réseau :** consommation quotidienne du réseau, lien consommation/température
(plus il fait froid, plus on consomme : utile pour anticiper les pics), consommation par
zone, incidents par type.

**Direction financière :** volume d'énergie par segment de client (base de revenu),
saisonnalité mensuelle (pour planifier les achats d'énergie), fraudes par type.

**Relation client :** analyse automatique des 3 000 réclamations. Satisfaction moyenne de
2,45 sur 5, et le sujet de mécontentement numéro un est la **facturation**.

**Pilotage projet :** avancement des lots, budget, matrice des risques, retour sur
investissement.

Ces tableaux de bord sont interactifs (on peut survoler, zoomer, filtrer), ce qui remplace
avantageusement les fichiers Excel figés utilisés jusqu'ici.

---

## 7. La détection de fraude

Nous ne disposions que de 24 fraudes confirmées : c'est trop peu pour un apprentissage
classique. Nous avons donc utilisé une méthode de **détection d'anomalies** (Isolation
Forest) qui classe les compteurs du plus suspect au moins suspect, à partir de leur
comportement de consommation.

Choix important : la détection se fait **par rapport au groupe de pairs** (un industriel est
comparé aux industriels), pour ne pas signaler un compteur simplement parce qu'il consomme
beaucoup.

**Résultat :** en contrôlant seulement 5 % des compteurs, on retrouve plus de la moitié des
fraudes connues, soit environ 10 fois plus efficace qu'un contrôle au hasard. Chaque alerte
est accompagnée de sa raison (par exemple une chute durable de consommation).

Point éthique : le modèle est une **aide à la priorisation**, pas un verdict. Un humain
tranche, conformément au RGPD sur les décisions automatisées.

---

## 8. La sécurité

Néovolt étant une infrastructure critique, la sécurité est traitée comme une priorité.

- **Analyse des journaux (logique SIEM)** : en analysant 47 824 événements, nous avons
  détecté une attaque réelle. Une adresse externe (203.0.113.45) a tenté 47 connexions en
  échec, puis a réussi à se connecter sur un compte utilisateur. Ce compte réalise par
  ailleurs des exports de données : il y a donc un risque de fuite de données personnelles.
- **Analyse de risque** : cartographie des 28 actifs, scénarios de menace et plan de
  traitement priorisé (méthode inspirée d'EBIOS et de la norme ISO 27001).
- **Audit du prototype et DevSecOps** : nous avons scanné nos dépendances logicielles, ce
  qui a révélé 3 vulnérabilités connues ; nous les avons corrigées, puis re-testé.
- **Runbook** : procédure de réponse à incident alignée sur la réglementation NIS 2
  (notification d'un incident majeur sous 24 heures).

Mesures « par conception » déjà en place : conteneur qui ne tourne pas en administrateur,
aucun secret ni donnée personnelle dans le code, requêtes à la base sécurisées contre
l'injection. Priorité identifiée avant mise en service : ajouter l'authentification sur
l'API et le chiffrement des données.

---

## 9. Le business case (budget et rentabilité)

Coûts calculés à partir des coûts unitaires fournis :

- Coût de la phase 1 : environ **325 000 euros**, soit sous l'enveloppe de 450 000 euros
  fixée, avec de la marge.
- Pertes liées à la fraude récupérables : environ **5,7 millions d'euros par an** (estimation
  prudente, hypothèses explicitées).
- **Retour sur investissement : environ 1,7 mois.**

Une analyse de sensibilité montre que le retour reste inférieur à un an même dans
l'hypothèse la plus pessimiste : la décision d'investir est donc robuste.

---

## 10. Procédure de test (démonstration)

### Préparation (une fois)
1. Double-cliquer sur `demarrer-demo.bat` : régénère toutes les données et ouvre les
   tableaux de bord. Attendre le message « PRET POUR LA DEMO ».
2. (Optionnel, pour montrer Docker) Ouvrir Docker Desktop, puis double-cliquer sur
   `lancer-docker.bat`.

### Tests à réaliser
1. **Docker** : dans Docker Desktop, le conteneur `neovolt-api` apparaît en vert (running).
2. **API - qualité** : sur `http://127.0.0.1:8000/docs`, ouvrir `GET /qualite`, cliquer
   « Try it out » puis « Execute ». Réponse attendue : taux exploitable 0,9846.
3. **API - santé** : `GET /health` -> « Execute » -> statut « ok » et 511 700 relevés.
4. **API - données** : `GET /consommation/par-zone` -> « Execute » -> consommation agrégée.
5. **Tableaux de bord** : ouvrir les 4 fichiers HTML (déjà ouverts) et naviguer.
6. **Détection de fraude** : ouvrir l'image `volet-datascience/figures/evaluation_fraude.png`.
7. **Sécurité** : ouvrir le rapport `docs/rapport-siem.md`.
8. **Arrêt propre** : double-cliquer sur `arreter-docker.bat`.

### Ce qui valide la démonstration
- Le conteneur Docker est en vert.
- L'API répond (qualité 0,9846 et 511 700 relevés).
- Les tableaux de bord s'affichent et sont interactifs.

---

## 11. Questions fréquentes (et nos réponses)

- **Pourquoi Docker ?** Pour la reproductibilité (ça tourne à l'identique partout), la
  portabilité (n'importe quel cloud, pas d'enfermement) et comme base pour la montée en
  charge. Nous l'avons réellement testé.
- **24 fraudes, est-ce fiable ?** C'est précisément pourquoi nous faisons de la détection
  d'anomalies et que nous évaluons sur ces cas. La performance est indicative, nous
  l'assumons.
- **Risque d'accuser des clients à tort ?** Le modèle priorise une enquête, il ne condamne
  pas. Un humain décide, et une analyse d'impact (AIPD) encadre le traitement.
- **Les chiffres de ROI sont-ils crédibles ?** Les hypothèses sont explicites et ajustables ;
  l'analyse de sensibilité montre un retour inférieur à un an même au pire.

---

## 12. Note sur l'usage de l'intelligence artificielle

Conformément aux consignes, l'usage d'un assistant d'IA est déclaré. Il a servi à accélérer
la production (code, rédaction). Nous avons vérifié et corrigé ses propositions (par exemple
une erreur d'interprétation d'une corrélation, et des vulnérabilités de dépendances). Nous
comprenons et assumons chaque choix présenté.
