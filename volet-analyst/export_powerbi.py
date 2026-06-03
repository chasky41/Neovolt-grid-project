"""
Néovolt Grid+ — Export de données prêtes pour Power BI (volet Data Analyst).

Produit des fichiers CSV AGRÉGÉS (aucune donnée personnelle individuelle -> RGPD OK),
avec des noms de colonnes clairs en français, à importer directement dans Power BI
(ou Tableau / Excel).

Sortie : volet-analyst/powerbi/*.csv
Usage : .venv\\Scripts\\python.exe volet-analyst/export_powerbi.py
"""
from __future__ import annotations
import os, sys, unicodedata
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
DATA_DIR = os.environ.get("NEOVOLT_DATA", os.path.normpath(os.path.join(PROJ, "..", "donnees")))
PROC = os.path.join(PROJ, "data", "processed")
OUT = os.path.join(HERE, "powerbi"); os.makedirs(OUT, exist_ok=True)

def save(df, nom):
    p = os.path.join(OUT, nom)
    df.to_csv(p, index=False, encoding="utf-8-sig")  # utf-8-sig = accents OK dans Power BI/Excel
    print(f"  -> {nom} ({len(df)} lignes)")

def sa(s):
    return "".join(c for c in unicodedata.normalize("NFD", str(s).lower())
                   if unicodedata.category(c) != "Mn")

def main():
    print("Export Power BI :")
    enr = pd.read_csv(os.path.join(PROC, "conso_enrichie.csv"), parse_dates=["date"],
                      usecols=["date","consommation_kwh","zone","segment","type_client",
                               "temp_moyenne_c","flag_manquant","mois"])
    d = enr[enr["flag_manquant"] == 0]

    # 1. Conso par zone et par mois (séries temporelles + carte)
    d2 = d.copy(); d2["mois_annee"] = d2["date"].dt.to_period("M").astype(str)
    g = (d2.groupby(["zone","mois_annee"])["consommation_kwh"].sum()
           .reset_index().rename(columns={"consommation_kwh":"conso_kwh"}))
    save(g, "conso_par_zone_mois.csv")

    # 2. Conso moyenne par segment
    g = (d.groupby("segment")["consommation_kwh"].mean().round(1)
           .reset_index().rename(columns={"consommation_kwh":"conso_moyenne_kwh_jour"}))
    save(g, "conso_par_segment.csv")

    # 3. Saisonnalité mensuelle (conso totale réseau)
    g = (d.groupby("mois")["consommation_kwh"].sum().div(1000).round(0)
           .reset_index().rename(columns={"consommation_kwh":"conso_mwh"}))
    save(g, "saisonnalite_mensuelle.csv")

    # 4. Conso réseau vs météo (corrélation)
    g = (d.groupby("date").agg(conso_mwh=("consommation_kwh", lambda s: s.sum()/1000),
                               temp_moyenne_c=("temp_moyenne_c","mean")).round(2)
           .reset_index())
    save(g, "conso_vs_meteo.csv")

    # 5. Réclamations par thème + satisfaction
    rec = pd.read_csv(os.path.join(DATA_DIR, "reclamations.csv"))
    rec["txt"] = rec["texte"].map(sa)
    themes = {"facturation":"facture|prelevement|montant|rembours|tarif|regularisation",
              "coupure_panne":"coupure|panne|interruption|courant",
              "compteur":"compteur|releve|index|communicant",
              "donnees_rgpd":"rgpd|donnee|consentement|accord|privee",
              "relation_client":"technicien|accueil|conseiller|attente|rappel|joindre",
              "raccordement":"raccordement|branchement|mise en service|delai"}
    rows = []
    for th, pat in themes.items():
        m = rec["txt"].str.contains(pat, regex=True)
        rows.append({"theme": th, "nb_reclamations": int(m.sum()),
                     "satisfaction_moyenne": round(rec[m]["satisfaction"].mean(), 2)})
    save(pd.DataFrame(rows).sort_values("nb_reclamations", ascending=False),
         "reclamations_par_theme.csv")

    # 6. Satisfaction par canal
    g = (rec.groupby("canal")["satisfaction"].agg(["mean","count"]).round(2)
           .reset_index().rename(columns={"mean":"satisfaction_moyenne","count":"nb"}))
    save(g, "satisfaction_par_canal.csv")

    # 7. Incidents par type
    inc = pd.read_csv(os.path.join(DATA_DIR, "incidents_reseau.csv"))
    g = (inc.groupby("type").agg(nb_incidents=("id_incident","count"),
                                 pdl_impactes=("nb_pdl_impactes","sum"),
                                 duree_moyenne_min=("duree_minutes","mean")).round(0)
           .reset_index().sort_values("nb_incidents", ascending=False))
    save(g, "incidents_par_type.csv")

    # 8. Fraude par type
    fr = pd.read_csv(os.path.join(DATA_DIR, "cas_fraude_confirmes.csv"))
    g = fr["type_fraude"].value_counts().reset_index()
    g.columns = ["type_fraude", "nb_cas"]
    save(g, "fraude_par_type.csv")

    # 9. Indicateurs clés (1 ligne, pour les "cartes" Power BI)
    comp = pd.read_csv(os.path.join(DATA_DIR, "compteurs.csv"))
    kpi = pd.DataFrame([{
        "nb_pdl": d["zone"].count() and comp["id_pdl"].nunique(),
        "nb_releves_exploitables": len(d),
        "satisfaction_moyenne": round(rec["satisfaction"].mean(), 2),
        "pct_insatisfaits": round((rec["satisfaction"] <= 2).mean(), 3),
        "nb_fraudes_confirmees": len(fr),
        "taux_fraude": round(len(fr)/comp["id_pdl"].nunique(), 4),
    }])
    save(kpi, "indicateurs_cles.csv")

    print(f"\n>> 9 fichiers prêts pour Power BI dans : {OUT}")

if __name__ == "__main__":
    main()
