# Script — Vidéo de soutenance (20-30 min)

**Règle clé :** **chaque membre prend la parole, visage visible** (élément noté
individuellement). Un membre qu'on ne voit ni n'entend perd des points. Répartir le temps.

## Déroulé proposé (≈ 25 min)

| # | Section | Qui | Durée | Messages clés |
|---|---|---|---|---|
| 1 | **Intro & contexte** | Chef de projet (CPID) | 2 min | Néovolt, infra critique, 6 problèmes, mission cadrage+prototype |
| 2 | **Cadrage & périmètre** | CPID | 2 min | 2 cas d'usage retenus, hypothèses, périmètre, SCADA isolé |
| 3 | **Architecture & socle (ILD)** | **ESIS ILD (toi)** | 4 min | Chaîne nettoyage→entrepôt→API→Docker, choix SQLite→Postgres, démo API |
| 4 | **Analyses & dashboards** | Data Analyst | 4 min | Saisonnalité, corrélation météo réseau, segmentation, NLP réclamations, 3 dashboards |
| 5 | **Détection de fraude** | Data Scientist | 4 min | Approche non supervisée, lift ×10,8, choix « par pairs », éthique faux positifs |
| 6 | **Sécurité & conformité** | Cyber | 4 min | Attaque détectée (a.bernard), EBIOS, audit DevSecOps, runbook NIS 2, RGPD/AIPD |
| 7 | **Business case & pilotage** | CPID | 3 min | 325 k€/450 k€, ROI ~1,7 mois, priorisation, gouvernance, conduite du changement |
| 8 | **Transverses, limites & suite** | tous (1 phrase chacun) | 2 min | Éthique, Green IT, limites assumées, phase 2 |

## Points à savoir défendre (questions probables du jury)
- **Pourquoi SQLite et pas Postgres ?** Prototype qui tourne en zéro install ; code portable
  vers Postgres (réversibilité). On assume.
- **24 fraudes seulement, votre modèle est-il fiable ?** C'est pour ça qu'on fait de la
  **détection d'anomalies** (non supervisé) et qu'on **évalue** sur ces 24 cas ; performance
  indicative, pas garantie. Honnêteté assumée.
- **Risque de discriminer des clients ?** Score = priorité d'enquête, **pas un verdict** ;
  humain dans la boucle, AIPD, suivi du biais par segment.
- **Vos chiffres de ROI sont-ils crédibles ?** Hypothèses **explicites et ajustables** ;
  analyse de **sensibilité** : ROI < 1 an même au pire. On ne cache pas les hypothèses.
- **Et le SCADA ?** Jamais touché, isolé par conception. Contrainte respectée.
- **Qu'a fait l'IA, qu'avez-vous fait ?** L'IA accélère ; on a corrigé ses erreurs (piège de
  corrélation, CVE), on comprend et on assume chaque ligne.

## Conseils de forme
- Chacun **maîtrise son volet** (le sujet vérifie ça en live). Lire les README de son volet.
- Montrer 1-2 artefacts réels par section (dashboard, figure, sortie de script).
- Assumer les limites : ça inspire plus confiance que survendre.
- Filmer visage visible, son clair ; répéter le minutage.
