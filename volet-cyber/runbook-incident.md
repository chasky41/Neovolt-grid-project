# Runbook de réponse à incident — Néovolt Grid+ (volet Cybersécurité)

Procédure opérationnelle de réponse, alignée **NIS 2** (notification d'un incident majeur
**sous 24 h**) et **RGPD** (notification CNIL **sous 72 h** en cas de violation de données
personnelles). Cycle : **Détection → Qualification → Confinement → Éradication →
Rétablissement → Retour d'expérience**.

## Cas d'usage déroulé : compromission de compte (incident RÉEL détecté)

> **Détecté par le SIEM (règle R3)** : l'IP externe `203.0.113.45` a enchaîné **47 échecs**
> de connexion puis **1 succès** sur le compte **`a.bernard`** — compte qui réalise par
> ailleurs **116 exports de données**. Risque : **exfiltration de données personnelles**.

### T0 → T+1h : Détection & qualification
- [ ] Alerte SIEM R3 (échecs en rafale + succès, IP externe) → astreinte SOC.
- [ ] Qualifier : compte `a.bernard`, IP `203.0.113.45`, fenêtre temporelle, périmètre accédé.
- [ ] **Déclencher la cellule de crise** si données personnelles potentiellement touchées
      (→ incident majeur probable au sens NIS 2).

### T+1h → T+4h : Confinement
- [ ] **Désactiver/verrouiller** le compte `a.bernard` ; révoquer ses sessions et jetons.
- [ ] **Bloquer l'IP** `203.0.113.45` au pare-feu (et le bloc associé).
- [ ] Forcer **réinitialisation MFA** ; rechercher d'autres comptes vus depuis cette IP.
- [ ] Geler/auditer les **exports** réalisés par le compte sur la période (preuve, ampleur).

### T+4h → T+24h : Éradication & notification
- [ ] Analyse de compromission : le compte a-t-il servi à exporter / pivoter ? Quelles données ?
- [ ] **Notification NIS 2** de l'incident majeur à l'autorité compétente **sous 24 h**.
- [ ] Si données personnelles exfiltrées → **notification CNIL sous 72 h** + information des
      personnes si risque élevé (coordination **DPO**).
- [ ] Recherche d'IOC (autres accès suspects, persistance).

### T+24h → T+72h : Rétablissement
- [ ] Rétablir le compte avec nouveau secret + MFA, sous surveillance renforcée.
- [ ] Vérifier l'intégrité des données accédées (relevés, base clients).
- [ ] Surveillance accrue (règles SIEM affinées sur le mode opératoire).

### Après : Retour d'expérience (REX)
- [ ] Post-mortem sans blâme : comment l'attaque a réussi (MFA absente ?), délais de détection.
- [ ] Mesures correctives (cf. [analyse de risque](analyse-risques.md), priorité P0 : MFA).
- [ ] Mise à jour des règles de détection et de ce runbook.

## Rôles (qui fait quoi)
| Rôle | Responsabilité |
|---|---|
| Astreinte SOC | Détection, qualification, première réaction |
| RSSI | Pilotage de la cellule de crise, décision de confinement |
| DSI | Coordination technique, rétablissement |
| DPO | Évaluation RGPD, notification CNIL, information des personnes |
| Direction / Comm | Notification NIS 2, communication externe maîtrisée |

## Autres scénarios couverts (résumé)
- **Rançongiciel** : isoler les machines, ne pas payer, restaurer depuis sauvegardes
  **hors-ligne testées**, notifier.
- **Injection de faux relevés (IoT/SCADA-02)** : isoler la passerelle, basculer en relevé de
  secours, vérifier l'intégrité, préserver l'isolation du **SCADA-01**.
- **Exfiltration via exports massifs** : couper l'accès du compte, mesurer l'ampleur (règle R5),
  notifier DPO.

## Indicateurs de réponse (à suivre)
- **MTTD** (temps moyen de détection) et **MTTR** (temps moyen de réponse).
- Délai de notification (< 24 h NIS 2 / < 72 h CNIL) — **respecté oui/non** par incident.
