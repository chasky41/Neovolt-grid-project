"""
Néovolt Grid+ — Pipeline de nettoyage & enrichissement (volet ILD / Data Eng).

Transforme les CSV bruts (imparfaits) en jeux de données propres, documentés et
reproductibles, consommables par les volets Analyst et Data Scientist.

Règles appliquées (toutes justifiées dans docs/rapport-nettoyage.md) :
  1. Doublons exacts (id_pdl, date) -> supprimés (déduplication).
  2. Consommation NÉGATIVE -> mise à NaN (physiquement impossible = erreur capteur).
  3. Consommation == 0 -> conservée mais FLAGUÉE (peut être un logement vacant).
  4. Aberrants hauts -> détectés PAR PDL (médiane + 10·MAD), FLAGUÉS et non supprimés
     (une conso élevée est normale pour un industriel : un seuil global serait faux).
  5. Manquants -> conservés en NaN + signalés (l'imputation est laissée au volet modélisation).
  6. Enrichissement -> jointures compteur + client + météo pour une table d'analyse unique.

Sorties (dans data/processed/, NON versionnées — RGPD) :
  - releves_propres.csv         : relevés nettoyés + colonnes de flags qualité
  - conso_enrichie.csv          : relevés propres + attributs compteur/client/météo
  - docs/rapport-nettoyage.md   : rapport avant/après (versionné, c'est un livrable)

Usage :  .venv\\Scripts\\python.exe scripts/02_nettoyage.py
"""
# --- Import des librairies ---
from __future__ import annotations
import os
import io
import pandas as pd
import numpy as np
# --- Configuration des chemins projet ---
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
DATA_DIR = os.environ.get("NEOVOLT_DATA", os.path.normpath(os.path.join(PROJ, "..", "donnees")))

# Dossier de sortie des données nettoyées
OUT_DIR = os.path.join(PROJ, "data", "processed")
# Rapport de nettoyage (livrable versionné)

REPORT = os.path.join(PROJ, "docs", "rapport-nettoyage.md")
os.makedirs(OUT_DIR, exist_ok=True)

buf = io.StringIO()
def log(*a):
    line = " ".join(str(x) for x in a)
    print(line)
    buf.write(line + "\n")

def load(name):
    return pd.read_csv(os.path.join(DATA_DIR, name))

def main():
    log("# Rapport de nettoyage des données — Néovolt Grid+\n")
    log(f"_Source brute : `{DATA_DIR}`_\n")

    # ----------------------------------------------------------------- CHARGEMENT
    rc = load("releves_consommation.csv")
    compteurs = load("compteurs.csv")
    clients = load("clients.csv")
    meteo = load("meteo.csv")
    n0 = len(rc)
    log(f"## 1. Relevés de consommation\n")
    log(f"- Lignes brutes : **{n0:,}**")

    rc["date"] = pd.to_datetime(rc["date"], errors="coerce")

    # --- Règle 1 : déduplication ------------------------------------------------
    dup_exact = rc.duplicated().sum()
    rc = rc.drop_duplicates()
    # s'il reste des (id_pdl, date) en conflit de valeur -> médiane (robuste)
    dup_key = rc.duplicated(subset=["id_pdl", "date"]).sum()
    if dup_key:
        agg = (rc.groupby(["id_pdl", "date"], as_index=False)
                 .agg(consommation_kwh=("consommation_kwh", "median"),
                      zone=("zone", "first")))
        rc = agg
    log(f"- Règle 1 — doublons exacts supprimés : **{dup_exact:,}** ; "
        f"conflits (id_pdl,date) résolus par médiane : **{dup_key:,}**")
    log(f"- Lignes après déduplication : **{len(rc):,}**")

    # --- Règle 2 : valeurs négatives -> NaN ------------------------------------
    neg = (rc["consommation_kwh"] < 0).sum()
    rc.loc[rc["consommation_kwh"] < 0, "consommation_kwh"] = np.nan
    log(f"- Règle 2 — valeurs négatives mises à NaN (erreur capteur) : **{neg:,}**")

    # --- Règle 3 : zéros -> flag ------------------------------------------------
    rc["flag_zero"] = (rc["consommation_kwh"] == 0).astype("int8")
    log(f"- Règle 3 — relevés à 0 conservés et flagués (vacance possible) : "
        f"**{int(rc['flag_zero'].sum()):,}**")

    # --- Règle 4 : aberrants PAR PDL (médiane + 10·MAD) ------------------------
    def mad(x):
        med = np.nanmedian(x)
        return np.nanmedian(np.abs(x - med))
    grp = rc.groupby("id_pdl")["consommation_kwh"]
    med_pdl = grp.transform("median")
    mad_pdl = grp.transform(lambda s: mad(s.values))
    # seuil robuste ; si MAD nul (PDL très stable) on ne flague pas
    seuil = med_pdl + 10 * mad_pdl.replace(0, np.nan)
    rc["flag_aberrant"] = ((rc["consommation_kwh"] > seuil) & seuil.notna()).astype("int8")
    log(f"- Règle 4 — aberrants hauts flagués (médiane + 10·MAD, **par PDL**) : "
        f"**{int(rc['flag_aberrant'].sum()):,}** "
        f"(non supprimés : une conso élevée peut être légitime pour un industriel)")

    # --- Règle 5 : manquants ----------------------------------------------------
    miss = rc["consommation_kwh"].isna().sum()
    rc["flag_manquant"] = rc["consommation_kwh"].isna().astype("int8")
    log(f"- Règle 5 — relevés manquants (NaN, dont négatifs convertis) conservés et signalés : "
        f"**{int(miss):,}** ({miss/len(rc):.2%})")

    # Indicateur qualité global
    pct_exploitable = 1 - (rc[["flag_manquant"]].sum().sum() / len(rc))
    log(f"\n**Taux de relevés directement exploitables : {pct_exploitable:.2%}**\n")

    # ----------------------------------------------------------------- ENRICHISSEMENT
    log("## 2. Enrichissement (jointures)\n")
    comp = compteurs[["id_pdl", "id_client", "type_client",
                      "puissance_souscrite_kva", "type_chauffage",
                      "type_compteur", "statut"]]
    enr = rc.merge(comp, on="id_pdl", how="left")
    n_no_comp = enr["id_client"].isna().sum()
    enr = enr.merge(clients[["id_client", "segment", "commune",
                             "nb_personnes_foyer", "surface_m2"]],
                    on="id_client", how="left")
    meteo["date"] = pd.to_datetime(meteo["date"], errors="coerce")
    enr = enr.merge(meteo, on=["zone", "date"], how="left")
    n_no_meteo = enr["temp_moyenne_c"].isna().sum()
    log(f"- Jointure compteur : {n_no_comp:,} relevés sans compteur correspondant")
    log(f"- Jointure client : sur id_client")
    log(f"- Jointure météo (zone, date) : {n_no_meteo:,} relevés sans météo")
    # variables temporelles utiles au downstream
    enr["annee"] = enr["date"].dt.year
    enr["mois"] = enr["date"].dt.month
    enr["jour_semaine"] = enr["date"].dt.dayofweek
    enr["weekend"] = (enr["jour_semaine"] >= 5).astype("int8")
    log(f"- Variables calendaires ajoutées : annee, mois, jour_semaine, weekend")
    log(f"- Table enrichie : **{len(enr):,} lignes × {len(enr.columns)} colonnes**\n")

    # ----------------------------------------------------------------- ÉCRITURE
    f1 = os.path.join(OUT_DIR, "releves_propres.csv")
    f2 = os.path.join(OUT_DIR, "conso_enrichie.csv")

    def ecrire(df, chemin):
        """Écrit le CSV, avec un message clair si le fichier est ouvert ailleurs."""
        try:
            df.to_csv(chemin, index=False)
        except PermissionError:
            nom = os.path.basename(chemin)
            print("\n" + "!" * 60)
            print(f"  IMPOSSIBLE d'écrire {nom} : le fichier est OUVERT")
            print("  dans un autre programme (Excel, Power BI, apercu...).")
            print(f"  -> Ferme {nom} puis relance.")
            print("!" * 60)
            sys.exit(1)

    ecrire(rc, f1)
    ecrire(enr, f2)
    log("## 3. Fichiers produits\n")
    log(f"- `data/processed/releves_propres.csv` ({len(rc):,} lignes)")
    log(f"- `data/processed/conso_enrichie.csv` ({len(enr):,} lignes, table d'analyse)")

    with open(REPORT, "w", encoding="utf-8") as fh:
        fh.write(buf.getvalue())
    log(f"\n>> Rapport : {REPORT}")

if __name__ == "__main__":
    main()
