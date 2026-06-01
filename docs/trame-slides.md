# Trame des diapositives — Soutenance Néovolt Grid+

~16 slides. Une idée par slide, peu de texte, des visuels (figures du projet).

| # | Slide | Contenu / visuel |
|---|---|---|
| 1 | **Titre** | « Néovolt Grid+ » + noms/spécialités de l'équipe + date |
| 2 | **Le client & le problème** | Néovolt, infra critique, 6 problèmes (icônes) |
| 3 | **Notre mission** | Cadrage + prototype en 1 semaine ; 2 cas d'usage retenus |
| 4 | **Architecture d'ensemble** | Le schéma (diagramme Mermaid exporté) ; SCADA isolé |
| 5 | **Données & qualité** | 10 jeux ; 512 986 relevés ; **98,46 % exploitable** après nettoyage |
| 6 | **Socle data (ILD)** | Pipeline→entrepôt→API→Docker ; capture Swagger |
| 7 | **Analyses (Analyst)** | Saisonnalité + corrélation météo réseau (fig. `03`) |
| 8 | **Segmentation & réclamations** | 4 profils + thèmes réclamations (fig. `05`, `07`) |
| 9 | **Détection de fraude (DS)** | Courbe d'évaluation (fig. `evaluation_fraude`) ; **lift ×10,8** |
| 10 | **Éthique de la fraude** | Humain dans la boucle, faux positifs, AIPD |
| 11 | **Sécurité (Cyber)** | L'attaque détectée (a.bernard) ; fig. `siem_brute_force` |
| 12 | **Risque & conformité** | Matrice EBIOS ; RGPD / NIS 2 ; audit DevSecOps |
| 13 | **Business case (CPID)** | 325 k€/450 k€ ; **ROI ~1,7 mois** ; fig. `roi_cumul` |
| 14 | **Pilotage & gouvernance** | Lots/jalons ; RACI ; conduite du changement |
| 15 | **Limites & suite** | Limites assumées ; phase 2 ; innovation (assistant IA) |
| 16 | **Conclusion** | Prototype complet, sécurisé, piloté ; appel à décision |

**Astuce :** réutiliser les figures déjà générées (`volet-*/figures/*.png`) et le schéma
d'architecture. Garder un fil rouge : **donnée → décision → valeur, en sécurité**.
