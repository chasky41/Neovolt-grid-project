# Éthique, RGPD & Analyse d'impact (AIPD) — Néovolt Grid+

Ces dimensions ne sont pas un chapitre à part : elles **irriguent** nos choix (détection
assistée et non automatique, données non versionnées, accès restreints, minimisation).

## 1. Les trois tensions, arbitrées
| Tension | Notre arbitrage |
|---|---|
| **Valeur vs vie privée** | On exploite les relevés pour le réseau et la fraude, mais **par défaut en agrégé** ; le détail nominatif est restreint, justifié et journalisé. Minimisation. |
| **Détection vs injustice** | Le modèle **priorise des enquêtes**, il ne **condamne pas**. Décision finale **humaine**. On suit le taux de faux positifs et l'équité par segment. |
| **Innovation vs criticité** | On n'expérimente pas en production sur une infra critique : prototype isolé, déploiement progressif, SCADA jamais touché. |

## 2. Conformité RGPD (synthèse)
- **Base légale** : intérêt légitime (lutte contre la fraude, équilibre du réseau) et exécution
  du contrat de fourniture ; à formaliser avec le DPO.
- **Minimisation** : on n'exploite que les données utiles ; pas de données versionnées dans
  le dépôt de code ; agrégation par défaut.
- **Conservation** : relevés détaillés 36 mois puis agrégation/anonymisation ; scores de
  fraude purgés après enquête (cf. gouvernance).
- **Droits des personnes** : information, accès, rectification, opposition ; un client peut
  contester une suspicion (recours humain).
- **Sécurité** : chiffrement, IAM/MFA, journalisation (cohérent avec le volet Cyber).

## 3. AIPD — Analyse d'Impact relative à la Protection des Données
*(traitement « détection de fraude sur les compteurs » — traitement à risque, AIPD requise)*

### 3.1 Description du traitement
Scoring d'anomalie par PDL (Isolation Forest + règles), à partir des relevés de consommation
et d'attributs compteur/client, pour **prioriser des enquêtes humaines** de fraude.

### 3.2 Finalité & base légale
Réduire les pertes non techniques (fraude) — intérêt légitime de Néovolt, proportionné à
l'enjeu (gisement estimé ~5,7 M€/an), sans se substituer au jugement humain.

### 3.3 Données utilisées (minimisation)
Relevés de consommation, puissance souscrite, type de chauffage, segment, zone.
**Exclus** : aucune donnée non nécessaire au signal de fraude ; pas de donnée de catégorie
particulière.

### 3.4 Nécessité & proportionnalité
La détection précoce (< 7 j vs plusieurs mois) est nécessaire à la finalité. Le traitement est
proportionné car il **n'entraîne pas de décision défavorable automatique** : il oriente une
vérification humaine.

### 3.5 Risques pour les personnes & mesures
| Risque | Mesure de réduction |
|---|---|
| **Accusation à tort** (faux positif) | Humain dans la boucle ; le score est une priorité d'enquête, pas une preuve |
| **Biais / discrimination** d'un segment | Suivi des taux de détection **par segment** ; revue d'équité ; pas de variable sensible |
| **Opacité** de la décision | Modèle **explicable** : chaque alerte est accompagnée de sa raison (chute de conso, ratio…) |
| **Atteinte à la vie privée** | Minimisation, accès restreint à l'équipe enquête, journalisation des consultations |
| **Réutilisation détournée** | Finalité limitée ; gouvernance et durées de conservation |

### 3.6 Mesure de l'équité (à mettre en place)
Comparer précision/rappel **par segment** (particulier, pro, industriel) pour vérifier
qu'aucun groupe n'est sur-ciblé ; seuil d'alerte ajustable selon le coût des faux positifs.

### 3.7 Conclusion de l'AIPD
Traitement **acceptable sous conditions** : maintien de l'humain dans la boucle, droit de
contestation, suivi du biais, sécurité des accès. Avis du **DPO** à recueillir avant mise en
service (jalon J2 du plan de projet).

## 4. Transparence & responsabilité
- Décisions automatisées **explicables** et contestables (droit de recours).
- Charte d'usage des données communiquée (y compris représentants du personnel : les
  données servent le réseau et la fraude, **pas le contrôle des agents**).
- Usage de l'IA dans le projet **déclaré** (voir [annexe usage IA](annexe-usage-ia.md)).
