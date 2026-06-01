# Script — Vidéo de démonstration (5-10 min)

**Objectif :** montrer le **produit en action** (pas des diapositives). Le prototype tourne en
direct. Prévoir : entrepôt construit, venv activé, navigateur ouvert.

> Préparation (avant d'enregistrer) :
> ```bash
> python scripts/02_nettoyage.py && python volet-ild-dataeng/build_warehouse.py
> python volet-datascience/detection_fraude.py && python volet-analyst/dashboard.py
> python volet-cpid-pilotage/dashboard_pilotage.py
> ```

| Temps | Ce qu'on montre à l'écran | Ce qu'on dit (idée clé) |
|---|---|---|
| 0:00–0:30 | Titre + schéma d'architecture | « Néovolt Grid+ : de la donnée brute au tableau de bord sécurisé. Voici la chaîne. » |
| 0:30–1:30 | Terminal : `02_nettoyage.py` + rapport | « Données réalistes donc imparfaites : on retire 1 286 doublons, on neutralise les négatifs, on flague les aberrants **par PDL**. Résultat : **98,46 % exploitable**. » |
| 1:30–3:00 | `uvicorn` → navigateur `/docs` Swagger ; tester `/qualite`, `/consommation/par-zone`, `/pdl/PDL-000001/consommation` | « Les données propres sont exposées par une **API**. Voici la doc interactive ; les autres volets consomment ces endpoints. » |
| 3:00–4:30 | Terminal : `detection_fraude.py` + figure `evaluation_fraude.png` | « Détection de fraude : en investiguant **5 % des compteurs, on capte 54 % des fraudes** — lift **×10,8**. Chaque alerte a sa raison ; l'humain tranche. » |
| 4:30–6:00 | Ouvrir les 3 dashboards HTML (clics, survols) | « Trois tableaux de bord décideurs. Exploitation : pics et incidents. Finance : volumes et fraude. Relation client : la **facturation** est la douleur n°1. » |
| 6:00–7:30 | `rapport-siem.md` + figure brute force | « Côté sécurité, le SIEM a trouvé une **vraie attaque** : une IP externe a compromis le compte a.bernard. On a aussi corrigé 3 CVE de dépendances. » |
| 7:30–8:30 | `dashboard_pilotage.html` + business case | « Côté pilotage : **325 k€** sous l'enveloppe, **ROI ~1,7 mois**. La fraude finance le programme. » |
| 8:30–9:00 | Récap architecture | « Un prototype complet, sécurisé, piloté, reproductible. Merci. » |

**Conseils :** son clair, écran lisible (zoom), pas de blanc — répéter une fois. Si un script
est long, le pré-exécuter et montrer la sortie/figure plutôt que d'attendre en direct.
