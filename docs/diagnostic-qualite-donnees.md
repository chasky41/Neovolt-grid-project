# Diagnostic qualité des données — Néovolt Grid+
_Source : `C:\Users\DEll\Desktop\sujet-examenS2\donnees`_


==============================================================================
1. TOUR D'HORIZON QUALITÉ (tous fichiers)
==============================================================================

### clients.csv
- Lignes : 700 | Colonnes : 7
- Colonnes : ['id_client', 'segment', 'commune', 'code_postal', 'date_entree', 'nb_personnes_foyer', 'surface_m2']
- Lignes dupliquées (toutes colonnes) : 0
  - manquants `nb_personnes_foyer` : 274 (39.1%)

### compteurs.csv
- Lignes : 700 | Colonnes : 9
- Colonnes : ['id_pdl', 'id_client', 'zone', 'type_client', 'puissance_souscrite_kva', 'type_chauffage', 'type_compteur', 'date_pose', 'statut']
- Lignes dupliquées (toutes colonnes) : 0
  - aucun manquant détecté (sur valeurs NaN ; attention aux vides/0 implicites)

### releves_consommation.csv
- Lignes : 512,986 | Colonnes : 4
- Colonnes : ['id_pdl', 'date', 'consommation_kwh', 'zone']
- Lignes dupliquées (toutes colonnes) : 1286
  - manquants `consommation_kwh` : 6856 (1.3%)

### releves_horaires_echantillon.csv
- Lignes : 21,600 | Colonnes : 4
- Colonnes : ['id_pdl', 'horodatage', 'consommation_kwh', 'zone']
- Lignes dupliquées (toutes colonnes) : 0
  - aucun manquant détecté (sur valeurs NaN ; attention aux vides/0 implicites)

### meteo.csv
- Lignes : 5,848 | Colonnes : 5
- Colonnes : ['date', 'zone', 'temp_moyenne_c', 'temp_min_c', 'temp_max_c']
- Lignes dupliquées (toutes colonnes) : 0
  - aucun manquant détecté (sur valeurs NaN ; attention aux vides/0 implicites)

### incidents_reseau.csv
- Lignes : 420 | Colonnes : 7
- Colonnes : ['id_incident', 'date_debut', 'duree_minutes', 'zone', 'type', 'nb_pdl_impactes', 'cause']
- Lignes dupliquées (toutes colonnes) : 0
  - aucun manquant détecté (sur valeurs NaN ; attention aux vides/0 implicites)

### reclamations.csv
- Lignes : 3,000 | Colonnes : 6
- Colonnes : ['id_reclamation', 'id_client', 'date', 'canal', 'texte', 'satisfaction']
- Lignes dupliquées (toutes colonnes) : 0
  - aucun manquant détecté (sur valeurs NaN ; attention aux vides/0 implicites)

### journaux_securite.csv
- Lignes : 47,824 | Colonnes : 6
- Colonnes : ['horodatage', 'utilisateur', 'source_ip', 'systeme', 'type_evenement', 'resultat']
- Lignes dupliquées (toutes colonnes) : 0
  - aucun manquant détecté (sur valeurs NaN ; attention aux vides/0 implicites)

### actifs_si.csv
- Lignes : 28 | Colonnes : 7
- Colonnes : ['id_actif', 'nom', 'type', 'criticite', 'exposition', 'proprietaire', 'donnees_sensibles']
- Lignes dupliquées (toutes colonnes) : 0
  - aucun manquant détecté (sur valeurs NaN ; attention aux vides/0 implicites)

### cas_fraude_confirmes.csv
- Lignes : 24 | Colonnes : 4
- Colonnes : ['id_pdl', 'date_detection', 'type_fraude', 'statut']
- Lignes dupliquées (toutes colonnes) : 0
  - aucun manquant détecté (sur valeurs NaN ; attention aux vides/0 implicites)

==============================================================================
2. FOCUS — releves_consommation.csv
==============================================================================
- Période : 2024-01-01 -> 2025-12-31
- Nb PDL distincts : 700
- Nb zones : 8 -> ['Bourg-Ancien', 'Centre-Ville', 'Coteaux-Ouest', 'Parc-Tertiaire', 'Plateau-Est', 'Rives-Sud', 'Val-Nord', 'Zone-Industrielle']
- Conso kWh : min=-1457.60 | médiane=14.42 | moy=80.81 | max=20766.90
- Valeurs négatives : 1034 | nulles (==0) : 639 | manquantes : 6856
- Seuil aberrant (Q3 + 3*IQR) = 153.4 kWh/j -> 47214 relevés au-dessus (9.20%)
- Doublons (id_pdl, date) : 1286
- Complétude : 512,986 relevés / 511,700 attendus (100.3%) sur 731 jours

==============================================================================
3. RÉFÉRENTIEL compteurs.csv & clients.csv
==============================================================================
- Répartition type_compteur :
    communicant: 640 (91.4%)
    ancien: 60 (8.6%)
- Répartition statut :
    actif: 673
    resilie: 27
- Répartition type_client :
    residentiel: 426
    professionnel: 211
    industriel: 63
- Répartition segment client :
    particulier: 426
    petit_pro: 131
    entreprise: 121
    collectivite: 22

==============================================================================
4. FRAUDE — cas_fraude_confirmes.csv (vérité terrain)
==============================================================================
- Nb fraudes confirmées : 24
- Types de fraude :
    sous_comptage: 14
    branchement_illicite: 6
    compteur_trafique: 4
- Statuts :
    confirmee: 24
- Taux de fraude observé (échantillon) : 24/700 = 3.43%

==============================================================================
5. RÉCLAMATIONS — reclamations.csv
==============================================================================
- Nb réclamations : 3000
- Canaux :
    courrier: 770
    telephone: 751
    email: 742
    espace_client: 737
- Satisfaction (1-5) :
    note 1: 712
    note 2: 882
    note 3: 918
    note 4: 334
    note 5: 154
  - réclamations contenant 'rgpd' : 189
  - réclamations contenant 'fraude' : 0
  - réclamations contenant 'donnee' : 189
  - réclamations contenant 'consentement' : 0
  - réclamations contenant 'panne' : 70
  - réclamations contenant 'coupure' : 701

==============================================================================
6. INCIDENTS RÉSEAU — incidents_reseau.csv
==============================================================================
- Nb incidents : 420
- Types :
    surtension: 103
    maintenance_programmee: 91
    baisse_tension: 81
    coupure: 76
    panne_poste: 69
- Durée (min) : médiane=96 | max=297
- Total PDL impactés (cumul) : 209,120
- Causes :
    inconnue: 84
    vetuste_materiel: 80
    intemperie: 74
    defaut_isolement: 65
    surcharge: 60
    travaux_tiers: 57

==============================================================================
7. JOURNAUX SÉCURITÉ — journaux_securite.csv
==============================================================================
- Période : 2026-03-01 00:23:27 -> 2026-05-29 23:39:49
- Nb événements : 47,824
- Utilisateurs distincts : 14 | IP sources distinctes : 3290
- Résultats :
    succes: 43898 (91.8%)
    echec: 3926 (8.2%)
- Types d'événements (top) :
    connexion_reussie: 41489
    connexion_echouee: 2979
    export_donnees: 1436
    modification_config: 973
    acces_refuse: 947
- Événements en échec : 3,926
  - Top IP sources d'échecs (suspicion brute force) :
      203.0.113.45: 47 échecs
      10.20.4.225: 6 échecs
      10.20.3.236: 6 échecs
      10.20.8.155: 6 échecs
      10.20.6.230: 6 échecs

==============================================================================
8. ACTIFS SI — actifs_si.csv
==============================================================================
- Nb actifs : 28
- Par criticité :
    faible: 12
    critique: 8
    elevee: 7
    moderee: 1
- Par exposition :
    interne: 22
    internet: 3
    dmz: 3
- Actifs avec données sensibles : 13 -> ['SRV-WEB-01', 'SRV-WEB-02', 'SRV-APP-10', 'SRV-DB-01', 'SRV-DB-02', 'SCADA-02', 'AD-01', 'SRV-MAIL-01', 'SRV-BI-01', 'SRV-FILE-01', 'SRV-SAUV-01', 'IOT-GW-01', 'IOT-GW-02']
