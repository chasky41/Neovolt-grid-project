# Volet Chef de Projet IT & Data (CPID)

**Rôle :** le chef d'orchestre. Cadrer, chiffrer, prioriser, gouverner et accompagner le changement afin de transformer les briques techniques en un **dossier de décision** exploitable par le comité de pilotage.

## Livrables

| Document                                         | Contenu                                                            |
| ------------------------------------------------ | ------------------------------------------------------------------ |
| [business-case.md](business-case.md)             | Budget prévisionnel, gains attendus, ROI et analyse de sensibilité |
| [plan-projet.md](plan-projet.md)                 | Lots, jalons, dépendances, priorisation et risques                 |
| [gouvernance-donnees.md](gouvernance-donnees.md) | Propriété des données, RACI, qualité, conservation et accès        |
| [conduite-changement.md](conduite-changement.md) | Adhésion des parties prenantes, résistances et communication       |
| `dashboard_pilotage.py`                          | Tableau de bord de pilotage (avancement, budget, risques, valeur)  |

## Le pitch en 3 chiffres (à dire en soutenance)

* **Budget initial estimé : 360 k€**.
* **Gains annuels estimés : 291 k€**.
* **Retour sur investissement estimé : environ 20 mois**.

## Décisions de pilotage clés

1. **Priorité au socle data et à la prévision de consommation** afin d'améliorer l'anticipation des pics de consommation et la planification énergétique.
2. **Sécurité P0 en parallèle** : infrastructure critique et données personnelles ; MFA et SIEM constituent des jalons bloquants avant toute mise en service.
3. **Déploiement progressif** (pilote puis généralisation) afin de limiter les risques techniques et organisationnels.
4. **Gouvernance des données dès le démarrage** afin de clarifier les responsabilités, les accès et les règles de qualité.

## Gouvernance

Réponse directe au constat initial : absence de gouvernance, responsabilités mal définies et règles de gestion peu formalisées.

Le projet met en place :

* une matrice **RACI** ;
* une politique de qualité des données ;
* des règles de conservation conformes au RGPD ;
* une gestion des accès basée sur le principe du moindre privilège ;
* un suivi régulier des indicateurs de qualité.

Voir : [gouvernance-donnees.md](gouvernance-donnees.md)

## Exécuter

```bash
python volet-cpid-pilotage/business_case.py
python volet-cpid-pilotage/dashboard_pilotage.py
```

Le tableau de bord de pilotage est généré au format HTML et peut être consulté directement dans un navigateur.

Les hypothèses du business case sont documentées et peuvent être ajustées afin de tester différents scénarios de coûts, de gains et de retour sur investissement.
