# Volet Chef de Projet IT & Data (CPID)

**Rôle :** le chef d'orchestre. Cadrer, chiffrer, prioriser, gouverner, accompagner le
changement — transformer les briques techniques en **dossier de décision** vendable au
comité de pilotage.

## Livrables
| Document | Contenu |
|---|---|
| [business-case.md](business-case.md) | Coût phase 1, ROI calculé, sensibilité (généré par `business_case.py`) |
| [plan-projet.md](plan-projet.md) | Lots, jalons, dépendances, priorisation, risques |
| [gouvernance-donnees.md](gouvernance-donnees.md) | Propriété des données, RACI, qualité, conservation, accès |
| [conduite-changement.md](conduite-changement.md) | Adhésion des parties prenantes, résistances, communication |
| `dashboard_pilotage.py` | Tableau de bord de pilotage (avancement, budget, risques, valeur) |

## Le pitch en 3 chiffres (à dire en soutenance)
- **Phase 1 : 325 k€** → tient dans l'enveloppe de 450 k€ **avec 125 k€ de marge**.
- **Gisement fraude ≈ 5,7 M€/an** ; récupérable dès l'an 1 ≈ **2,3 M€**.
- **ROI ≈ 1,7 mois** — et **< 1 an même dans l'hypothèse la plus pessimiste** (sensibilité).

## Décisions de pilotage clés
1. **Détection de fraude d'abord, prévision ensuite** : la fraude a un ROI rapide et mesurable
   qui **autofinance** le programme ; la prévision (gains plus diffus) vient en lot 2.
2. **Sécurité P0 en parallèle, pas à la fin** : infra critique + données personnelles ; MFA et
   SIEM sont des jalons bloquants avant mise en service.
3. **Déploiement progressif** (pilote → généralisation) pour maîtriser le risque d'adoption.

## Gouvernance
Réponse directe au constat « personne ne pilote, ni propriété ni règles » : **RACI**,
politique de qualité (outillée : 98,46 % de relevés exploitables), durées de conservation
RGPD, accès au moindre privilège. Voir [gouvernance-donnees.md](gouvernance-donnees.md).

## Exécuter
```bash
python volet-cpid-pilotage/business_case.py       # recalcule le business case + figure ROI
python volet-cpid-pilotage/dashboard_pilotage.py  # génère le dashboard de pilotage (HTML)
```
Le HTML de pilotage est autonome (ouverture navigateur, hors ligne). Les hypothèses du
business case sont en haut de `business_case.py` : **ajustables et défendables**.
