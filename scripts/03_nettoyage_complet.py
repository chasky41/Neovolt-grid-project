"""
Néovolt Grid+ — Nettoyage COMPLET de chaque fichier source.

Méthode alignée sur l'approche R de l'équipe (cohérence de groupe) :
  1. retirer les espaces superflus ;
  2. supprimer les doublons              (équivalent de duplicated());
  3. convertir les types                 (dates en Date, colonnes numériques) ;
  4. supprimer les lignes incomplètes    (équivalent de na.omit()) ;
  5. (consommation) une valeur négative est impossible -> traitée comme manquante,
     donc retirée par na.omit. C'est le seul ajout, justifié physiquement.

Sortie : un fichier "<nom>_clean.csv" par source, dans donnees_nettoyees_separees/
Usage : .venv\\Scripts\\python.exe scripts/03_nettoyage_complet.py
"""
from __future__ import annotations
import os, io, sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
import pandas as pd
# --- Configuration environnement (chemins projet) ---
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
DATA_DIR = os.environ.get("NEOVOLT_DATA", os.path.normpath(os.path.join(PROJ, "..", "donnees")))
OUT = os.path.join(PROJ, "donnees_nettoyees_separees")
os.makedirs(OUT, exist_ok=True)
REPORT = os.path.join(OUT, "RAPPORT-NETTOYAGE-COMPLET.md")
# --- Buffer log (console + rapport markdown) ---

buf = io.StringIO()
def log(*a):
    line = " ".join(str(x) for x in a); print(line); buf.write(line + "\n")

def nettoyer_texte(df):
    for c in [c for c in df.columns if df[c].dtype == object]:
        df[c] = df[c].astype("string").str.strip()
        df[c] = df[c].replace({"": pd.NA, "nan": pd.NA, "None": pd.NA, "NaN": pd.NA})
    return df

def ecrire(df, nom_out):
    try:
        df.to_csv(os.path.join(OUT, nom_out), index=False, encoding="utf-8-sig")
    except PermissionError:
        print(f"\n!! {nom_out} est ouvert (Excel ?). Ferme-le et relance.\n"); sys.exit(1)

def traiter(nom, out, dates=(), nums=(), conso=False):
    df = nettoyer_texte(pd.read_csv(os.path.join(DATA_DIR, nom)))
    n0 = len(df)
    # 2. doublons
    df = df.drop_duplicates()
    ndup = n0 - len(df)
    # 3. types
    for c in dates:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce")
    for c in nums:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    # 5. consommation négative = impossible -> manquante
    neg = 0
    if conso and "consommation_kwh" in df.columns:
        neg = int((df["consommation_kwh"] < 0).sum())
        df.loc[df["consommation_kwh"] < 0, "consommation_kwh"] = np.nan
    if "donnees_sensibles" in df.columns:
        df["donnees_sensibles"] = df["donnees_sensibles"].str.lower()
    # 4. na.omit -> supprimer les lignes incomplètes
    n_av = len(df)
    df = df.dropna()
    nna = n_av - len(df)
    ecrire(df, out)
    extra = f", dont {neg:,} négatives" if neg else ""
    log(f"| {nom} | {n0:,} | {ndup:,} | {nna:,}{extra} | **{len(df):,}** |")

def main():
    log("# Rapport de nettoyage complet (méthode na.omit, alignée R)\n")
    log(f"_Source : `{DATA_DIR}`  ->  Sortie : `donnees_nettoyees_separees/`_\n")
    log("Pour chaque fichier : espaces nettoyés, doublons supprimés, types convertis "
        "(dates/numériques), puis **lignes incomplètes supprimées (na.omit)**. "
        "Résultat : des fichiers **sans valeur manquante et sans doublon**.\n")
    log("| Fichier | Lignes avant | Doublons retirés | Lignes incomplètes retirées | Lignes après |")
    log("|---|---|---|---|---|")
    traiter("actifs_si.csv", "actifs_si_clean.csv")
    traiter("clients.csv", "clients_clean.csv",
            dates=["date_entree"], nums=["surface_m2", "nb_personnes_foyer"])
    traiter("compteurs.csv", "compteurs_clean.csv",
            dates=["date_pose"], nums=["puissance_souscrite_kva"])
    traiter("meteo.csv", "meteo_clean.csv",
            dates=["date"], nums=["temp_moyenne_c", "temp_min_c", "temp_max_c"])
    traiter("incidents_reseau.csv", "incidents_reseau_clean.csv",
            dates=["date_debut"], nums=["duree_minutes", "nb_pdl_impactes"])
    traiter("reclamations.csv", "reclamations_clean.csv",
            dates=["date"], nums=["satisfaction"])
    traiter("journaux_securite.csv", "journaux_securite_clean.csv", dates=["horodatage"])
    traiter("cas_fraude_confirmes.csv", "cas_fraude_confirmes_clean.csv", dates=["date_detection"])
    traiter("releves_consommation.csv", "releves_consommation_clean.csv",
            dates=["date"], nums=["consommation_kwh"], conso=True)
    traiter("releves_horaires_echantillon.csv", "releves_horaires_echantillon_clean.csv",
            dates=["horodatage"], nums=["consommation_kwh"], conso=True)
    log(f"\n>> 10 fichiers nettoyés écrits dans : {OUT}")
    with open(REPORT, "w", encoding="utf-8") as fh:
        fh.write(buf.getvalue())
    log(f">> Rapport : {REPORT}")

if __name__ == "__main__":
    main()
