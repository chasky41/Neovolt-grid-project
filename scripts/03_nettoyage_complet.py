"""
Néovolt Grid+ — Nettoyage COMPLET de chaque fichier source (volet Data Analyst / ILD).

Produit une version nettoyée de CHACUN des 10 fichiers d'origine, avec des règles
adaptées à chaque fichier, dans le dossier : donnees_nettoyees_separees/
  -> actifs_si_clean.csv, clients_clean.csv, ... (un "_clean.csv" par fichier)

Principe : on corrige ce qui est faux (doublons, valeurs impossibles, incohérences) ;
on NE supprime PAS l'information manquante (on la laisse vide, sans inventer de valeur).

Sorties : donnees_nettoyees_separees/*.csv + RAPPORT-NETTOYAGE-COMPLET.md
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

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
DATA_DIR = os.environ.get("NEOVOLT_DATA", os.path.normpath(os.path.join(PROJ, "..", "donnees")))
OUT = os.path.join(PROJ, "donnees_nettoyees_separees")
os.makedirs(OUT, exist_ok=True)
REPORT = os.path.join(OUT, "RAPPORT-NETTOYAGE-COMPLET.md")

buf = io.StringIO()
def log(*a):
    line = " ".join(str(x) for x in a); print(line); buf.write(line + "\n")

def charger(nom):
    return pd.read_csv(os.path.join(DATA_DIR, nom))

def nettoyer_texte(df):
    """Enlève les espaces superflus et transforme les vides en valeur manquante."""
    cols_texte = [c for c in df.columns if df[c].dtype == object]
    for c in cols_texte:
        df[c] = df[c].astype("string").str.strip()
        df[c] = df[c].replace({"": pd.NA, "nan": pd.NA, "None": pd.NA, "NaN": pd.NA})
    return df

def ecrire(df, nom_out):
    chemin = os.path.join(OUT, nom_out)
    try:
        df.to_csv(chemin, index=False, encoding="utf-8-sig")
    except PermissionError:
        print(f"\n!! {nom_out} est ouvert (Excel ?). Ferme-le et relance.\n"); sys.exit(1)
    log(f"  -> **{nom_out}** : {len(df):,} lignes")

# Chaque fonction renvoie le df nettoyé et logue ce qui a été corrigé.

def clean_actifs():
    log("\n### actifs_si.csv (inventaire des actifs)")
    df = nettoyer_texte(charger("actifs_si.csv"))
    n0 = len(df); df = df.drop_duplicates()
    df = df.drop_duplicates(subset=["id_actif"])
    df["donnees_sensibles"] = df["donnees_sensibles"].str.lower()
    log(f"- doublons retirés : {n0 - len(df)} ; colonne donnees_sensibles normalisée (oui/non)")
    ecrire(df, "actifs_si_clean.csv")

def clean_clients():
    log("\n### clients.csv (référentiel client)")
    df = nettoyer_texte(charger("clients.csv"))
    n0 = len(df); df = df.drop_duplicates().drop_duplicates(subset=["id_client"])
    df["date_entree"] = pd.to_datetime(df["date_entree"], errors="coerce")
    surf_neg = (pd.to_numeric(df["surface_m2"], errors="coerce") <= 0).sum()
    df["surface_m2"] = pd.to_numeric(df["surface_m2"], errors="coerce").where(lambda s: s > 0)
    miss_foyer = df["nb_personnes_foyer"].isna().sum()
    log(f"- doublons retirés : {n0 - len(df)} ; surfaces <=0 mises à vide : {surf_neg}")
    log(f"- nb_personnes_foyer manquant : {miss_foyer} (laissé vide, non inventé)")
    ecrire(df, "clients_clean.csv")

def clean_compteurs():
    log("\n### compteurs.csv (référentiel point de livraison)")
    df = nettoyer_texte(charger("compteurs.csv"))
    n0 = len(df); df = df.drop_duplicates().drop_duplicates(subset=["id_pdl"])
    df["date_pose"] = pd.to_datetime(df["date_pose"], errors="coerce")
    p = pd.to_numeric(df["puissance_souscrite_kva"], errors="coerce")
    bad_p = (p <= 0).sum(); df["puissance_souscrite_kva"] = p.where(p > 0)
    log(f"- doublons retirés : {n0 - len(df)} ; puissances <=0 mises à vide : {bad_p}")
    ecrire(df, "compteurs_clean.csv")

def clean_meteo():
    log("\n### meteo.csv (températures)")
    df = nettoyer_texte(charger("meteo.csv"))
    n0 = len(df); df = df.drop_duplicates().drop_duplicates(subset=["zone", "date"])
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    for c in ["temp_moyenne_c", "temp_min_c", "temp_max_c"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    # corrige les lignes où min > max (inversion) en échangeant les deux
    inv = df["temp_min_c"] > df["temp_max_c"]
    df.loc[inv, ["temp_min_c", "temp_max_c"]] = df.loc[inv, ["temp_max_c", "temp_min_c"]].values
    log(f"- doublons retirés : {n0 - len(df)} ; lignes min>max corrigées (échange) : {int(inv.sum())}")
    ecrire(df, "meteo_clean.csv")

def clean_incidents():
    log("\n### incidents_reseau.csv")
    df = nettoyer_texte(charger("incidents_reseau.csv"))
    n0 = len(df); df = df.drop_duplicates().drop_duplicates(subset=["id_incident"])
    d = pd.to_numeric(df["duree_minutes"], errors="coerce"); bad_d = (d < 0).sum()
    df["duree_minutes"] = d.where(d >= 0)
    n = pd.to_numeric(df["nb_pdl_impactes"], errors="coerce"); bad_n = (n < 0).sum()
    df["nb_pdl_impactes"] = n.where(n >= 0)
    df["date_debut"] = pd.to_datetime(df["date_debut"], errors="coerce")
    log(f"- doublons retirés : {n0 - len(df)} ; durées négatives : {bad_d} ; PDL impactés négatifs : {bad_n}")
    ecrire(df, "incidents_reseau_clean.csv")

def clean_reclamations():
    log("\n### reclamations.csv (texte libre)")
    df = nettoyer_texte(charger("reclamations.csv"))
    n0 = len(df); df = df.drop_duplicates().drop_duplicates(subset=["id_reclamation"])
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    s = pd.to_numeric(df["satisfaction"], errors="coerce")
    hors = ((s < 1) | (s > 5)).sum()
    df["satisfaction"] = s.where((s >= 1) & (s <= 5)).astype("Int64")
    vides = df["texte"].isna().sum()
    log(f"- doublons retirés : {n0 - len(df)} ; notes hors 1-5 mises à vide : {int(hors)} ; textes vides : {int(vides)}")
    ecrire(df, "reclamations_clean.csv")

def clean_journaux():
    log("\n### journaux_securite.csv")
    df = nettoyer_texte(charger("journaux_securite.csv"))
    n0 = len(df)
    df["horodatage"] = pd.to_datetime(df["horodatage"], errors="coerce")
    bad_dt = df["horodatage"].isna().sum()
    df = df.drop_duplicates()
    log(f"- doublons retirés : {n0 - len(df)} ; horodatages invalides : {int(bad_dt)}")
    ecrire(df, "journaux_securite_clean.csv")

def clean_fraude():
    log("\n### cas_fraude_confirmes.csv")
    df = nettoyer_texte(charger("cas_fraude_confirmes.csv"))
    n0 = len(df); df = df.drop_duplicates().drop_duplicates(subset=["id_pdl"])
    df["date_detection"] = pd.to_datetime(df["date_detection"], errors="coerce")
    log(f"- doublons retirés : {n0 - len(df)}")
    ecrire(df, "cas_fraude_confirmes_clean.csv")

def clean_releves(nom, cle_temps, out):
    log(f"\n### {nom} (relevés de consommation)")
    df = charger(nom)
    n0 = len(df)
    df[cle_temps] = pd.to_datetime(df[cle_temps], errors="coerce")
    df = df.drop_duplicates()
    dup_key = df.duplicated(subset=["id_pdl", cle_temps]).sum()
    if dup_key:
        df = df.groupby(["id_pdl", cle_temps], as_index=False).agg(
            consommation_kwh=("consommation_kwh", "median"), zone=("zone", "first"))
    neg = (df["consommation_kwh"] < 0).sum()
    df.loc[df["consommation_kwh"] < 0, "consommation_kwh"] = np.nan
    miss = df["consommation_kwh"].isna().sum()
    log(f"- doublons exacts + (id_pdl,{cle_temps}) retirés : {n0 - len(df):,}")
    log(f"- consommations négatives mises à vide : {int(neg):,} ; manquantes laissées vides : {int(miss):,}")
    ecrire(df, out)

def main():
    log("# Rapport de nettoyage complet — un fichier propre par source\n")
    log(f"_Source : `{DATA_DIR}`  ->  Sortie : `donnees_nettoyees_separees/`_\n")
    log("Règle générale : espaces nettoyés, doublons retirés, valeurs impossibles "
        "mises à vide, dates validées. **L'information manquante n'est jamais inventée.**\n")
    clean_actifs()
    clean_clients()
    clean_compteurs()
    clean_meteo()
    clean_incidents()
    clean_reclamations()
    clean_journaux()
    clean_fraude()
    clean_releves("releves_consommation.csv", "date", "releves_consommation_clean.csv")
    clean_releves("releves_horaires_echantillon.csv", "horodatage", "releves_horaires_echantillon_clean.csv")
    log(f"\n>> 10 fichiers nettoyés écrits dans : {OUT}")
    with open(REPORT, "w", encoding="utf-8") as fh:
        fh.write(buf.getvalue())
    log(f">> Rapport : {REPORT}")

if __name__ == "__main__":
    main()
