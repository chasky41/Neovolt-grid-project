# Audit de sécurité du prototype — Néovolt Grid+ (volet Cybersécurité)

**Périmètre :** notre propre prototype (API FastAPI, entrepôt, conteneur, pipeline) —
audit **éthique, sur notre périmètre uniquement**, comme l'exige le sujet. Objectif :
identifier nos failles avant industrialisation, pas se déclarer parfaits.

## 1. Scan automatisé des dépendances (DevSecOps réel)

Outil : `pip-audit`. **Boucle complète menée :**

| Étape | Résultat |
|---|---|
| Scan initial (`requirements-api.txt`) | **3 vulnérabilités** sur `starlette 0.38.6` : CVE-2024-47874, CVE-2025-54121, PYSEC-2026-161 |
| Remédiation | Montée de version `fastapi 0.115 → 0.136.3` (→ `starlette 1.2.1`), `uvicorn → 0.48.0` |
| Non-régression | **Smoke test API : 9/9 OK** après upgrade |
| Re-scan | ✅ **« No known vulnerabilities found »** |

➡️ À industrialiser : `pip-audit` (ou `safety`) **bloquant dans la CI** + Dependabot.

## 2. Revue de sécurité applicative (API)

| ID | Constat | Sévérité | Recommandation |
|---|---|---|---|
| A1 | **Aucune authentification** sur l'API : les données personnelles de consommation sont accessibles sans identification | 🔴 Critique | OAuth2/JWT + clé API par consommateur ; rien d'ouvert sans auth |
| A2 | Endpoint `/fraude` expose des **données sensibles** (PDL + label fraude) sans contrôle d'accès ni journalisation | 🔴 Critique | RBAC (rôle « enquête fraude » uniquement) + traçage de chaque accès |
| A3 | Pas de **chiffrement en transit** (HTTP en prototype) | 🟠 Élevée | TLS obligatoire (reverse proxy / ingress) ; HSTS |
| A4 | Pas de **rate limiting** → scraping / brute force possibles | 🟠 Élevée | Limitation par IP/clé + verrouillage progressif |
| A5 | Pas de **journalisation d'accès** côté API (pas de piste d'audit) | 🟠 Élevée | Logs structurés → SIEM (cohérent avec les règles de détection) |
| A6 | **CORS** non configuré | 🟡 Moyenne | Liste blanche d'origines |
| A7 | Données au repos **non chiffrées** (fichier SQLite) | 🟠 Élevée | Chiffrement au repos (cible PostgreSQL UE + TDE/volume chiffré) |

## 3. Points positifs déjà en place (sécurité by design)
- ✅ **Requêtes SQL paramétrées** partout (`?`) → pas d'injection SQL.
- ✅ Conteneur **non-root** (`USER appuser`) + entrepôt monté en **lecture seule**.
- ✅ **Aucun secret en clair** dans le code ; `.env`, `*.key`, `*.pem` exclus par `.gitignore`.
- ✅ **Données personnelles jamais versionnées** (CSV, `.db`, sorties PDL ignorés) → minimisation.
- ✅ Image **légère** (pas de dépendances inutiles → surface d'attaque réduite).

## 4. Recommandations priorisées (avant mise en service)
1. **P0** — Authentification + autorisation (A1, A2) : prérequis absolu, données personnelles.
2. **P0** — `pip-audit` bloquant en CI + scan d'image conteneur (Trivy).
3. **P1** — TLS, rate limiting, journalisation → SIEM (A3, A4, A5).
4. **P1** — Chiffrement au repos + gestion centralisée des secrets (Vault / secrets manager).
5. **P2** — Tests de sécurité réguliers (OWASP ZAP sur l'API, Nmap sur le périmètre projet).

## 5. Cadre éthique
Tout test est réalisé **sur notre propre périmètre de prototype**. Aucun scan ni test
d'intrusion n'est conduit sur les systèmes réels de Néovolt ni sur des tiers.
