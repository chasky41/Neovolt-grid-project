# Journal de bord individuel — Charaf (ESIS ILD)

**Nom, prénom :** Charaf _______________________
**Spécialité :** ESIS — Ingénierie Logiciel & Data Engineering
**Groupe :** _______________________

| Jour | Ce que j'ai réalisé | Livrable ou trace associé | Difficultés rencontrées |
|------|---------------------|---------------------------|--------------------------|
| Lun 01/06 | Cadrage & mise en place : structure du dépôt, environnement reproductible (venv), diagnostic qualité des 10 jeux de données. Construction du **socle data ILD** : pipeline de nettoyage (dédup, négatifs, aberrants par PDL → 98,46 % exploitable), entrepôt SQLite (8 tables), **API FastAPI** (8 endpoints) avec smoke test 9/9, **conteneurisation Docker** (build + run validés). | Commits `J1 cadrage`, `Volet ILD pipeline+API`, `Docker` ; `docs/00-note-de-cadrage.md` ; `volet-ild-dataeng/` | Dossier à tirets non importable en module Python (lancer uvicorn depuis `api/`) ; ne pas versionner les données personnelles ni l'entrepôt (RGPD) |
| Mar 02/06 | *(à compléter)* | | |
| Mer 03/06 | *(à compléter)* | | |
| Jeu 04/06 | *(à compléter)* | | |
| Ven 05/06 | *(à compléter)* | | |

> ⚠️ À adapter à ta contribution **réelle** au fil de la semaine. La ligne de lundi reflète le
> socle ILD construit ; complète les jours suivants (intégration des résultats des modèles
> dans l'API, sécurisation, préparation des vidéos…).
