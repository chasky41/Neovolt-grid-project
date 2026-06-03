# Rapport de nettoyage complet (méthode na.omit, alignée R)

_Source : `C:\Users\DEll\Desktop\sujet-examenS2\donnees`  ->  Sortie : `donnees_nettoyees_separees/`_

Pour chaque fichier : espaces nettoyés, doublons supprimés, types convertis (dates/numériques), puis **lignes incomplètes supprimées (na.omit)**. Résultat : des fichiers **sans valeur manquante et sans doublon**.

| Fichier | Lignes avant | Doublons retirés | Lignes incomplètes retirées | Lignes après |
|---|---|---|---|---|
| actifs_si.csv | 28 | 0 | 0 | **28** |
| clients.csv | 700 | 0 | 274 | **426** |
| compteurs.csv | 700 | 0 | 0 | **700** |
| meteo.csv | 5,848 | 0 | 0 | **5,848** |
| incidents_reseau.csv | 420 | 0 | 0 | **420** |
| reclamations.csv | 3,000 | 0 | 0 | **3,000** |
| journaux_securite.csv | 47,824 | 0 | 0 | **47,824** |
| cas_fraude_confirmes.csv | 24 | 0 | 0 | **24** |
| releves_consommation.csv | 512,986 | 1,286 | 7,870, dont 1,032 négatives | **503,830** |
| releves_horaires_echantillon.csv | 21,600 | 0 | 0 | **21,600** |

>> 10 fichiers nettoyés écrits dans : C:\Users\DEll\Desktop\sujet-examenS2\neovolt-grid-plus\donnees_nettoyees_separees
