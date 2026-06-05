## Script — Vidéo de soutenance (20-30 min)

**Règle clé :** **chaque membre prend la parole, visage visible** (élément noté individuellement). Un membre qu'on ne voit ni n'entend perd des points. Répartir le temps.

## Déroulé proposé (≈ 25 min)

| # | Section                          | Qui                    | Durée | Messages clés                                                                                             |
| - | -------------------------------- | ---------------------- | ----- | --------------------------------------------------------------------------------------------------------- |
| 1 | **Intro & contexte**             | Chef de projet (CPID)  | 2 min | Néovolt, infrastructure critique, problèmes identifiés, mission cadrage + prototype                       |
| 2 | **Cadrage & périmètre**          | CPID                   | 2 min | Cas d'usage retenus, hypothèses, périmètre, SCADA isolé                                                   |
| 3 | **Architecture & socle (ILD)**   | ESIS ILD               | 4 min | Chaîne nettoyage → entrepôt → API → Docker, choix SQLite → PostgreSQL, démonstration API                  |
| 4 | **Analyses & dashboards**        | Data Analyst           | 4 min | Saisonnalité, corrélation météo/réseau, segmentation, NLP réclamations, dashboards                        |
| 5 | **Prévision de consommation**    | Data Scientist         | 4 min | Variables météo et temporelles, comparaison de modèles, métriques MAE/RMSE/MAPE/R², anticipation des pics |
| 6 | **Sécurité & conformité**        | Cyber                  | 4 min | Attaque détectée (a.bernard), EBIOS, audit DevSecOps, runbook NIS 2, RGPD                                 |
| 7 | **Business case & pilotage**     | CPID                   | 3 min | Budget 360 k€, gains annuels estimés, ROI ~20 mois, gouvernance, conduite du changement                   |
| 8 | **Transverses, limites & suite** | Tous (1 phrase chacun) | 2 min | Éthique, Green IT, limites assumées, perspectives d'évolution                                             |

---

## Points à savoir défendre (questions probables du jury)

### Pourquoi SQLite et pas PostgreSQL ?

Prototype qui tourne sans installation complexe ; architecture pensée pour migrer facilement vers PostgreSQL en phase d'industrialisation.

### Pourquoi avoir choisi la prévision de consommation ?

La prévision répond directement à un besoin métier identifié : anticiper les pics de consommation, améliorer la planification énergétique et optimiser les achats d'énergie.

### Votre modèle est-il fiable ?

Les performances ont été évaluées avec plusieurs métriques (MAE, RMSE, MAPE et R²). Le modèle retenu atteint un MAPE inférieur à 10 %, ce qui est satisfaisant pour un prototype de prévision énergétique.

### Les chiffres du ROI sont-ils crédibles ?

Les hypothèses sont explicites et ajustables. Une analyse de sensibilité a été réalisée afin de vérifier la robustesse du business case.

### Et le SCADA ?

Jamais touché. Il reste isolé par conception conformément aux contraintes du sujet.

### Qu'a fait l'IA, qu'avez-vous fait ?

L'IA a servi d'assistance pour accélérer certaines tâches. Les choix techniques, les vérifications, les corrections et les arbitrages ont été réalisés par l'équipe. Chaque membre comprend et assume son travail.

---

## Conseils de forme

* Chaque membre doit maîtriser son volet et être capable de répondre aux questions associées.
* Montrer 1 à 2 artefacts réels par section (dashboard, notebook, API, rapport, graphique).
* Assumer les limites du prototype plutôt que survendre les résultats.
* Filmer avec le visage visible et un son clair.
* Répéter la soutenance pour respecter le temps imparti.
* Prévoir une transition fluide entre les différents intervenants.

---

## Chiffres clés à retenir

### Données

* 512 986 relevés de consommation analysés.
* 700 points de livraison.
* 8 zones géographiques.
* 98,46 % de relevés exploitables après nettoyage.

### Data Analyst

* Satisfaction moyenne : 2,45 / 5.
* 3 000 réclamations analysées.
* Facturation = principal motif d'insatisfaction.

### Data Scientist

* Prévision de consommation énergétique.
* Comparaison de plusieurs modèles de Machine Learning.
* MAPE inférieur à 10 %.
* Anticipation des pics de consommation.

### Cybersécurité

* 47 824 événements analysés.
* Compte a.bernard compromis suite à une attaque.
* 3 vulnérabilités corrigées.

### Chef de projet

* Budget initial : 360 000 €.
* Coût annuel : 75 000 €.
* Gains annuels estimés : 291 000 €.
* Gain net annuel estimé : 216 000 €.
* ROI estimé : environ 20 mois.
.
