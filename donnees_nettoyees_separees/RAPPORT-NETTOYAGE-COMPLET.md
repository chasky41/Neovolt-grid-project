# Rapport de nettoyage complet — un fichier propre par source

_Source : `C:\Users\DEll\Desktop\sujet-examenS2\donnees`  ->  Sortie : `donnees_nettoyees_separees/`_

Règle générale : espaces nettoyés, doublons retirés, valeurs impossibles mises à vide, dates validées. **L'information manquante n'est jamais inventée.**


### actifs_si.csv (inventaire des actifs)
- doublons retirés : 0 ; colonne donnees_sensibles normalisée (oui/non)
  -> **actifs_si_clean.csv** : 28 lignes

### clients.csv (référentiel client)
- doublons retirés : 0 ; surfaces <=0 mises à vide : 0
- nb_personnes_foyer manquant : 274 (laissé vide, non inventé)
  -> **clients_clean.csv** : 700 lignes

### compteurs.csv (référentiel point de livraison)
- doublons retirés : 0 ; puissances <=0 mises à vide : 0
  -> **compteurs_clean.csv** : 700 lignes

### meteo.csv (températures)
- doublons retirés : 0 ; lignes min>max corrigées (échange) : 0
  -> **meteo_clean.csv** : 5,848 lignes

### incidents_reseau.csv
- doublons retirés : 0 ; durées négatives : 0 ; PDL impactés négatifs : 0
  -> **incidents_reseau_clean.csv** : 420 lignes

### reclamations.csv (texte libre)
- doublons retirés : 0 ; notes hors 1-5 mises à vide : 0 ; textes vides : 0
  -> **reclamations_clean.csv** : 3,000 lignes

### journaux_securite.csv
- doublons retirés : 0 ; horodatages invalides : 0
  -> **journaux_securite_clean.csv** : 47,824 lignes

### cas_fraude_confirmes.csv
- doublons retirés : 0
  -> **cas_fraude_confirmes_clean.csv** : 24 lignes

### releves_consommation.csv (relevés de consommation)
- doublons exacts + (id_pdl,date) retirés : 1,286
- consommations négatives mises à vide : 1,032 ; manquantes laissées vides : 7,870
  -> **releves_consommation_clean.csv** : 511,700 lignes

### releves_horaires_echantillon.csv (relevés de consommation)
- doublons exacts + (id_pdl,horodatage) retirés : 0
- consommations négatives mises à vide : 0 ; manquantes laissées vides : 0
  -> **releves_horaires_echantillon_clean.csv** : 21,600 lignes

>> 10 fichiers nettoyés écrits dans : C:\Users\DEll\Desktop\sujet-examenS2\neovolt-grid-plus\donnees_nettoyees_separees
