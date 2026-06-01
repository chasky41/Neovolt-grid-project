# Plan de gouvernance des données — Néovolt Grid+ (volet Chef de projet)

Objectif : répondre au constat « **personne n'est propriétaire des données, ni les règles
d'accès ni de conservation ne sont formalisées** » (état des lieux SI). La gouvernance
**irrigue** les autres volets (qualité côté data, accès côté sécurité, conformité côté DPO).

## 1. Domaines de données & propriété (data ownership)
| Domaine | Données | Propriétaire (métier) | Dépositaire (technique) | Sensibilité |
|---|---|---|---|---|
| Clients | référentiel client, segment, foyer | Direction Relation Client | DSI | Personnelle (RGPD) |
| Compteurs | référentiel PDL, puissance | Exploitation Réseau | DSI | Personnelle (RGPD) |
| Consommation | relevés (quotidien/horaire) | Exploitation Réseau | Pôle Données | **Personnelle sensible** |
| Réseau | incidents, postes | Exploitation Réseau | Pôle Données | Interne |
| Fraude | cas confirmés, scores | Direction Financière | Pôle Données | **Sensible (restreint)** |
| Sécurité | journaux | RSSI | RSSI | Sensible |

## 2. Matrice RACI (gouvernance des données)
*R = Réalise, A = Approuve/responsable, C = Consulté, I = Informé*

| Activité | DSI | Pôle Données | DPO | RSSI | Métier | Direction |
|---|---|---|---|---|---|---|
| Définir la politique de données | A | R | C | C | C | I |
| Qualité des données | A | R | I | I | C | I |
| Classification & accès | C | R | C | A | C | I |
| Conformité RGPD / AIPD | I | C | **A/R** | C | I | I |
| Sécurité des données | C | C | C | **A/R** | I | I |
| Durées de conservation | C | R | A | C | C | I |
| Décision d'usage (ex. fraude) | C | C | C | C | **A** (métier) | I |

## 3. Politique de qualité
- Contrôles **systématiques** à l'ingestion (doublons, valeurs négatives/aberrantes,
  manquants) — déjà outillés (pipeline ILD : **98,46 % de relevés exploitables**).
- Indicateurs qualité exposés (endpoint `/qualite`) et suivis dans le dashboard de pilotage.
- Règles de gestion documentées et **versionnées** (fini les fichiers Excel personnels).

## 4. Cycle de vie & conservation (RGPD : minimisation + limitation)
| Donnée | Durée de conservation proposée | Base |
|---|---|---|
| Relevés de consommation détaillés | 36 mois glissants, puis **agrégation/anonymisation** | Minimisation |
| Données de facturation | Durée légale comptable | Obligation légale |
| Scores / cas de fraude | Le temps de l'enquête + durée légale, puis purge | Proportionnalité |
| Journaux de sécurité | 12 mois (détection + preuve) | Sécurité / NIS 2 |

## 5. Accès — « qui a le droit de voir quoi »
- **Moindre privilège** + rôles (RBAC) ; données de consommation accessibles **agrégées**
  par défaut, détail nominatif sur justification et **journalisé**.
- L'endpoint `/fraude` (données sensibles) : rôle « enquête » uniquement, chaque accès tracé.
- Revue trimestrielle des accès ; **suppression des comptes partagés / prestataires dormants**
  (cf. anomalie SIEM : 3 290 IP pour 14 comptes).

## 6. Outillage
Licence d'outil de gouvernance (catalogue + lignage + qualité) budgétée (25 k€/an dans le
business case). En attendant : dictionnaire de données + ce document + contrôles automatisés.
