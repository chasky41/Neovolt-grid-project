# Plan de projet & de portefeuille — Néovolt Grid+ (volet Chef de projet)

## 1. Découpage en lots
| Lot | Contenu | Volet porteur | Priorité |
|---|---|---|---|
| **L0** | Cadrage, gouvernance, architecture cible | CPID + tous | Fait (sprint) |
| **L1** | Plateforme data : ingestion, qualité, entrepôt, API | ILD | **1** (socle) |
| **L2** | **Détection de fraude** (modèle + intégration + workflow enquête) | Data Scientist | **1** (ROI) |
| **L3** | Restitution : dashboards décideurs (exploitation/finance/relation client) | Data Analyst | 2 |
| **L4** | Sécurité & conformité : MFA, SIEM/SOC, RGPD/AIPD | Cyber | **1** (P0 transverse) |
| **L5** | Prévision de consommation (anticipation des pics) | Data Scientist | 3 |
| **L6** | Conduite du changement & déploiement progressif | CPID | 2→3 |

## 2. Priorisation argumentée (valeur × risque)
- **L1 d'abord** : rien n'est possible sans le socle data (les autres lots en dépendent).
- **L2 (fraude) avant L5 (prévision)** : la fraude a un **ROI rapide et mesurable** (gisement
  ≈ 5,7 M€, vérité terrain disponible) qui **autofinance** le programme dès ~1,7 mois ; la
  prévision apporte des gains réels mais plus **diffus** (achats d'équilibrage évités) → lot 2.
- **L4 (sécurité) en parallèle dès le début, pas à la fin** : infrastructure critique +
  données personnelles. Les mesures **P0** (MFA, SIEM) sont **non négociables** avant toute
  mise en service (cf. incident de compromission détecté dans les journaux).

## 3. Dépendances (chemin critique)
```
L1 (socle data) ──► L2 (fraude) ──► L6 (déploiement)
        │
        ├──► L3 (dashboards)
        └──► L5 (prévision)
L4 (sécurité) ─── transverse, couvre L1→L6 (jalon bloquant avant mise en service)
```

## 4. Jalons (phase 1 ≈ 6 mois après le prototype)
| Jalon | Échéance | Critère de passage |
|---|---|---|
| J1 — Socle data en pré-prod | M+2 | API + qualité opérationnelles, fraîcheur J+1 |
| J2 — Fraude en pilote | M+3 | Workflow d'enquête + humain dans la boucle + AIPD validée |
| J3 — Sécurité « go-live » | M+4 | MFA, SIEM actif, audit externe passé |
| J4 — Dashboards en service | M+5 | 3 dashboards adoptés par les directions |
| J5 — Bilan & décision phase 2 | M+6 | ROI mesuré, décision prévision (L5) |

## 5. Allocation des ressources (équipe phase 1)
3 profils data/dev/sécurité + 1 chef de projet + 1 expert + appui prestataire ponctuel
(détail chiffré dans [business-case.md](business-case.md)). Charge calée pour tenir dans
l'enveloppe 450 k€ avec marge.

## 6. Gestion des risques (registre projet)
| # | Risque | Prob. | Impact | Mitigation | Porteur |
|---|---|---|---|---|---|
| R1 | Qualité des données insuffisante | Élevée | Élevé | Lot qualité dès L1, indicateurs suivis | ILD |
| R2 | Modèle de fraude biaisé / faux positifs | Moyenne | Élevé | Humain dans la boucle, AIPD, suivi par segment | DS + DPO |
| R3 | Rejet par les utilisateurs (exploitants, SC) | Moyenne | Élevé | Conduite du changement L6, implication early | CPID |
| R4 | Incident de sécurité pendant le déploiement | Moyenne | Critique | L4 P0 (MFA/SIEM), runbook, audit | RSSI |
| R5 | Dépassement budgétaire | Faible | Moyen | Contingence 15 %, jalons go/no-go | CPID |
| R6 | Dépendance fournisseur cloud (lock-in) | Faible | Moyen | Formats ouverts, conteneurs, réversibilité | ILD |

## 7. Méthode de pilotage
Sprints courts + **Kanban**, revues de jalon **go/no-go**, **dépôt Git** comme source de
vérité (traçabilité), tableau de bord de pilotage (voir `dashboard_pilotage.py`).
