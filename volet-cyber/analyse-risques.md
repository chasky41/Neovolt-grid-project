# Analyse de risque — Néovolt Grid+ (volet Cybersécurité)

Méthode : inspirée d'**EBIOS Risk Manager** (cadrage → biens supports → événements
redoutés → scénarios → traitement) et du référentiel **ISO 27001/27005**. Néovolt est un
**opérateur d'infrastructure critique** soumis à **NIS 2**. L'analyse est ancrée dans
l'inventaire réel des actifs (`donnees/actifs_si.csv`) et dans les **signaux d'attaque
observés** dans les journaux (voir [rapport SIEM](../docs/rapport-siem.md)).

## 1. Périmètre & valeurs métier à protéger
- **Continuité de la distribution d'énergie** (service essentiel).
- **Données personnelles de consommation** (RGPD) — 600 000 clients.
- **Intégrité des relevés** (base de la facturation et de la détection de fraude).
- **Image et conformité** (NIS 2, RGPD).

## 2. Biens supports (cartographie — 28 actifs)
| Catégorie | Actifs | Criticité | Exposition |
|---|---|---|---|
| Exposés Internet/DMZ | SRV-WEB-01, SRV-WEB-02, SCADA-02, VPN-01, FW-01, SRV-MAIL-01 | critique/élevée | **internet/dmz** |
| Données sensibles | SRV-DB-01, SRV-DB-02, SRV-APP-10 (data lake), AD-01 | **critique** | interne |
| Industriel / OT | **SCADA-01** (isolé), SCADA-02, IOT-GW-01/02 | critique/élevée | interne/dmz |
| Support | SRV-BI-01, SRV-FILE-01, SRV-SAUV-01, 12 postes | élevée→faible | interne |

8 actifs critiques, 13 portant des données sensibles, 6 exposés (internet/DMZ) =
**surface d'attaque prioritaire**.

## 3. Événements redoutés
| ER | Description | Impact |
|---|---|---|
| ER1 | Fuite de données personnelles de consommation | RGPD, sanction CNIL, perte de confiance |
| ER2 | Manipulation/falsification des relevés | Pertes financières, fraude facilitée |
| ER3 | Interruption de la distribution / supervision | Continuité de service (vital), NIS 2 |
| ER4 | Indisponibilité de la plateforme data | Décisions à l'aveugle, retour aux silos |

## 4. Scénarios de risque (gravité × vraisemblance)

| ID | Scénario | Bien support | ER | Gravité | Vraisemb. | Risque |
|---|---|---|---|---|---|---|
| **S1** | **Brute force Internet → compte à privilèges compromis → exfiltration** (⚠️ **OBSERVÉ** : `203.0.113.45` a réussi sur `a.bernard`, qui exporte des données) | VPN-01, AD-01, SRV-APP-10 | ER1 | Critique | **Forte (avérée)** | 🔴 **Critique** |
| S2 | Attaque de la passerelle télérelève (DMZ) → injection de faux relevés / pivot | SCADA-02, IOT-GW | ER2/ER3 | Critique | Moyenne | 🔴 Élevé |
| S3 | Rançongiciel via mail/poste → chiffrement des bases | SRV-MAIL-01, PC-*, SRV-DB | ER3/ER4 | Critique | Moyenne | 🔴 Élevé |
| S4 | Exfiltration via exports massifs / comptes de service (svc_batch, admin.sys) | SRV-APP-10, SRV-DB | ER1 | Élevée | Moyenne | 🟠 Élevé |
| S5 | Abus de **comptes prestataires à droits élevés** (signalés dans le SI existant) | AD-01, tous | ER1/ER2 | Élevée | Moyenne | 🟠 Élevé |
| S6 | Compromission concentrateur IoT → déni / faux relevés de masse | IOT-GW-01/02 | ER2/ER3 | Élevée | Faible | 🟡 Moyen |

> ⚠️ **S1 n'est pas hypothétique** : la chaîne échecs-en-rafale-puis-succès depuis une IP
> externe est visible dans les journaux. C'est le risque n°1 à traiter.

## 5. Écarts du socle de sécurité (constats)
- Pas d'**inventaire de risque à jour**, gestion des accès **hétérogène**, **comptes
  prestataires à droits élevés** (source : état des lieux SI).
- **MFA absente** sur les accès exposés (VPN, portail) → brute force possible (S1).
- **3 290 IP sources pour 14 comptes** → forte suspicion de **partage de comptes** /
  absence de cloisonnement (R4 du SIEM).
- Pas de **SIEM/SOC** : les attaques ne sont pas détectées en temps réel.

## 6. Plan de traitement (mesures priorisées)
| Priorité | Mesure | Couvre | Coût indicatif |
|---|---|---|---|
| **P0** | **MFA** sur VPN, portail, AD + blocage IP après N échecs | S1 | faible (config) |
| **P0** | Déployer le **SIEM** + les 6 règles de détection (voir SIEM) + SOC d'astreinte | S1-S6 | moyen |
| **P0** | Révoquer/cloisonner les **comptes partagés et prestataires**, principe du moindre privilège | S1, S5 | faible |
| P1 | **Segmentation réseau** : maintenir SCADA **isolé**, durcir la DMZ (SCADA-02) | S2 | moyen |
| P1 | **Chiffrement au repos** des données conso + **DLP** sur les exports | S1, S4 | moyen |
| P1 | Durcir les **comptes de service** (svc_batch), pas d'export interactif | S4 | faible |
| P2 | EDR + plan de patch (vétusté matériel signalée), durcissement IoT (mTLS compteurs) | S3, S6 | élevé |
| P2 | Sauvegardes hors-ligne testées (anti-rançongiciel), PCA/PRA | S3 | moyen |

## 7. Lien avec l'architecture du projet
- Le **SCADA reste isolé** (choix d'architecture imposé et respecté).
- L'**API** expose des données personnelles → authentification + journalisation + endpoint
  `/fraude` restreint (voir [audit du prototype](audit-securite-prototype.md)).
- La détection de fraude est une **décision assistée** (humain dans la boucle) → pas de
  décision défavorable automatique (exigence RGPD + éthique).
