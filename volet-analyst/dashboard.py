"""
Néovolt Grid+ — Tableaux de bord décisionnels interactifs (volet Data Analyst).

Génère 3 dashboards HTML autonomes (Plotly), un par profil de décideur :
  1. Exploitation réseau  — anticipation des pics, incidents, géographie
  2. Direction financière — volumes (revenu), fraude, saisonnalité des achats
  3. Relation client      — thèmes de réclamation, satisfaction

Les HTML sont AUTONOMES (Plotly embarqué) : ouvrables hors ligne pour la vidéo démo.
Ils n'exposent que des AGRÉGATS (aucun PDL individuel) → conformes RGPD.

Sorties : volet-analyst/dashboards/*.html
Usage : .venv\\Scripts\\python.exe volet-analyst/dashboard.py
"""
from __future__ import annotations
import os, sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
DATA_DIR = os.environ.get("NEOVOLT_DATA", os.path.normpath(os.path.join(PROJ, "..", "donnees")))
PROC = os.path.join(PROJ, "data", "processed")
DASH = os.path.join(HERE, "dashboards"); os.makedirs(DASH, exist_ok=True)
BLEU, VERT, ROUGE, ORANGE = "#2c7fb8", "#27ae60", "#c0392b", "#e67e22"

def save(fig, name, titre):
    fig.update_layout(title_text=titre, title_font_size=20, template="plotly_white",
                      height=720, showlegend=True, margin=dict(t=90))
    path = os.path.join(DASH, name)
    fig.write_html(path, include_plotlyjs=True, full_html=True)
    print(f"  -> {name}")

def main():
    enr = pd.read_csv(os.path.join(PROC, "conso_enrichie.csv"), parse_dates=["date"],
                      usecols=["date","consommation_kwh","zone","segment","type_chauffage",
                               "temp_moyenne_c","flag_manquant","mois"])
    d = enr[enr["flag_manquant"] == 0]
    inc = pd.read_csv(os.path.join(DATA_DIR, "incidents_reseau.csv"))
    rec = pd.read_csv(os.path.join(DATA_DIR, "reclamations.csv"))
    fra = pd.read_csv(os.path.join(DATA_DIR, "cas_fraude_confirmes.csv"))
    print("Génération des dashboards :")

    # ===================== 1. EXPLOITATION RÉSEAU =========================
    daily = d.groupby("date").agg(conso=("consommation_kwh","sum"),
                                  temp=("temp_moyenne_c","mean")).reset_index()
    daily["conso_mwh"] = daily["conso"] / 1000
    zone = d.groupby("zone")["consommation_kwh"].mean().sort_values()
    inc_type = inc.groupby("type").agg(n=("id_incident","count"),
                                       pdl=("nb_pdl_impactes","sum")).sort_values("n")
    fig = make_subplots(rows=2, cols=2,
        subplot_titles=("Consommation réseau quotidienne (MWh)",
                        "Consommation vs température (anticipation des pics)",
                        "Consommation moyenne par zone (kWh/j)",
                        "Incidents réseau par type (nb)"))
    fig.add_trace(go.Scatter(x=daily["date"], y=daily["conso_mwh"], line=dict(color=BLEU),
                             name="Conso MWh"), 1, 1)
    fig.add_trace(go.Scatter(x=daily["temp"], y=daily["conso_mwh"], mode="markers",
                             marker=dict(color=ORANGE, size=5, opacity=.5), name="jour"), 1, 2)
    fig.add_trace(go.Bar(x=zone.values, y=zone.index, orientation="h",
                         marker_color=BLEU, name="kWh/j"), 2, 1)
    fig.add_trace(go.Bar(x=inc_type["n"].values, y=inc_type.index, orientation="h",
                         marker_color=ROUGE, name="incidents"), 2, 2)
    fig.update_xaxes(title_text="Température (°C)", row=1, col=2)
    save(fig, "1_dashboard_exploitation.html",
         "Néovolt Grid+ — Tableau de bord EXPLOITATION RÉSEAU")

    # ===================== 2. DIRECTION FINANCIÈRE ========================
    seg_vol = d.groupby("segment")["consommation_kwh"].sum().sort_values() / 1000
    mensuel = (d.groupby("mois")["consommation_kwh"].sum() / 1000)
    fra_type = fra["type_fraude"].value_counts()
    fig = make_subplots(rows=2, cols=2,
        subplot_titles=("Volume d'énergie par segment (MWh) — base de revenu",
                        "Saisonnalité mensuelle (pilotage des achats d'énergie)",
                        "Fraudes confirmées par type",
                        "Indicateurs clés"),
        specs=[[{"type":"bar"},{"type":"bar"}],[{"type":"bar"},{"type":"indicator"}]])
    fig.add_trace(go.Bar(x=seg_vol.values, y=seg_vol.index, orientation="h",
                         marker_color=VERT, name="MWh"), 1, 1)
    fig.add_trace(go.Bar(x=mensuel.index, y=mensuel.values, marker_color=BLEU,
                         name="MWh/mois"), 1, 2)
    fig.add_trace(go.Bar(x=fra_type.index, y=fra_type.values, marker_color=ROUGE,
                         name="fraudes"), 2, 1)
    fig.add_trace(go.Indicator(mode="number+delta", value=len(fra),
                  title={"text":"Fraudes confirmées<br>(taux 3,4% de l'échantillon)"},
                  number={"suffix":" cas"}), 2, 2)
    fig.update_xaxes(title_text="Mois", row=1, col=2)
    save(fig, "2_dashboard_finance.html",
         "Néovolt Grid+ — Tableau de bord DIRECTION FINANCIÈRE")

    # ===================== 3. RELATION CLIENT =============================
    import unicodedata
    def sa(s): return "".join(c for c in unicodedata.normalize("NFD", str(s).lower())
                              if unicodedata.category(c) != "Mn")
    rec["txt"] = rec["texte"].map(sa)
    themes = {"facturation":"facture|prelevement|montant|rembours|tarif|regularisation",
              "coupure/panne":"coupure|panne|interruption|courant",
              "compteur":"compteur|releve|index|communicant",
              "donnees/RGPD":"rgpd|donnee|consentement|accord|privee",
              "relation client":"technicien|accueil|conseiller|attente|rappel|joindre",
              "raccordement":"raccordement|branchement|mise en service|delai"}
    rows = []
    for th, pat in themes.items():
        m = rec["txt"].str.contains(pat, regex=True)
        rows.append({"theme":th, "nb":int(m.sum()), "satisfaction":rec[m]["satisfaction"].mean()})
    th_df = pd.DataFrame(rows).sort_values("nb")
    canal = rec.groupby("canal")["satisfaction"].mean()
    dist = rec["satisfaction"].value_counts().sort_index()
    fig = make_subplots(rows=2, cols=2,
        subplot_titles=("Réclamations par thème (nb)",
                        "Satisfaction moyenne par thème (/5)",
                        "Satisfaction par canal (/5)",
                        "Distribution des notes de satisfaction"))
    fig.add_trace(go.Bar(x=th_df["nb"], y=th_df["theme"], orientation="h",
                         marker_color=ORANGE, name="nb"), 1, 1)
    cols = [ROUGE if v < rec["satisfaction"].mean() else VERT for v in th_df["satisfaction"]]
    fig.add_trace(go.Bar(x=th_df["satisfaction"], y=th_df["theme"], orientation="h",
                         marker_color=cols, name="satisf"), 1, 2)
    fig.add_trace(go.Bar(x=canal.index, y=canal.values, marker_color=BLEU, name="canal"), 2, 1)
    fig.add_trace(go.Bar(x=dist.index.astype(str), y=dist.values, marker_color=BLEU,
                         name="notes"), 2, 2)
    save(fig, "3_dashboard_relation_client.html",
         "Néovolt Grid+ — Tableau de bord RELATION CLIENT")

    print(f"\n>> 3 dashboards HTML dans : {DASH}")
    print("   Ouvre-les dans un navigateur (autonomes, fonctionnent hors ligne).")

if __name__ == "__main__":
    main()
