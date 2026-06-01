# 🎬 Guide de démo pas-à-pas (pour débutant total)

Ce guide te dit **exactement** quoi cliquer, quoi montrer, et quoi dire devant tes camarades.
Pas besoin de comprendre le code : suis les étapes dans l'ordre. Respire, tu gères. 💪

---

## C'est quoi, en 1 phrase
> « On a construit une mini-plateforme qui prend les données brutes d'un distributeur
> d'énergie, les nettoie, **détecte les fraudes**, **affiche des tableaux de bord**, et
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
> données de compteurs mais les exploite mal : fraudes détectées trop tard, pas de tableaux
> de bord, sécurité jamais auditée. Notre mission : un **prototype** qui répond à ça. »

*(Tu peux montrer le schéma d'architecture : ouvre [docs/01-architecture-cible.md](docs/01-architecture-cible.md).)*

---

## ÉTAPE 2 — Montre la qualité des données (1 min)

Ouvre le fichier [docs/rapport-nettoyage.md](docs/rapport-nettoyage.md) et montre les chiffres.

> « Les données sont réalistes donc **imparfaites**. Notre pipeline a retiré **1 286 doublons**,
> neutralisé les valeurs impossibles, et flague les valeurs aberrantes. Résultat : **98,46 %
> de relevés exploitables**. Tout est automatique et reproductible. »

---

## ÉTAPE 3 — Montre les 3 tableaux de bord (3 min) ⭐ LE PLUS VISUEL

Va sur les onglets déjà ouverts dans le navigateur. **Clique / survole** les graphiques.

**Onglet 1 — Exploitation réseau :**
> « Consommation du réseau jour par jour, et son lien avec la météo : plus il fait froid, plus
> on consomme. C'est ce qui sert à **anticiper les pics**. »

**Onglet 2 — Direction financière :**
> « Le volume d'énergie par type de client, la saisonnalité pour planifier les achats, et les
> fraudes par type. »

**Onglet 3 — Relation client :**
> « On a analysé **3 000 réclamations** automatiquement. Satisfaction moyenne **2,45/5**, et
> le sujet n°1 de mécontentement, c'est la **facturation**. »

---

## ÉTAPE 4 — Montre la détection de fraude (2 min) ⭐ LE PLUS FORT

Ouvre l'image [volet-datascience/figures/evaluation_fraude.png](volet-datascience/figures/evaluation_fraude.png)
et le rapport [docs/rapport-detection-fraude.md](docs/rapport-detection-fraude.md).

> « Notre modèle classe les compteurs du plus au moins suspect. En contrôlant seulement
> **5 % des compteurs**, on retrouve **plus de la moitié des fraudes** : c'est **10 fois plus
> efficace** qu'un contrôle au hasard. Et chaque alerte vient avec **sa raison** (chute de
> consommation, etc.). Important : c'est une **aide à la décision, un humain tranche** — on
> n'accuse personne automatiquement. »

---

## ÉTAPE 5 — Montre la sécurité (1,5 min) ⭐ L'EFFET "WAOUH"

Ouvre [docs/rapport-siem.md](docs/rapport-siem.md) et l'image
[volet-cyber/figures/siem_brute_force.png](volet-cyber/figures/siem_brute_force.png).

> « En analysant 47 000 journaux de sécurité, on a détecté une **vraie attaque** : une adresse
> externe a essayé **47 fois** de se connecter, puis **a réussi** à pirater le compte
> "a.bernard" — un compte qui exporte des données. On a aussi scanné nos dépendances :
> **3 failles trouvées et corrigées**. »

---

## ÉTAPE 6 — Montre le pilotage et l'argent (1 min)

Va sur l'onglet **« Tableau de bord de PILOTAGE »** (le 4ᵉ ouvert).

> « Côté budget : le projet tient dans l'enveloppe de 450 000 € avec de la marge, et le
> **retour sur investissement est d'environ 1,7 mois** grâce aux fraudes récupérées. »

---

## ÉTAPE 7 (optionnelle, si tu te sens à l'aise) — L'API en direct

1. **Double-clique sur `lancer-api.bat`.**
2. Une page web s'ouvre (`http://127.0.0.1:8000/docs`). *Si elle montre une erreur, attends 3
   secondes et appuie sur **F5**.*
3. Tu vois la liste des « endpoints ». Clique sur **`GET /qualite`** → **« Try it out »** →
   **« Execute »**. Ça renvoie les chiffres de qualité en direct.

> « Et tout ça est exposé par une **API** : les données propres sont disponibles pour les
> tableaux de bord et les autres outils. »

4. Pour **arrêter l'API** : ferme la fenêtre noire (ou Ctrl+C dedans).

---

## 🧠 Antisèche — les chiffres à retenir (au cas où on te pose une question)
- **98,46 %** de relevés exploitables après nettoyage.
- Détection fraude : **×10,8** plus efficace, **54 %** des fraudes en contrôlant **5 %** des compteurs.
- Réclamations : **2,45/5** de satisfaction, **facturation** = problème n°1.
- Sécurité : compte **a.bernard** compromis par l'IP **203.0.113.45** ; **3 failles** corrigées.
- Budget : **325 k€** (sur 450 k€), **ROI ≈ 1,7 mois**, gisement fraude **≈ 5,7 M€/an**.

## 🗣️ Si on te demande « c'est l'IA qui a tout fait ? »
> « L'IA nous a aidés à coder plus vite, mais on a **vérifié et corrigé** : par exemple une
> erreur d'analyse sur la corrélation météo, et des failles de sécurité. On comprend et on
> assume chaque choix. » *(C'est déclaré dans [docs/annexe-usage-ia.md](docs/annexe-usage-ia.md).)*

---

## 🔧 Si ça plante
| Problème | Solution |
|---|---|
| `demarrer-demo.bat` dit `[ERREUR] .venv introuvable` | Voir « Installation une seule fois » ci-dessous. |
| Une étape `[x/6]` échoue | Vérifie que le dossier `donnees/` (les CSV) est bien à côté de `neovolt-grid-plus`. |
| Les dashboards ne s'ouvrent pas | Va dans `volet-analyst\dashboards\`, double-clique sur les fichiers `.html`. |
| La page de l'API montre une erreur | Attends 3 secondes, appuie sur **F5**. Vérifie que la fenêtre noire de `lancer-api.bat` est toujours ouverte. |
| Windows bloque le `.bat` | Clic droit → Propriétés → coche « Débloquer », ou clic droit → « Exécuter quand même ». |

## ⚙️ Installation une seule fois (seulement sur un NOUVEL ordi)
*(Sur ta machine actuelle, c'est déjà fait — saute cette section.)*
1. Installer **Python 3.11** (cocher « Add Python to PATH »).
2. Ouvrir un terminal dans le dossier `neovolt-grid-plus` et taper :
   ```
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. S'assurer que le dossier `donnees/` (les fichiers CSV) est à côté de `neovolt-grid-plus`.
4. Ensuite, `demarrer-demo.bat` fonctionne.

## 🆘 Plan B (si pas d'ordi ou pas le temps)
Tout est **déjà enregistré** : montre les **fichiers `.md`** (rapports) et les **images
`figures/*.png`** de chaque volet, ou la **vidéo de démonstration** que vous aurez filmée
(script dans [docs/script-video-demo.md](docs/script-video-demo.md)).
