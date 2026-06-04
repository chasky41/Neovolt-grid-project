"""
Néovolt Grid+ — Tableau de bord de pilotage projet (volet Chef de projet).

Vue décideur : avancement des lots, consommation budgétaire, matrice des risques,
indicateurs de valeur. Sortie HTML autonome (Plotly).

Usage :
.venv\\Scripts\\python.exe volet-cpid-pilotage/dashboard_pilotage.py
"""

from __future__ import annotations

import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import plotly.graph_objects as go
from plotly.subplots import make_subplots


HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "dashboard_pilotage.html")


# --- État du prototype (sprint) : % d'avancement par lot ---------------------
lots = [
    "L0 Cadrage",
    "L1 Plateforme data",
    "L2 Prévision",
    "L3 Dashboards",
    "L4 Sécurité",
    "L5 Anomalies/fraude",
    "L6 Déploiement",
]

avancement = [
    100,  # cadrage réalisé
    80,   # socle data partiellement réalisé
    100,  # prévision réalisée dans l'US6
    60,   # dashboards en cours / volet DA
    70,   # sécurité en cours
    20,   # anomalies/fraude uniquement en perspective
    40,   # préparation du déploiement / MLOps
]


# --- Budget ------------------------------------------------------------------
# Cohérent avec le business case CPID : budget programme estimé à 360 k€
ENVELOPPE = 360_000
ESTIME = 325_000


# --- Risques (probabilité 1-5, gravité 1-5) ----------------------------------
risques = [
    ("R1 Qualité données", 4, 4),
    ("R2 Modèle prévision peu fiable", 3, 4),
    ("R3 Rejet utilisateurs", 3, 4),
    ("R4 Incident sécurité", 3, 5),
    ("R5 Budget", 2, 3),
    ("R6 Industrialisation limitée", 3, 3),
]


def main():
    fig = make_subplots(
        rows=2,
        cols=2,
        specs=[
            [{"type": "bar"}, {"type": "indicator"}],
            [{"type": "scatter"}, {"type": "indicator"}],
        ],
        subplot_titles=(
            "Avancement des lots (%)",
            "Budget programme (€)",
            "Matrice des risques (probabilité × gravité)",
            "Valeur — performance du modèle",
        ),
    )

    colors = [
        "#27ae60" if a == 100 else "#e67e22" if a > 0 else "#bdc3c7"
        for a in avancement
    ]

    fig.add_trace(
        go.Bar(
            x=avancement,
            y=lots,
            orientation="h",
            marker_color=colors,
            text=[f"{a}%" for a in avancement],
            textposition="auto",
        ),
        1,
        1,
    )
    fig.update_xaxes(range=[0, 100], row=1, col=1)

    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=ESTIME,
            number={"prefix": "", "suffix": " €", "valueformat": ",.0f"},
            gauge={
                "axis": {"range": [0, ENVELOPPE]},
                "bar": {"color": "#27ae60"},
                "threshold": {
                    "line": {"color": "red", "width": 3},
                    "value": ENVELOPPE,
                },
            },
            title={"text": "Estimé vs budget 360 k€"},
        ),
        1,
        2,
    )

    fig.add_trace(
        go.Scatter(
            x=[r[1] for r in risques],
            y=[r[2] for r in risques],
            mode="markers+text",
            text=[r[0] for r in risques],
            textposition="top center",
            marker=dict(
                size=[r[1] * r[2] * 2 for r in risques],
                color=[r[1] * r[2] for r in risques],
                colorscale="YlOrRd",
                showscale=True,
                cmin=1,
                cmax=25,
            ),
        ),
        2,
        1,
    )

    fig.update_xaxes(title_text="Probabilité", range=[0, 6], row=2, col=1)
    fig.update_yaxes(title_text="Gravité", range=[0, 6], row=2, col=1)

    fig.add_trace(
        go.Indicator(
            mode="number+delta",
            value=8.64,
            number={"suffix": " %", "valueformat": ".2f"},
            delta={
                "reference": 10,
                "decreasing": {"color": "green"},
                "increasing": {"color": "red"},
                "valueformat": ".2f",
            },
            title={
                "text": "MAPE du modèle de prévision<br>objectif : < 10 %"
            },
        ),
        2,
        2,
    )

    fig.update_layout(
        title_text="Néovolt Grid+ — Tableau de bord de pilotage projet",
        title_font_size=20,
        template="plotly_white",
        height=780,
        showlegend=False,
        margin=dict(t=90),
    )

    fig.write_html(OUT, include_plotlyjs=True, full_html=True)
    print(f">> Dashboard de pilotage : {OUT}")


if __name__ == "__main__":
    main()
