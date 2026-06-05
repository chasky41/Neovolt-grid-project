# 🎤 Présentation Néovolt Grid+ — discours complet + démo

> Légende : 🎤 = ce que tu DIS · 🖱️ = ce que tu MONTRES/FAIS · ⏱️ = durée

## ⚙️ AVANT DE COMMENCER (2 min, à faire avant que ça parle)

1. Double-clic **`demarrer-demo.bat`** → attends « PRET POUR LA DEMO » (les 4 dashboards s'ouvrent).
2. Double-clic **`lancer-docker.bat`** → le conteneur démarre + la page `/docs` s'ouvre.
3. Garde ouverts : les onglets dashboards, la page `/docs`, et Docker Desktop.

---

## 0. ACCROCHE ⏱️15 s

🎤 « Bonjour à tous. On vous présente **Néovolt Grid+**. Le principe est simple : prendre la montagne de données des compteurs d'un distributeur d'énergie et la transformer en **décisions concrètes** — anticiper la consommation, améliorer le pilotage du réseau et sécuriser le tout. »

---

## 1. LE CONTEXTE & LE PROBLÈME ⏱️1 min

🎤 « Notre client, **Néovolt**, est un distributeur d'électricité et de gaz : **600 000 foyers**, une **infrastructure critique**. Depuis deux ans, ses compteurs communicants envoient la consommation automatiquement. Résultat : une mine de données… mais mal exploitée.

Concrètement, Néovolt a plusieurs problèmes : des données **en désordre**, des **pics de consommation mal anticipés**, **aucun tableau de bord** pour les décideurs, une **sécurité jamais auditée**, et **personne qui pilote** réellement le programme.

On nous a demandé, en une semaine, un **prototype** et un **dossier de décision** pour prouver qu'on sait concevoir, réaliser, sécuriser et piloter la solution. »

---

## 2. NOTRE SOLUTION EN UNE IMAGE ⏱️1 min

🖱️ Ouvre `docs/01-architecture-cible.md` (montre le schéma).

🎤 « Notre solution est une **chaîne complète** : on récupère les données brutes, on les **nettoie**, on les range dans une **base**, on les expose par une **API**, et au bout on a des **tableaux de bord** et un **modèle de prévision de consommation**.

Le tout est **sécurisé**, **gouverné** et **piloté**. Cinq spécialités, cinq briques qui s'emboîtent. Je vous montre brique par brique. »

---

# 3. LES 5 VOLETS (avec démo)

## 3.1 — Le socle technique (Ingénierie / Data Engineering) ⏱️2 min

🎤 « Je commence par les **fondations**, parce que sans elles rien ne tient. J'ai construit la **tuyauterie des données**.

D'abord un **pipeline de nettoyage** : les données réelles sont pleines d'erreurs. On a retiré **1 286 doublons**, neutralisé les valeurs impossibles, et marqué les valeurs aberrantes.

Résultat : **98,46 % de données exploitables**.

Ensuite, je range tout dans une **base de données**, et je l'expose par une **API**. C'est ce qui permet aux autres volets — analyses, modèles et dashboards — de récupérer les données proprement.

Et j'ai tout mis dans un **conteneur Docker** pour que ça tourne à l'identique partout. »

### 🖱️ DÉMO API + DOCKER

1. Docker Desktop → `neovolt-api` en vert.
2. `/docs` → `GET /qualite` → Execute.
3. `/docs` → `GET /consommation/par-zone` → Execute.

🎤 « Voici notre API en fonctionnement. »

---

## 3.2 — Les analyses & tableaux de bord (Data Analyst) ⏱️2 min

🎤 « Une fois les données propres, on les fait parler. »

🖱️ Montrer les dashboards.

🎤 « Trois tableaux de bord ont été développés :

* **Exploitation** : suivi de la consommation et des incidents réseau.
* **Finance** : volumes d'énergie et indicateurs de consommation par segment.
* **Relation client** : analyse automatique de **3 000 réclamations**.

La satisfaction moyenne est de **2,45/5** et le principal motif d'insatisfaction est la **facturation**. »

---

## 3.3 — La prévision de consommation (Data Scientist) ⏱️2 min

🖱️ Montrer le notebook et les fichiers générés.

🎤 « Nous avons développé un modèle de prévision de consommation à partir des données historiques et météorologiques.

Plusieurs modèles de Machine Learning ont été comparés.

Les performances ont été évaluées avec les métriques :

* MAE
* RMSE
* MAPE
* R²

Le modèle retenu atteint un **MAPE inférieur à 10 %**, ce qui permet d'obtenir des prévisions suffisamment fiables pour aider à anticiper les pics de consommation et améliorer la planification énergétique.

L'objectif n'est pas de remplacer les équipes métier mais de leur fournir une aide à la décision. »

---

## 3.4 — La sécurité (Cybersécurité) ⏱️2 min

🖱️ Ouvre `rapport-siem.md` + image SIEM.

🎤 « Néovolt est une infrastructure critique : la sécurité n'est pas une option.

Nous avons analysé plus de **47 000 événements** et identifié une **attaque réelle** : une adresse IP externe a tenté de se connecter à plusieurs reprises puis a compromis le compte *a.bernard*.

Nous avons également réalisé un audit de sécurité et corrigé **3 vulnérabilités**. »

---

## 3.5 — Le pilotage & le budget (Chef de projet) ⏱️1 min 30

🖱️ Ouvrir le dashboard de pilotage.

🎤 « Enfin, nous avons étudié la viabilité économique du programme.

Le budget initial est estimé à **360 000 €**.

Les gains annuels attendus sont estimés à **291 000 €**.

Après prise en compte des coûts de fonctionnement, le gain net annuel est estimé à **216 000 €**.

Le retour sur investissement est estimé à environ **20 mois**, ce qui reste très favorable pour un projet de transformation data. »

---

# 4. LES DIMENSIONS TRANSVERSES ⏱️30 s

🎤 « Trois fils rouges traversent tout le projet :

* l'**éthique et le RGPD** ;
* la **sécurité dès la conception** ;
* la **sobriété numérique**.

Les données sont minimisées, les accès sont contrôlés, et l'ensemble de l'architecture a été pensé pour rester simple et reproductible. »

---

# 5. CONCLUSION ⏱️30 s

🎤 « Pour résumer : nous avons livré une **chaîne complète**, de la donnée brute jusqu'à l'aide à la décision.

Le prototype est :

* reproductible ;
* sécurisé ;
* piloté ;
* économiquement viable.

Nous assumons les limites du prototype, mais la démonstration est faite : Néovolt dispose désormais d'une base solide pour poursuivre son programme de transformation data. Merci pour votre attention. »

---

# ❓ QUESTIONS PROBABLES

### Pourquoi Docker ?

🎤 « Pour la reproductibilité et la portabilité. »

### Pourquoi avoir choisi la prévision de consommation ?

🎤 « Parce qu'elle répond directement à un besoin métier identifié : anticiper les pics et améliorer la planification énergétique. »

### Votre modèle est-il fiable ?

🎤 « Il a été évalué avec plusieurs métriques et atteint un MAPE inférieur à 10 %, ce qui est satisfaisant pour ce prototype. »

### Vos chiffres de ROI sont-ils crédibles ?

🎤 « Les hypothèses sont explicites et ajustables. Une analyse de sensibilité a été réalisée. »

### C'est l'IA qui a tout fait ?

🎤 « L'IA nous a aidés à accélérer certaines tâches, mais tous les choix techniques ont été vérifiés et validés par l'équipe. »

---

# ✅ RÉCAP DES TESTS À FAIRE EN DIRECT

1. `lancer-docker.bat`
2. Docker Desktop → conteneur vert
3. `/docs` → `GET /qualite`
4. `/docs` → `GET /health`
5. Les dashboards
6. Notebook de prévision + résultats
7. Rapport SIEM
8. Dashboard de pilotage
9. `arreter-docker.bat`
