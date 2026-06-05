# 🎤 Présentation Néovolt Grid+ — discours complet + démo

> Légende : 🎤 = ce que tu DIS · 🖱️ = ce que tu MONTRES/FAIS · ⏱️ = durée

## ⚙️ AVANT DE COMMENCER (2 min, à faire avant que ça parle)
1. Double-clic **`demarrer-demo.bat`** → attends « PRET POUR LA DEMO » (les 4 dashboards s'ouvrent).
2. Double-clic **`lancer-docker.bat`** → le conteneur démarre + la page `/docs` s'ouvre.
3. Garde ouverts : les onglets dashboards, la page `/docs`, et Docker Desktop.

---

## 0. ACCROCHE ⏱️15 s
🎤 « Bonjour à tous. On vous présente **Néovolt Grid+**. Le principe est simple : prendre la
montagne de données des compteurs d'un distributeur d'énergie et la transformer en
**décisions concrètes** — détecter les fraudes, anticiper la consommation, et sécuriser le tout. »

## 1. LE CONTEXTE & LE PROBLÈME ⏱️1 min
🎤 « Notre client, **Néovolt**, est un distributeur d'électricité et de gaz : **600 000 foyers**,
une **infrastructure critique**. Depuis deux ans, ses compteurs communicants envoient la
consommation automatiquement. Résultat : une mine de données… mais mal exploitée.

Concrètement, Néovolt a cinq problèmes : des données **en désordre**, des **fraudes**
détectées des mois trop tard, **aucun tableau de bord** pour les décideurs, une **sécurité
jamais auditée**, et **personne qui pilote** le budget.

On nous a demandé, en une semaine, un **prototype** et un **dossier de décision** pour
prouver qu'on sait concevoir, réaliser, sécuriser et piloter la solution. »

## 2. NOTRE SOLUTION EN UNE IMAGE ⏱️1 min
🖱️ Ouvre [docs/01-architecture-cible.md](docs/01-architecture-cible.md) (montre le schéma).
🎤 « Notre solution est une **chaîne complète** : on récupère les données brutes, on les
**nettoie**, on les range dans une **base**, on les expose par une **API**, et au bout on a des
**tableaux de bord** et un **modèle de détection de fraude**. Le tout **sécurisé** et **chiffré**
côté budget. Cinq spécialités, cinq briques qui s'emboîtent. Je vous montre brique par brique. »

---

## 3. LES 5 VOLETS (avec démo)

### 3.1 — Le socle technique (mon volet : Ingénierie / Data Engineering) ⏱️2 min
🎤 « Je commence par les **fondations**, parce que sans elles rien ne tient. J'ai construit la
**tuyauterie des données**.

D'abord un **pipeline de nettoyage** : les données réelles sont pleines d'erreurs. On a retiré
**1 286 doublons**, neutralisé les valeurs impossibles, et marqué les valeurs aberrantes — en
les comparant **par type de client**, parce qu'un industriel consomme beaucoup
légitimement. Résultat : **98,46 % de données exploitables**.

Ensuite, je range tout dans une **base de données**, et je l'expose par une **API** : c'est ce
qui permet aux autres volets — analyses, modèles, dashboards — de récupérer les données
proprement. Et j'ai tout mis dans un **conteneur Docker** pour que ça tourne à l'identique
partout. Je vous montre. »

🖱️ **DÉMO API + DOCKER :**
1. Montre **Docker Desktop** → `neovolt-api` en **vert**. 🎤 « Voici notre service qui tourne, isolé, dans un conteneur. »
2. Va sur **`/docs`** → **`GET /qualite`** → *Try it out* → *Execute*.
   🎤 « En direct, l'API me renvoie la qualité : **98,46 % exploitable**. »
3. **`GET /consommation/par-zone`** → *Execute*. 🎤 « Et là, la consommation agrégée par zone, prête pour les dashboards. »

### 3.2 — Les analyses & tableaux de bord (Data Analyst) ⏱️2 min
🎤 « Une fois les données propres, on les fait **parler**. »
🖱️ Va sur les **3 onglets de dashboards** déjà ouverts.
🎤 « Trois tableaux de bord, un par décideur :
- **Exploitation** : la consommation suit la météo — plus il fait froid, plus on consomme.
  C'est ce qui sert à **anticiper les pics**.
- **Finance** : les volumes par type de client et les fraudes par catégorie.
- **Relation client** : on a analysé **3 000 réclamations** automatiquement. Satisfaction
  moyenne **2,45 sur 5**, et le sujet n°1 de mécontentement, c'est la **facturation**. »

### 3.3 — La prévision de consommation (Data Scientist) ⏱️2 min
Nous avons développé un modèle de prévision de consommation à partir des données historiques et météorologiques.

Plusieurs modèles ont été comparés à l'aide des métriques MAE, RMSE, MAPE et R².

Le modèle retenu atteint un MAPE inférieur à 10 %, ce qui permet d'obtenir des prévisions suffisamment fiables pour aider à l'anticipation des pics de consommation et à la planification énergétique.

### 3.4 — La sécurité (Cybersécurité) ⏱️2 min
🖱️ Ouvre [docs/rapport-siem.md](docs/rapport-siem.md) + [l'image SIEM](volet-cyber/figures/siem_brute_force.png).
🎤 « Néovolt, c'est une infrastructure critique : la sécurité n'est pas une option. On a analysé
**47 000 journaux** et on a trouvé une **vraie attaque** : une adresse externe a essayé de se
connecter **47 fois**, puis a **réussi** à pirater un compte qui exporte des données — donc un
risque de fuite. On a aussi **scanné nos dépendances** et **corrigé 3 failles**, et écrit un
**plan de réponse à incident** conforme à la réglementation. »

### 3.5 — Le pilotage & le budget (Chef de projet) ⏱️1,5 min
🖱️ Montre l'onglet **dashboard de pilotage**.
🎤 « Enfin, on a chiffré tout ça. Le projet est estimé à 360 000 €.

Les gains annuels estimés sont de 291 000 €,
pour un gain net annuel de 216 000 € après prise en compte des coûts de fonctionnement.

Le retour sur investissement est estimé à environ 20 mois, ce qui reste très favorable pour un projet de transformation data. »

---

## 4. LES DIMENSIONS TRANSVERSES ⏱️30 s
🎤 « Trois fils rouges traversent tout le projet : l'**éthique et le RGPD** — données
minimisées, humain dans la boucle, analyse d'impact pour la fraude ; la **sécurité dès la
conception** ; et la **sobriété** — on a travaillé sur un échantillon avant le volume, sans
gaspiller de calcul. »

## 5. CONCLUSION ⏱️30 s
🎤 « Pour résumer : on a livré une **chaîne complète**, de la donnée brute au tableau de bord,
**sécurisée** et **rentable**, avec un prototype qui **tourne vraiment**. On assume nos limites —
peu de cas de fraude pour évaluer, prototype sur échantillon — mais la démonstration est
faite : Néovolt peut lancer le projet. Merci, on répond à vos questions. »

---

## ❓ QUESTIONS PROBABLES (réponses prêtes)
- **« Pourquoi Docker ? »** → « Reproductibilité, portabilité, et c'est la base pour passer à
  l'échelle. Et on l'a vraiment testé, pas juste schématisé. »
- **« 24 fraudes, c'est fiable ? »** → « C'est pour ça qu'on fait de la détection d'anomalies et
  qu'on évalue dessus. Performance indicative, on l'assume. »
- **« Risque d'accuser des innocents ? »** → « Le score priorise une enquête, il ne condamne
  pas. Humain dans la boucle, et analyse d'impact RGPD. »
- **« Vos chiffres de ROI ? »** → « Hypothèses explicites et ajustables ; même au pire, le retour
  est sous un an. »
- **« C'est l'IA qui a tout fait ? »** → « L'IA a accéléré, mais on a vérifié et corrigé ses erreurs.
  On comprend et on assume chaque choix. »

---

## ✅ RÉCAP DES TESTS À FAIRE EN DIRECT
1. `lancer-docker.bat` → conteneur **vert** dans Docker Desktop.
2. `/docs` → **GET /qualite** → Execute → `0.9846`.
3. `/docs` → **GET /health** → Execute → `status: ok`, `511700`.
4. Les **3 dashboards** (clics/survols).
5. La **figure de fraude** + le **rapport SIEM**.
6. Le **dashboard de pilotage** (ROI).
7. `arreter-docker.bat` à la fin.
