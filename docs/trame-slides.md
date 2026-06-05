# Trame des diapositives — Soutenance Néovolt Grid+

~16 slides. Une idée par slide, peu de texte, des visuels (figures du projet).

| #  | Slide                                        | Contenu / visuel                                                                                       |
| -- | -------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| 1  | **Titre**                                    | « Néovolt Grid+ » + noms/spécialités de l'équipe + date                                                |
| 2  | **Le client & le problème**                  | Néovolt, infrastructure critique, problèmes identifiés                                                 |
| 3  | **Notre mission**                            | Cadrage + prototype en 1 semaine ; cas d'usage retenus                                                 |
| 4  | **Architecture d'ensemble**                  | Schéma d'architecture ; SCADA isolé                                                                    |
| 5  | **Données & qualité**                        | 10 jeux de données ; 512 986 relevés ; **98,46 % exploitables** après nettoyage                        |
| 6  | **Socle data (ILD)**                         | Pipeline → entrepôt → API → Docker ; capture Swagger                                                   |
| 7  | **Analyses (Data Analyst)**                  | Saisonnalité, corrélation météo/réseau, consommation par zone                                          |
| 8  | **Segmentation & réclamations**              | 4 profils clients ; analyse NLP ; satisfaction 2,45/5                                                  |
| 9  | **Prévision de consommation (Data Science)** | Démarche de modélisation ; variables météo ; comparaison des modèles ; métriques MAE, RMSE, MAPE et R² |
| 10 | **Résultats Data Science**                   | Prévision des pics de consommation ; aide à la planification énergétique ; MAPE < 10 %                 |
| 11 | **Sécurité (Cyber)**                         | Attaque détectée (a.bernard) ; figure SIEM ; supervision sécurité                                      |
| 12 | **Risque & conformité**                      | Matrice EBIOS ; RGPD ; NIS 2 ; audit DevSecOps                                                         |
| 13 | **Business case (CPID)**                     | Budget **360 k€** ; gains annuels **291 k€** ; ROI **≈ 20 mois**                                       |
| 14 | **Pilotage & gouvernance**                   | Lots ; jalons ; RACI ; conduite du changement                                                          |
| 15 | **Limites & perspectives**                   | Limites du prototype ; industrialisation ; détection d'anomalies comme évolution future                |
| 16 | **Conclusion**                               | Prototype complet, sécurisé, piloté ; recommandation de passage en phase d'industrialisation           |

## Fil rouge de la présentation

**Donnée → Information → Décision → Valeur**

1. Collecter et fiabiliser les données.
2. Exploiter les données via API et dashboards.
3. Anticiper la consommation grâce à la Data Science.
4. Sécuriser l'ensemble de la plateforme.
5. Générer de la valeur métier et un pilotage fiable.

## Visuels recommandés

* Schéma d'architecture globale.
* Swagger / API.
* Dashboard Exploitation.
* Dashboard Finance.
* Dashboard Relation Client.
* Capture du notebook Data Science.
* Résultats de métriques (MAE, RMSE, MAPE, R²).
* Figure SIEM.
* Dashboard de pilotage.
* Tableau du business case.

## Message final

« Néovolt Grid+ démontre qu'il est possible de transformer des données dispersées en un système cohérent permettant d'améliorer la qualité des données, d'anticiper la consommation énergétique, de renforcer la sécurité et d'améliorer la prise de décision. »
