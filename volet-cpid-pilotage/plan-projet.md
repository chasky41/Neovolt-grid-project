# Plan de projet & de portefeuille — Néovolt Grid+ (volet Chef de projet)

## 1. Découpage en lots

| Lot    | Contenu                                                                                 | Volet porteur  | Priorité              |
| ------ | --------------------------------------------------------------------------------------- | -------------- | --------------------- |
| **L0** | Cadrage, gouvernance, architecture cible                                                | CPID + tous    | Fait (sprint)         |
| **L1** | Plateforme data : ingestion, qualité, entrepôt, API                                     | ILD            | **1** (socle)         |
| **L2** | **Prévision de consommation** (modèle prédictif + intégration + suivi des performances) | Data Scientist | **1**                 |
| **L3** | Restitution : dashboards décideurs (exploitation/finance/relation client)               | Data Analyst   | 2                     |
| **L4** | Sécurité & conformité : MFA, SIEM/SOC, RGPD/AIPD                                        | Cyber          | **1** (P0 transverse) |
| **L5** | Détection d'anomalies et de fraude (perspective d'évolution)                            | Data Scientist | 3                     |
| **L6** | Conduite du changement & déploiement progressif                                         | CPID           | 2→3                   |

## 2. Priorisation argumentée (valeur × risque)

* **L1 d'abord** : aucun traitement n'est possible sans un socle data fiable et des données de qualité.
* **L2 (prévision) avant L5 (détection d'anomalies)** : la prévision de consommation apporte une valeur immédiate à Néovolt en permettant d'anticiper les besoins énergétiques, les pics de consommation et les achats d'énergie. Elle constitue également une base solide pour développer ultérieurement des mécanismes de détection d'anomalies.
* **L4 (sécurité) en parallèle dès le début** : l'infrastructure manipule des données sensibles et doit respecter les exigences de sécurité et de conformité dès la phase de conception.

## 3. Dépendances (chemin critique)

L1 (socle data) ──► L2 (prévision) ──► L6 (déploiement)
│
├──► L3 (dashboards)
└──► L5 (anomalies / fraude - évolution future)

L4 (sécurité) ─── transverse, couvre L1→L6 (jalon bloquant avant mise en service)

## 4. Jalons (phase 1 ≈ 6 mois après le prototype)

| Jalon                         | Échéance | Critère de passage                                           |
| ----------------------------- | -------- | ------------------------------------------------------------ |
| J1 — Socle data en pré-prod   | M+2      | API + qualité opérationnelles, fraîcheur J+1                 |
| J2 — Prévision en pilote      | M+3      | Modèle validé, métriques conformes aux objectifs             |
| J3 — Sécurité « go-live »     | M+4      | MFA, SIEM actif, audit externe passé                         |
| J4 — Dashboards en service    | M+5      | 3 dashboards adoptés par les directions                      |
| J5 — Bilan & décision phase 2 | M+6      | Performances mesurées, décision sur la détection d'anomalies |

## 5. Allocation des ressources (équipe phase 1)

3 profils data/dev/sécurité + 1 chef de projet + 1 expert + appui prestataire ponctuel.

La charge est calibrée pour respecter l'enveloppe budgétaire définie dans le business case.

## 6. Gestion des risques (registre projet)

| #  | Risque                                            | Prob.   | Impact   | Mitigation                                            | Porteur        |
| -- | ------------------------------------------------- | ------- | -------- | ----------------------------------------------------- | -------------- |
| R1 | Qualité des données insuffisante                  | Élevée  | Élevé    | Contrôles qualité et indicateurs suivis dès L1        | ILD            |
| R2 | Performances insuffisantes du modèle de prévision | Moyenne | Élevé    | Comparaison de plusieurs modèles, suivi MAE/RMSE/MAPE | Data Scientist |
| R3 | Rejet par les utilisateurs                        | Moyenne | Élevé    | Conduite du changement, implication des métiers       | CPID           |
| R4 | Incident de sécurité pendant le déploiement       | Moyenne | Critique | MFA, SIEM, audit de sécurité                          | RSSI           |
| R5 | Dépassement budgétaire                            | Faible  | Moyen    | Suivi des coûts et jalons go/no-go                    | CPID           |
| R6 | Dépendance fournisseur cloud                      | Faible  | Moyen    | Formats ouverts, conteneurs, réversibilité            | ILD            |

## 7. Méthode de pilotage

Pilotage Agile basé sur des sprints courts et un tableau Kanban (Trello). Les évolutions sont suivies dans GitHub afin d'assurer la traçabilité des contributions. Des points de contrôle réguliers permettent de vérifier l'avancement, la qualité des livrables et la maîtrise des risques.
