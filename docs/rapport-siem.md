# Rapport SIEM — Détection sur les journaux de sécurité (volet Cyber)

- Période : 2026-03-01 00:23:27 → 2026-05-29 23:39:49
- 47,824 événements | 14 utilisateurs | 3290 IP sources distinctes
- Taux d'échec global : 8.2% (3,926 échecs)

## R2 — Activité depuis des IP externes (hors 10.x)

- 1 IP externes pour 48 événements (0.1% du trafic).
  - 203.0.113.45 : 48 événements, 98% d'échec

## R1 — Brute force (échecs de connexion par IP)

| IP source | Échecs | Interne ? |
|---|---|---|
| 203.0.113.45 | 47 | **NON (externe)** |
| 10.20.6.230 | 6 | oui |
| 10.20.8.155 | 6 | oui |
| 10.20.3.236 | 6 | oui |
| 10.20.4.225 | 6 | oui |
| 10.20.3.206 | 5 | oui |
| 10.20.9.196 | 5 | oui |
| 10.20.2.111 | 5 | oui |

- **Suspect principal : 203.0.113.45** avec 47 échecs (vs médiane 1 par IP).

## R3 — Tentative de compromission (échecs en rafale puis succès)

- ⚠️ L'IP 203.0.113.45 a aussi **1 connexion(s) RÉUSSIE(S)** sur le(s) compte(s) : ['a.bernard'] → signature de **compte potentiellement compromis**, à traiter en priorité.

## R4 — Comptes vus depuis un nombre anormal d'IP sources

- Anomalie structurelle : 14 utilisateurs mais 3290 IP → en moyenne 235 IP/utilisateur (attendu : quelques-unes). Signature de partage de comptes ou de proxy/rotation d'IP.
  - a.bernard : 2142 IP sources distinctes
  - s.leroy : 2128 IP sources distinctes
  - e.blanc : 2127 IP sources distinctes
  - svc_batch : 2125 IP sources distinctes
  - n.faure : 2121 IP sources distinctes

## R5 — Exports de données (risque d'exfiltration / RGPD)

- 1,436 exports de données au total.
  - c.dubois : 134 exports
  - n.faure : 120 exports
  - p.garcia : 116 exports
  - a.bernard : 116 exports
  - admin.sys : 111 exports
- Exports hors heures ouvrées (22h–6h) : **119** (8%) → à investiguer (exfiltration possible).

## R6 — Sondage de privilèges & modifications de configuration

- Accès refusés : 947 | Modifications de config : 973
- Modifications de config hors heures ouvrées : 69 (changement furtif possible).

## Règles de détection à industrialiser (SIEM/SOC)

| ID | Règle | Seuil proposé | Sévérité |
|---|---|---|---|
| R1 | Échecs de connexion répétés depuis une même IP | > 20 / heure | Haute |
| R2 | Connexion depuis IP hors plan d'adressage interne | tout événement | Moyenne |
| R3 | Échecs en rafale puis succès (même IP/compte) | motif | **Critique** |
| R4 | Compte authentifié depuis > N IP distinctes | > 5 / jour | Moyenne |
| R5 | Export de données hors heures ouvrées | tout export 22h–6h | Haute |
| R6 | Modification de configuration hors heures ouvrées | tout événement | Haute |

→ Conforme à l'exigence NIS 2 : notification d'un incident majeur **sous 24 h** (voir runbook). Détection à brancher sur un SIEM (ex. Elastic) en cible.

## Figures produites

- `siem_brute_force.png`, `siem_par_heure.png`, `siem_echecs_jour.png`
