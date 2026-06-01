# Dossier projet — Néovolt Grid+

**Examen de fin de semestre — projet transverse · Équipe pluridisciplinaire**
*Document de synthèse intégrant le cadrage, l'architecture, les cinq volets métier, les
dimensions transverses et l'executive summary.*

> 📄 **Executive summary (EN)** en page dédiée : [executive-summary-EN.md](executive-summary-EN.md)

---

## Sommaire
1. [Contexte & besoin](#1-contexte--besoin)
2. [Cadrage & périmètre](#2-cadrage--périmètre)
3. [Architecture d'ensemble](#3-architecture-densemble)
4. [Les cinq volets métier](#4-les-cinq-volets-métier)
5. [Dimensions transverses](#5-dimensions-transverses)
6. [Organisation & pilotage](#6-organisation--pilotage)
7. [Résultats, limites & suite](#7-résultats-limites--suite)
8. [Index des livrables](#8-index-des-livrables)

---

## 1. Contexte & besoin
Néovolt, distributeur d'énergie (~600 000 PDL, **infrastructure critique**), sous-exploite les
données de ses compteurs communicants. Six problèmes : données en silos et de qualité
inégale, pics mal anticipés, fraudes détectées trop tard, décideurs sans tableaux de bord,
sécurité jamais auditée, aucun pilotage d'ensemble. → Programme **Néovolt Grid+**.
Détail : [note de cadrage](00-note-de-cadrage.md).

## 2. Cadrage & périmètre
Mission de **cadrage + prototype** en une semaine. **Périmètre retenu : 2 cas d'usage**
traités sérieusement (détection de fraude, prévision de consommation) portés par une
chaîne de données complète, sécurisée et pilotée. Hors périmètre assumé : production réelle,
connexion au SCADA (isolé), volume réel (architecture pensée pour). Objectifs mesurables,
hypothèses et risques : [note de cadrage](00-note-de-cadrage.md).

## 3. Architecture d'ensemble
Chaîne **sources → ingestion → qualité → entrepôt → modèles → API → restitution**, avec
sécurité et gouvernance transverses, et **SCADA isolé**. Prototype (Docker/SQLite/FastAPI)
→ cible (cloud UE/PostgreSQL/Kafka-Airflow/Kubernetes). Détail et schémas :
[architecture cible](01-architecture-cible.md).

## 4. Les cinq volets métier

### 4.1 Ingénierie Logiciel & Data Engineering (ILD)
La chaîne de données **qui tourne de bout en bout** : nettoyage documenté
(**98,46 % de relevés exploitables**), entrepôt SQLite (8 tables), **API FastAPI** (8 endpoints,
smoke test 9/9), conteneurisation **Docker** (build + run validés). Le socle que tous les
autres volets consomment. → [volet ILD](../volet-ild-dataeng/README.md).

### 4.2 Data Scientist — détection de fraude
Détection d'anomalies non supervisée (Isolation Forest + règles explicables) évaluée sur les
24 fraudes confirmées : **lift ×10,8**, **54 % des fraudes captées en investiguant 5 % des
compteurs**. Choix clé : détection **relative au groupe de pairs**. Éthique : aide à la
décision, humain dans la boucle. → [volet Data Scientist](../volet-datascience/README.md).

### 4.3 Data Analyst — analyses & dashboards
Saisonnalité (corrélation réseau/température **-0,32**), segmentation en 4 profils, **NLP de
3 000 réclamations** (satisfaction **2,45/5**, facturation = douleur n°1), et **3 dashboards
interactifs** (exploitation/finance/relation client). → [volet Data Analyst](../volet-analyst/README.md).

### 4.4 Cybersécurité
Analyse **SIEM** des 47 824 journaux : découverte d'une **attaque réelle** (IP externe ayant
brute-forcé et compromis le compte `a.bernard`). Cartographie de risque **EBIOS** (28 actifs),
**audit DevSecOps** du prototype (3 CVE corrigées), **runbook** NIS 2 (< 24 h). →
[volet Cyber](../volet-cyber/README.md).

### 4.5 Chef de projet IT & Data (CPID)
**Business case** dans l'enveloppe (**325 k€** / 450 k€), gisement fraude **~5,7 M€/an**,
**ROI ~1,7 mois** (robuste en sensibilité). Plan de projet (lots, jalons, priorisation),
**gouvernance/RACI**, conduite du changement, dashboard de pilotage. →
[volet CPID](../volet-cpid-pilotage/README.md).

## 5. Dimensions transverses (intégrées)
- **Éthique & RGPD** : minimisation, **AIPD** de la détection de fraude, humain dans la
  boucle, suivi du biais → [éthique/RGPD/AIPD](ethique-rgpd-aipd.md).
- **Sécurité by design** : MFA, SIEM, chiffrement, SCADA isolé (volet Cyber).
- **Gouvernance des données** : propriété, qualité, conservation, accès (volet CPID).
- **Green IT** : sobriété (échantillon avant volume, batch avant streaming, pas de deep
  learning gratuit), réversibilité.
- **Valeur métier** : chaque brique sert un décideur identifié + ROI chiffré.
- **Innovation** : piste d'un **assistant IA** expliquant une anomalie en langage naturel.

## 6. Organisation & pilotage
Travail tracé dans un **dépôt Git** (commits nominatifs par volet), suivi Kanban, jalons
go/no-go. Répartition par spécialité, intégration portée par le volet ILD. Détail :
[plan de projet](../volet-cpid-pilotage/plan-projet.md).

## 7. Résultats, limites & suite
**Résultats :** un prototype complet, reproductible, couvrant les 5 spécialités, avec un ROI
démontré et la sécurité/conformité intégrées.
**Limites assumées :** 24 labels de fraude seulement (évaluation indicative), business case
fondé sur des hypothèses explicites, prototype sur échantillon de 700 PDL.
**Suite recommandée :** industrialiser la fraude + le socle data (phase 1), sécurité en jalon
bloquant, prévision en lot 2 ; recueillir l'avis du DPO (AIPD) avant mise en service.

## 8. Index des livrables
Voir [liste des livrables & checklist de dépôt](liste-livrables.md).

---
*Usage de l'IA déclaré : [annexe](annexe-usage-ia.md). Chaque choix est compris et
défendable par l'équipe en soutenance.*
