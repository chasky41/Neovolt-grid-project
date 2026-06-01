"""
Néovolt Grid+ — Analyse descriptive & multivariée de la consommation (volet Data Analyst).

Transforme les relevés nettoyés en compréhension métier : saisonnalité, profils de
consommation, corrélations (météo / segment / zone) et segmentation des clients.

Produit des figures (pour le rapport / les slides) + des tables d'indicateurs agrégées
(pour les dashboards) + une synthèse chiffrée.

Sorties :
  - volet-analyst/figures/*.png
  - volet-analyst/dashboards/kpi_*.csv     (agrégats pour Power BI / Plotly — non versionnés)
  - docs/analyse-descriptive.md
Usage : .venv\\Scripts\\python.exe volet-analyst/analyse_descriptive.py
"""
from __future__ import annotations
import os, io, sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

sns.set_theme(style="whitegrid")
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
PROC = os.path.join(PROJ, "data", "processed")
FIGS = os.path.join(HERE, "figures"); os.makedirs(FIGS, exist_ok=True)
DASH = os.path.join(HERE, "dashboards"); os.makedirs(DASH, exist_ok=True)
REPORT = os.path.join(PROJ, "docs", "analyse-descriptive.md")
RANDOM_STATE = 42

buf = io.StringIO()
def log(*a):
    line = " ".join(str(x) for x in a); print(line); buf.write(line + "\n")

def main():
    log("# Analyse descriptive de la consommation — Néovolt Grid+ (volet Data Analyst)\n")
    df = pd.read_csv(os.path.join(PROC, "conso_enrichie.csv"), parse_dates=["date"])
    # on travaille sur les relevés exploitables (hors manquants)
    d = df[df["flag_manquant"] == 0].copy()
    log(f"- Base d'analyse : {len(d):,} relevés exploitables, "
        f"{d['id_pdl'].nunique()} PDL, {d['zone'].nunique()} zones, "
        f"du {d['date'].min().date()} au {d['date'].max().date()}\n")

    # ---------- 1. Saisonnalité : conso totale mensuelle ----------------------
    log("## 1. Saisonnalité\n")
    d["mois_annee"] = d["date"].dt.to_period("M").dt.to_timestamp()
    mensuel = d.groupby("mois_annee")["consommation_kwh"].sum() / 1000  # MWh
    plt.figure(figsize=(9, 4))
    mensuel.plot(marker="o")
    plt.title("Consommation totale mensuelle (échantillon 700 PDL)")
    plt.ylabel("MWh / mois"); plt.xlabel("")
    plt.tight_layout(); plt.savefig(os.path.join(FIGS, "01_saisonnalite_mensuelle.png"), dpi=120); plt.close()
    hiver = d[d["mois"].isin([12, 1, 2])]["consommation_kwh"].mean()
    ete = d[d["mois"].isin([6, 7, 8])]["consommation_kwh"].mean()
    log(f"- Conso moyenne journalière : **hiver {hiver:.1f} kWh** vs **été {ete:.1f} kWh** "
        f"(ratio ×{hiver/ete:.2f}) → forte saisonnalité, pics hivernaux.")
    log(f"- Pic mensuel : {mensuel.idxmax():%B %Y} ({mensuel.max():.0f} MWh) ; "
        f"creux : {mensuel.idxmin():%B %Y} ({mensuel.min():.0f} MWh).\n")

    # ---------- 2. Profil par segment & type de client ------------------------
    log("## 2. Profils par segment et type de client\n")
    seg = d.groupby("segment")["consommation_kwh"].mean().sort_values(ascending=False)
    plt.figure(figsize=(7, 4))
    sns.barplot(x=seg.values, y=seg.index, color="#2a7")
    plt.title("Consommation journalière moyenne par segment client")
    plt.xlabel("kWh / jour"); plt.tight_layout()
    plt.savefig(os.path.join(FIGS, "02_conso_par_segment.png"), dpi=120); plt.close()
    for k, v in seg.items():
        log(f"- {k} : {v:.1f} kWh/j")
    log("")

    # ---------- 3. Corrélation conso / température ----------------------------
    log("## 3. Corrélation consommation / température\n")
    # (a) au niveau du relevé individuel : corrélation trompeuse car l'écart de TAILLE
    #     entre clients (industriel vs particulier) écrase l'effet météo.
    corr_releve = d["consommation_kwh"].corr(d["temp_moyenne_c"])
    # (b) BON niveau pour un gestionnaire de réseau : agrégat journalier du réseau.
    daily = d.groupby("date").agg(conso=("consommation_kwh", "sum"),
                                  temp=("temp_moyenne_c", "mean"))
    corr_agg = daily["conso"].corr(daily["temp"])
    # (c) sensibilité intra-PDL des logements chauffés à l'électricité
    elec = d[d["type_chauffage"] == "electrique"]
    corr_pdl_elec = (elec.groupby("id_pdl")
                     .apply(lambda g: g["consommation_kwh"].corr(g["temp_moyenne_c"]))
                     .mean())
    log(f"- Au niveau du relevé individuel : corr = **{corr_releve:.3f}** → quasi nulle, "
        f"car la variance de taille entre clients masque l'effet météo (piège classique).")
    log(f"- **Au niveau agrégé du réseau (conso totale/jour vs température/jour) : "
        f"corr = {corr_agg:.3f}** → nettement négative : plus il fait froid, plus le réseau "
        f"consomme. C'est CE signal qui sert à anticiper les pics.")
    log(f"- Sensibilité moyenne intra-PDL des logements chauffage électrique : "
        f"{corr_pdl_elec:.3f} (négative = chauffage thermosensible).")
    # graphique sur l'agrégat réseau (lisible et juste)
    plt.figure(figsize=(7, 4.5))
    sns.regplot(data=daily, x="temp", y=daily["conso"] / 1000,
                scatter_kws={"alpha": .25, "s": 14}, line_kws={"color": "red"})
    plt.title(f"Consommation réseau vs température (corr = {corr_agg:.2f})")
    plt.xlabel("Température moyenne du réseau (°C)"); plt.ylabel("Consommation totale (MWh/j)")
    plt.tight_layout(); plt.savefig(os.path.join(FIGS, "03_conso_vs_temperature.png"), dpi=120); plt.close()
    log("")

    # ---------- 4. Conso par zone ---------------------------------------------
    log("## 4. Disparités géographiques (par zone)\n")
    zone = d.groupby("zone")["consommation_kwh"].mean().sort_values(ascending=False)
    plt.figure(figsize=(8, 4))
    sns.barplot(x=zone.values, y=zone.index, color="#369")
    plt.title("Consommation journalière moyenne par zone")
    plt.xlabel("kWh / jour"); plt.tight_layout()
    plt.savefig(os.path.join(FIGS, "04_conso_par_zone.png"), dpi=120); plt.close()
    log(f"- Zone la plus consommatrice : **{zone.idxmax()}** ({zone.max():.1f} kWh/j) ; "
        f"la plus faible : {zone.idxmin()} ({zone.min():.1f} kWh/j).\n")

    # ---------- 5. Segmentation (KMeans sur profils PDL) ----------------------
    log("## 5. Segmentation des clients (KMeans sur profils de consommation)\n")
    prof = d.groupby("id_pdl").agg(
        conso_moy=("consommation_kwh", "mean"),
        cv=("consommation_kwh", lambda s: s.std() / (s.mean() + 1e-9)),
        ratio_hiver_ete=("consommation_kwh", "mean"),  # placeholder remplacé ci-dessous
    )
    hi = d[d["mois"].isin([12,1,2])].groupby("id_pdl")["consommation_kwh"].mean()
    su = d[d["mois"].isin([6,7,8])].groupby("id_pdl")["consommation_kwh"].mean()
    prof["ratio_hiver_ete"] = (hi / su).reindex(prof.index).replace([np.inf, -np.inf], np.nan).fillna(1)
    we = d.groupby(["id_pdl", "weekend"])["consommation_kwh"].mean().unstack()
    prof["ratio_weekend"] = (we[1] / we[0]).reindex(prof.index).fillna(1)
    prof = prof.dropna()
    X = StandardScaler().fit_transform(prof[["conso_moy","cv","ratio_hiver_ete","ratio_weekend"]])
    km = KMeans(n_clusters=4, random_state=RANDOM_STATE, n_init=10).fit(X)
    prof["cluster"] = km.labels_
    resume = prof.groupby("cluster").agg(
        nb_pdl=("conso_moy", "size"),
        conso_moy=("conso_moy", "mean"),
        ratio_hiver_ete=("ratio_hiver_ete", "mean"),
        ratio_weekend=("ratio_weekend", "mean")).round(2)
    log("Profils types identifiés (segmentation comportementale) :\n")
    log("| Cluster | Nb PDL | Conso moy (kWh/j) | Ratio hiver/été | Ratio week-end/semaine |")
    log("|---|---|---|---|---|")
    for c, r in resume.iterrows():
        log(f"| {c} | {int(r['nb_pdl'])} | {r['conso_moy']:.1f} | {r['ratio_hiver_ete']:.2f} | {r['ratio_weekend']:.2f} |")
    plt.figure(figsize=(7, 4.5))
    sns.scatterplot(data=prof, x="conso_moy", y="ratio_hiver_ete",
                    hue="cluster", palette="tab10", s=25, alpha=.7)
    plt.xlim(0, prof["conso_moy"].quantile(0.97))
    plt.title("Segmentation des clients par profil de consommation")
    plt.xlabel("Consommation moyenne (kWh/j)"); plt.ylabel("Ratio hiver/été")
    plt.tight_layout(); plt.savefig(os.path.join(FIGS, "05_segmentation_clients.png"), dpi=120); plt.close()
    log("")

    # ---------- Exports KPI agrégés (pour dashboards / Power BI) ---------------
    mensuel.reset_index().rename(columns={"consommation_kwh":"conso_mwh"}).to_csv(
        os.path.join(DASH, "kpi_conso_mensuelle.csv"), index=False)
    d.groupby(["zone","mois_annee"])["consommation_kwh"].sum().reset_index().to_csv(
        os.path.join(DASH, "kpi_conso_zone_mois.csv"), index=False)
    seg.reset_index().to_csv(os.path.join(DASH, "kpi_conso_segment.csv"), index=False)

    log("## Figures & exports produits\n")
    log("- 5 figures dans `volet-analyst/figures/`")
    log("- 3 tables d'indicateurs agrégées dans `volet-analyst/dashboards/` (import Power BI / Plotly)")

    with open(REPORT, "w", encoding="utf-8") as fh:
        fh.write(buf.getvalue())
    log(f"\n>> Rapport : {REPORT}")

if __name__ == "__main__":
    main()
