# Éthique, RGPD & Analyse d'impact (AIPD) — Néovolt Grid+

Ces dimensions ne sont pas un chapitre à part : elles **irriguent** nos choix (prévision de consommation, données non versionnées, accès restreints, minimisation).

## 1. Les trois tensions, arbitrées

| Tension                     | Notre arbitrage                                                                                                                                                                                        |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Valeur vs vie privée**    | On exploite les relevés pour améliorer le pilotage du réseau et la prévision de consommation, mais **par défaut en agrégé** ; le détail nominatif est restreint, justifié et journalisé. Minimisation. |
| **Innovation vs confiance** | Les modèles fournissent une **aide à la décision**, jamais une décision automatique. Les résultats restent interprétés par les équipes métier.                                                         |
| **Innovation vs criticité** | On n'expérimente pas en production sur une infrastructure critique : prototype isolé, déploiement progressif, SCADA jamais touché.                                                                     |

## 2. Conformité RGPD (synthèse)

* **Base légale** : intérêt légitime (pilotage du réseau, amélioration de la qualité de service) et exécution du contrat de fourniture ; à formaliser avec le DPO.
* **Minimisation** : on n'exploite que les données utiles ; pas de données versionnées dans le dépôt de code ; agrégation par défaut.
* **Conservation** : relevés détaillés 36 mois puis agrégation/anonymisation (cf. gouvernance).
* **Droits des personnes** : information, accès, rectification, opposition.
* **Sécurité** : chiffrement, IAM/MFA, journalisation (cohérent avec le volet Cyber).

## 3. AIPD — Analyse d'Impact relative à la Protection des Données

*(prévision de consommation énergétique — traitement nécessitant une analyse préalable des impacts potentiels sur les données personnelles)*

### 3.1 Description du traitement

Prévision de la consommation énergétique à partir des relevés de consommation, des données météorologiques et de variables temporelles afin d'aider les équipes métier à anticiper les pics de consommation et améliorer la planification énergétique.

### 3.2 Finalité & base légale

Améliorer l'exploitation du réseau, anticiper les besoins énergétiques et renforcer le pilotage opérationnel de Néovolt.

### 3.3 Données utilisées (minimisation)

Relevés de consommation, données météorologiques, période de mesure, zone géographique.

**Exclus** : aucune donnée sensible ou sans lien avec la finalité du traitement.

### 3.4 Nécessité & proportionnalité

La prévision permet d'améliorer l'anticipation des pics de consommation et la planification énergétique.

Le traitement reste proportionné car il produit uniquement des estimations agrégées servant d'aide à la décision.

### 3.5 Risques pour les personnes & mesures

| Risque                                | Mesure de réduction                                    |
| ------------------------------------- | ------------------------------------------------------ |
| Mauvaise interprétation des résultats | Validation par les équipes métier avant toute décision |
| Atteinte à la vie privée              | Minimisation, accès restreint, journalisation          |
| Réutilisation détournée des données   | Finalité limitée, gouvernance des données              |
| Fuite de données                      | Chiffrement, contrôle d'accès, supervision sécurité    |

### 3.6 Mesures complémentaires

* Revue régulière des accès.
* Documentation des traitements.
* Contrôles qualité sur les données exploitées.
* Validation périodique des performances du modèle.

### 3.7 Conclusion de l'AIPD

Le traitement apparaît compatible avec les principes du RGPD sous réserve du respect des mesures de sécurité, de gouvernance et de minimisation définies dans le projet.

L'avis du **DPO** reste requis avant toute mise en production.

## 4. Transparence & responsabilité

* Les résultats produits sont explicables et interprétés par les équipes métier.
* Les traitements reposent sur des finalités clairement définies.
* Charte d'usage des données communiquée aux parties prenantes.
* Usage de l'IA dans le projet **déclaré** (voir [annexe usage IA](annexe-usage-ia.md)).

## 5. Perspectives d'évolution

Une future phase du programme pourrait intégrer des mécanismes de détection d'anomalies ou de fraude.

Dans ce cas, une AIPD spécifique devrait être réalisée avant toute mise en œuvre opérationnelle afin d'évaluer les risques supplémentaires liés à ce nouveau traitement.

