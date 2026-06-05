# 🎬 Guide de démo pas-à-pas (pour débutant total)

Ce guide te dit **exactement** quoi cliquer, quoi montrer, et quoi dire devant tes camarades.
Pas besoin de comprendre le code : suis les étapes dans l'ordre. Respire, tu gères. 💪

---

## C'est quoi, en 1 phrase
> « On a construit une mini-plateforme qui prend les données brutes d'un distributeur
> d'énergie, les nettoie, **prévoit la consommation énergétique**, **affiche des tableaux de bord**, et
> **sécurise le tout** — et on a chiffré le retour sur investissement. »

---

## ÉTAPE 0 — 5 minutes AVANT de présenter (préparation)

1. Ouvre le dossier `neovolt-grid-plus`.
2. **Double-clique sur `demarrer-demo.bat`.**
3. Une fenêtre noire s'ouvre et écrit `[1/6] ... OK`, `[2/6] ... OK`, etc. **Attends** qu'elle
   affiche **« PRET POUR LA DEMO »** (environ 1 minute).
4. À la fin, **4 onglets de tableaux de bord s'ouvrent tout seuls** dans ton navigateur.
   Laisse-les ouverts.

✅ Si tu vois « PRET POUR LA DEMO », tout fonctionne. Tu peux présenter.

> Si la fenêtre affiche `[ERREUR]`, va voir la section **« Si ça plante »** plus bas.

---

## ÉTAPE 1 — Présente le problème (30 secondes, tu parles)

> « Néovolt est un distributeur d'énergie, une **infrastructure critique**. Il croule sous les
> données de compteurs mais les exploite mal : pics de consommation mal anticipés, pas de tableaux
> de bord, sécurité jamais auditée. Notre mission : un **prototype** qui répond à ça. »

*(Tu peux montrer le schéma d'architecture : ouvre docs/01-architecture-cible.md.)*

---

## ÉTAPE 2 — Montre la qualité des données (1 min)

Ouvre le fichier `docs/rapport-nettoyage.md` et montre les chiffres.

> « Les données sont réalistes donc **imparfaites**. Notre pipeline a retiré **1 286 doublons**,
> neutralisé les valeurs impossibles, et flague les valeurs aberrantes. Résultat : **98,46 %
> de relevés exploitables**. Tout est automatique et reproductible. »

---

## ÉTAPE 3 — Montre les 3 tableaux de bord (3 min) ⭐ LE PLUS VISUEL

Va sur les onglets déjà ouverts dans le navigateur. **Clique / survole** les graphiques.

### Onglet 1 — Exploitation réseau

> « Consommation du réseau jour par jour, et son lien avec la météo : plus il fait froid, plus
> on consomme. C'est ce qui sert à **anticiper les pics**. »

### Onglet 2 — Direction financière

> « Le volume d'énergie par type de client, la saisonnalité pour planifier les achats, et les
> indicateurs de consommation par segment. »

### Onglet 3 — Relation client

> « On a analysé **3 000 réclamations** automatiquement. Satisfaction moyenne **2,45/5**, et
> le sujet n°1 de mécontentement, c'est la **facturation**. »

---

## ÉTAPE 4 — Montre la prévision de consommation (2 min)

> « Notre modèle permet d'anticiper la consommation énergétique à partir des données historiques
> et des données météorologiques. Nous avons comparé plusieurs approches de Machine Learning puis
> retenu le modèle le plus performant.

> Les performances ont été évaluées à l'aide des métriques MAE, RMSE, MAPE et R². Le modèle
> retenu atteint un MAPE inférieur à 10 %, ce qui est considéré comme satisfaisant pour un cas
> d'usage de prévision énergétique.

> L'objectif n'est pas de remplacer les équipes métier mais de leur fournir une aide à la
> décision afin d'anticiper les pics de consommation, améliorer la planification du réseau et
> optimiser les achats d'énergie. »

---

## ÉTAPE 5 — Montre la sécurité (1,5 min) ⭐ L'EFFET "WAOUH"

Ouvre `docs/rapport-siem.md` et l'image
`volet-cyber/figures/siem_brute_force.png`.

> « En analysant 47 000 journaux de sécurité, on a détecté une **vraie attaque** : une adresse
> externe a essayé **47 fois** de se connecter, puis **a réussi** à pirater le compte
> "a.bernard" — un compte qui exporte des données. On a aussi scanné nos dépendances :
> **3 failles trouvées et corrigées**. »

---

## ÉTAPE 6 — Montre le pilotage et l'argent (1 min)

Va sur l'onglet **« Tableau de bord de PILOTAGE »** (le 4ᵉ ouvert).

> « Côté pilotage, nous avons construit un business case complet afin d'évaluer la viabilité
> économique du projet.

> Le budget initial du programme est estimé à **360 000 €**, avec un coût annuel de
> fonctionnement d'environ **75 000 €**.

> Les gains annuels attendus sont estimés à **291 000 €**, soit un gain net annuel de
> **216 000 €** après prise en compte des coûts de fonctionnement.

> Le retour sur investissement est estimé à environ **20 mois**, ce qui reste particulièrement
> intéressant pour un projet de transformation data de cette ampleur.

> Nous avons également défini une gouvernance des données, un plan de conduite du changement et
> un tableau de bord de pilotage pour accompagner le déploiement du programme. »

---

## ÉTAPE 7 (optionnelle, si tu te sens à l'aise) — L'API en direct

1. Double-clique sur `lancer-api.bat`.
2. Une page web s'ouvre (`http://127.0.0.1:8000/docs`).
3. Clique sur **GET /qualite** → **Try it out** → **Execute**.

> « Et tout ça est exposé par une **API** : les données propres sont disponibles pour les
> tableaux de bord et les autres outils. »

4. Pour arrêter l'API : ferme la fenêtre noire.

---

## 🧠 Antisèche — les chiffres à retenir

- 98,46 % de relevés exploitables après nettoyage.
- Modèle de prévision évalué avec MAE, RMSE, MAPE et R².
- MAPE inférieur à 10 % sur le modèle retenu.
- Réclamations : 2,45/5 de satisfaction, facturation = problème n°1.
- Sécurité : compte a.bernard compromis par l'IP 203.0.113.45 ; 3 failles corrigées.
- Budget initial : 360 k€.
- Coût annuel de fonctionnement : 75 k€.
- Gains annuels estimés : 291 k€.
- Gain net annuel estimé : 216 k€.
- ROI estimé : environ 20 mois.
- La prévision de consommation constitue le cas d'usage principal du prototype.
- La détection d'anomalies et de fraude est identifiée comme une évolution future du programme.

## 🗣️ Si on te demande « c'est l'IA qui a tout fait ? »

> « L'IA nous a aidés à coder plus vite, mais on a vérifié et corrigé. On comprend et on assume chaque choix. »

---

## 🔧 Si ça plante

| Problème | Solution |
|---|---|
| `demarrer-demo.bat` dit `[ERREUR] .venv introuvable` | Voir installation. |
| Une étape `[x/6]` échoue | Vérifier le dossier `donnees/`. |
| Les dashboards ne s'ouvrent pas | Ouvrir les `.html` manuellement. |
| L'API affiche une erreur | Attendre quelques secondes puis F5. |
| Windows bloque le `.bat` | Clic droit → Exécuter quand même. |

## ⚙️ Installation une seule fois

1. Installer Python 3.11.
2. Créer le venv.
3. Installer les dépendances.
4. Vérifier la présence du dossier `donnees/`.

## 🆘 Plan B

Montrer les rapports `.md`, les images générées ou la vidéo de démonstration enregistrée.