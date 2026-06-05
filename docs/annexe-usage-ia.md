# Annexe — Déclaration d'usage de l'intelligence artificielle

Conformément aux règles de l'examen, voici comment l'équipe a utilisé un assistant d'IA, à
quelles étapes, et comment nous garantissons que **nous maîtrisons et assumons** chaque livrable.

## Outil utilisé
Assistant d'IA générative (Claude, via Claude Code) — utilisé comme **pair-programmeur et
rédacteur assistant**, sous supervision humaine constante.

## À quelles étapes
| Étape | Usage de l'IA | Contrôle humain |
|---|---|---|
| Analyse du sujet & cadrage | Synthèse du dossier de cas, structuration de la note de cadrage | Relecture, validation du périmètre et des hypothèses |
| Code (pipeline, API, modèles, analyses) | Génération et refactorisation de code Python | Exécution, tests, lecture ligne à ligne, correction de bugs |
| Analyses & modèles | Proposition de features, préparation des données, comparaison de modèles de Machine Learning | Vérification des résultats, correction du piège de corrélation, choix des variables métier et validation des performances |
| Documentation | Rédaction des rapports et README | Vérification des chiffres, ajustement du discours métier |
| Sécurité | Règles de détection, structure EBIOS/AIPD | Validation de la cohérence avec le cas Néovolt |

## Ce que nous garantissons (responsabilité)
- **Reproductibilité** : tout le code s'exécute depuis le dépôt ; les chiffres cités sont
  produits par nos scripts (diagnostic, nettoyage, modèles, business case), pas inventés.
- **Compréhension** : chaque membre peut **expliquer et défendre** son volet (les README
  documentent la démarche et les points à défendre). C'est l'objet de la soutenance filmée.
- **Vérification** : nous avons détecté et corrigé des erreurs proposées par l'IA (ex. piège de
  corrélation conso/température au niveau du relevé, bug d'affichage, vulnérabilités de
  dépendances). L'IA accélère, elle ne décide pas à notre place.
- **Honnêteté** : les limites sont assumées (peu de labels de fraude, hypothèses du business
  case explicitées, performance indicative).

## Décisions humaines non déléguées
Le choix du périmètre, la priorisation (prévision de consommation), les arbitrages éthiques
(humain dans la boucle, minimisation), et l'interprétation métier des résultats sont des
**décisions de l'équipe**, éclairées mais non remplacées par l'IA.
