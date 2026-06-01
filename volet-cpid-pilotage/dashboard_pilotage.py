"""
Néovolt Grid+ — Tableau de bord de pilotage projet (volet Chef de projet).
Vue décideur : avancement des lots, consommation budgétaire, matrice des risques,
indicateurs de valeur. Sortie HTML autonome (Plotly).

Usage : .venv\\Scripts\\python.exe volet-cpid-pilotage/dashboard_pilotage.py
"""
from __future__ import annotations
import os, sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import plotly.graph_objects as go
from plotly.subplots import make_subplots

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "dashboard_pilotage.html")

# --- État du prototype (sprint) : % d'avancement par lot ---------------------
lots = ["L0 Cadrage", "L1 Plateforme", "L2 Fraude", "L3 Dashboards",
        "L4 Sécurité", "L5 Prévision", "L6 Déploiement"]
avancement = [100, 100, 100, 100, 90, 0, 0]   # prototype : L5/L6 = phase ultérieure

# --- Budget ------------------------------------------------------------------
ENVELOPPE, ESTIME = 450_000, 325_278

# --- Risques (probabilité 1-5, gravité 1-5) ----------------------------------
risques = [("R1 Qualité données",4,4),("R2 Biais fraude",3,4),
           ("R3 Rejet utilisateurs",3,4),("R4 Incident sécu",3,5),
           ("R5 Budget",2,3),("R6 Lock-in",2,3)]

def main():
    fig = make_subplots(
        rows=2, cols=2,
        specs=[[{"type":"bar"},{"type":"indicator"}],
               [{"type":"scatter"},{"type":"indicator"}]],
        subplot_titles=("Avancement des lots (%)", "Budget phase 1 (€)",
                        "Matrice des risques (probabilité × gravité)",
                        "Valeur — retour sur investissement"))

    colors = ["#27ae60" if a==100 else "#e67e22" if a>0 else "#bdc3c7" for a in avancement]
    fig.add_trace(go.Bar(x=avancement, y=lots, orientation="h",
                         marker_color=colors, text=[f"{a}%" for a in avancement],
                         textposition="auto"), 1, 1)
    fig.update_xaxes(range=[0,100], row=1, col=1)

    fig.add_trace(go.Indicator(
        mode="gauge+number", value=ESTIME,
        number={"prefix":"", "suffix":" €", "valueformat":",.0f"},
        gauge={"axis":{"range":[0,ENVELOPPE]},
               "bar":{"color":"#27ae60"},
               "threshold":{"line":{"color":"red","width":3},"value":ENVELOPPE}},
        title={"text":"Estimé vs enveloppe 450 k€"}), 1, 2)

    fig.add_trace(go.Scatter(
        x=[r[1] for r in risques], y=[r[2] for r in risques], mode="markers+text",
        text=[r[0] for r in risques], textposition="top center",
        marker=dict(size=[r[1]*r[2]*2 for r in risques],
                    color=[r[1]*r[2] for r in risques], colorscale="YlOrRd",
                    showscale=True, cmin=1, cmax=25)), 2, 1)
    fig.update_xaxes(title_text="Probabilité", range=[0,6], row=2, col=1)
    fig.update_yaxes(title_text="Gravité", range=[0,6], row=2, col=1)

    fig.add_trace(go.Indicator(
        mode="number+delta", value=1.7,
        number={"suffix":" mois", "valueformat":".1f"},
        delta={"reference":12, "decreasing":{"color":"green"},
               "valueformat":".0f"},
        title={"text":"ROI (retour sur invest.)<br>gisement fraude ≈ 5,7 M€/an"}), 2, 2)

    fig.update_layout(title_text="Néovolt Grid+ — Tableau de bord de PILOTAGE PROJET",
                      title_font_size=20, template="plotly_white", height=780,
                      showlegend=False, margin=dict(t=90))
    fig.write_html(OUT, include_plotlyjs=True, full_html=True)
    print(f">> Dashboard de pilotage : {OUT}")

if __name__ == "__main__":
    main()
