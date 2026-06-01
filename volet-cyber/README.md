# Volet Cybersécurité & Infrastructures Critiques

**Rôle :** protéger un service essentiel. Penser comme un attaquant pour mieux défendre,
et préparer Néovolt au pire. Analyse **ancrée dans le cas réel** (actifs + journaux fournis
+ prototype réellement construit), pas une liste générique de bonnes pratiques.

## Livrables
| Document | Contenu |
|---|---|
| `analyse_journaux.py` + [rapport SIEM](../docs/rapport-siem.md) | Détection sur 47 824 événements (6 règles SOC), 3 figures |
| [analyse-risques.md](analyse-risques.md) | Cartographie des 28 actifs, scénarios EBIOS, matrice de risque, plan de traitement |
| [audit-securite-prototype.md](audit-securite-prototype.md) | Audit de notre propre prototype + scan de dépendances (DevSecOps) |
| [runbook-incident.md](runbook-incident.md) | Procédure de réponse (NIS 2 < 24 h), déroulée sur l'incident détecté |

## 🔴 Découverte majeure (à raconter en soutenance)
Le SIEM a reconstitué une **chaîne d'attaque réelle** dans les journaux :
> L'IP externe **`203.0.113.45`** a tenté **47 connexions en échec**, puis **réussi** sur le
> compte **`a.bernard`** — un compte qui réalise **116 exports de données**.
> = **brute force réussi → compte compromis → risque d'exfiltration de données personnelles.**

Autres signaux : **3 290 IP pour 14 comptes** (partage de comptes probable), 1 436 exports
(dont 119 hors heures ouvrées), 973 modifications de configuration.

## Risque n°1 & parade
**S1 : compromission de compte exposé → exfiltration RGPD.** Parades **P0** : MFA partout,
blocage après N échecs, SIEM + SOC, révocation des comptes partagés/prestataires, moindre privilège.

## Conformité (synthèse)
- **RGPD** : données de consommation = données personnelles → base légale, **minimisation**
  (on ne versionne ni n'exporte plus que le nécessaire), durée de conservation, droits des
  personnes, **AIPD obligatoire pour la détection de fraude** (voir volet éthique). Notification
  CNIL < 72 h en cas de violation.
- **NIS 2** (opérateur essentiel) : sécurité renforcée, **notification d'incident majeur < 24 h**,
  continuité de service. Gouvernance sécurité au niveau direction.
- **ISO 27001/27005** : démarche d'analyse de risque, mesures, amélioration continue.

## Continuité & reprise (PCA/PRA — éléments)
- **Sauvegardes hors-ligne testées** (anti-rançongiciel), RPO/RTO à définir par criticité.
- **Isolation maintenue du SCADA-01** : un incident sur la plateforme data ne doit pas
  atteindre la supervision réseau.
- Mode dégradé : relevé manuel de secours si la passerelle de télérelève est compromise.

## DevSecOps
- Scan de dépendances `pip-audit` → **3 CVE trouvées, corrigées, re-scan clean** (cf. audit).
- À industrialiser : scan bloquant en CI, scan d'image (Trivy), gestion centralisée des secrets,
  TLS, journalisation applicative vers le SIEM.

## Exécuter l'analyse SIEM
```bash
python volet-cyber/analyse_journaux.py
# -> docs/rapport-siem.md + 3 figures dans volet-cyber/figures/
```

## Cadre éthique
Tests et analyses **sur notre seul périmètre de projet**. Aucune action sur les systèmes
réels de Néovolt ou des tiers.
