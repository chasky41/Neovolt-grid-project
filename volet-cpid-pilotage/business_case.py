"""
Néovolt Grid+ — Business case chiffré (volet Chef de projet IT & Data).

Calcule de manière reproductible le budget programme, les gains annuels
et le retour sur investissement du projet Néovolt Grid+.

Le business case est aligné avec la priorisation retenue :
1. Socle data et qualité des données
2. Prévision de consommation
3. Tableaux de bord de pilotage
4. Détection d'anomalies / fraude en évolution future

Sorties :
- volet-cpid-pilotage/business-case.md
- volet-cpid-pilotage/figures/roi_cumul.png

Usage :
.venv\\Scripts\\python.exe volet-cpid-pilotage/business_case.py
"""

from __future__ import annotations

import os
import io
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


HERE = os.path.dirname(os.path.abspath(__file__))
FIGS = os.path.join(HERE, "figures")
os.makedirs(FIGS, exist_ok=True)

REPORT = os.path.join(HERE, "business-case.md")


# ============================ HYPOTHÈSES =====================================

BUDGET_INITIAL = 360_000
COUT_ANNUEL_FONCTIONNEMENT = 75_000

GAINS_ANNUELS = {
    "Réduction des pertes et fraudes": 135_000,
    "Optimisation des interventions terrain": 36_000,
    "Gain de temps service client & exploitation": 45_000,
    "Amélioration de la planification réseau": 50_000,
    "Réduction du risque opérationnel": 25_000,
}

POSTES_COUTS = {
    "Cadrage projet, ateliers métiers et pilotage": 30_000,
    "Data engineering : collecte, nettoyage, pipelines": 85_000,
    "Data science : modèle de prévision et analyse": 70_000,
    "Tableaux de bord BI et data storytelling": 35_000,
    "Infrastructure cloud, stockage et sécurité": 40_000,
    "Gouvernance des données et qualité": 25_000,
    "Conduite du changement, formation et documentation": 25_000,
    "Tests, recette et amélioration continue": 20_000,
    "Marge de sécurité projet": 30_000,
}


buf = io.StringIO()


def log(*args):
    line = " ".join(str(x) for x in args)
    print(line)
    buf.write(line + "\n")


def eur(value):
    return f"{value:,.0f} €".replace(",", " ")


def main():
    gains_bruts = sum(GAINS_ANNUELS.values())
    gain_net_annuel = gains_bruts - COUT_ANNUEL_FONCTIONNEMENT
    roi_annees = BUDGET_INITIAL / gain_net_annuel
    roi_mois = roi_annees * 12

    log("# Business case — Programme Néovolt Grid+\n")
    log("> Business case aligné avec le volet Chef de Projet IT & Data.\n")

    log("## 1. Coût estimé du programme\n")
    log("| Poste | Coût estimé |")
    log("|---|---:|")

    for poste, cout in POSTES_COUTS.items():
        log(f"| {poste} | {eur(cout)} |")

    log(f"| **Budget initial estimé** | **{eur(BUDGET_INITIAL)}** |")
    log(f"\nCoût annuel de fonctionnement estimé : **{eur(COUT_ANNUEL_FONCTIONNEMENT)}**.\n")

    log("## 2. Bénéfices annuels attendus\n")
    log("| Source de gain | Gain annuel estimé |")
    log("|---|---:|")

    for source, gain in GAINS_ANNUELS.items():
        log(f"| {source} | {eur(gain)} |")

    log(f"| **Total des gains annuels estimés** | **{eur(gains_bruts)}** |")
    log(f"| Coût annuel de fonctionnement | - {eur(COUT_ANNUEL_FONCTIONNEMENT)} |")
    log(f"| **Gain net annuel estimé** | **{eur(gain_net_annuel)}** |")

    log("\n## 3. Retour sur investissement\n")
    log(f"- Budget initial : **{eur(BUDGET_INITIAL)}**")
    log(f"- Gain net annuel : **{eur(gain_net_annuel)}**")
    log(f"- ROI estimé : **{roi_mois:.1f} mois**, soit environ **18 à 24 mois**.\n")

    log("## 4. Priorisation recommandée\n")
    log(
        "La priorité est donnée au socle data et à la prévision de consommation, "
        "car ces éléments apportent une valeur opérationnelle rapide et présentent "
        "un risque métier plus maîtrisé que la détection de fraude."
    )
    log(
        "La détection d'anomalies et de fraudes est conservée comme une évolution future, "
        "une fois les données fiabilisées et les premiers usages adoptés par les métiers.\n"
    )

    log("## 5. Projection sur 3 ans\n")
    gains_3_ans = gains_bruts * 3
    couts_run_3_ans = COUT_ANNUEL_FONCTIONNEMENT * 3
    gain_net_3_ans = gains_3_ans - BUDGET_INITIAL - couts_run_3_ans

    log(f"- Gains bruts sur 3 ans : **{eur(gains_3_ans)}**")
    log(f"- Coût initial du programme : **- {eur(BUDGET_INITIAL)}**")
    log(f"- Coûts de fonctionnement sur 3 ans : **- {eur(couts_run_3_ans)}**")
    log(f"- Gain net estimé sur 3 ans : **{eur(gain_net_3_ans)}**")

    # Figure ROI cumulée
    annees = [0, 1, 2, 3]
    cumul = [-BUDGET_INITIAL]

    for _ in range(3):
        cumul.append(cumul[-1] + gain_net_annuel)

    plt.figure(figsize=(7, 4))
    plt.axhline(0, color="grey", lw=1)
    plt.plot(annees, [c / 1000 for c in cumul], marker="o", color="#27ae60")
    plt.title("Trésorerie cumulée du programme Néovolt Grid+")
    plt.xlabel("Année")
    plt.ylabel("k€ cumulés")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(FIGS, "roi_cumul.png"), dpi=120)
    plt.close()

    with open(REPORT, "w", encoding="utf-8") as file:
        file.write(buf.getvalue())

    log(f"\n>> Business case généré : {REPORT}")


if __name__ == "__main__":
    main()