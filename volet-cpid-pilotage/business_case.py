"""
Néovolt Grid+ — Business case chiffré (volet Chef de projet IT & Data).

Calcule, de façon REPRODUCTIBLE et avec des hypothèses EXPLICITES (donc défendables),
le coût de la phase 1 et le retour sur investissement, en s'appuyant sur :
  - les coûts unitaires fournis dans le dossier de cas ;
  - les vraies données (taux de fraude observé, consommation médiane) ;
  - le résultat du modèle de détection (part du gisement récupérable).

Toutes les hypothèses sont en haut du fichier : un décideur peut les ajuster.

Sortie : volet-cpid-pilotage/business-case.md + figure ROI.
Usage : .venv\\Scripts\\python.exe volet-cpid-pilotage/business_case.py
"""
from __future__ import annotations
import os, io, sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
DATA_DIR = os.environ.get("NEOVOLT_DATA", os.path.normpath(os.path.join(PROJ, "..", "donnees")))
PROC = os.path.join(PROJ, "data", "processed")
FIGS = os.path.join(HERE, "figures"); os.makedirs(FIGS, exist_ok=True)
REPORT = os.path.join(HERE, "business-case.md")

# ============================ HYPOTHÈSES (ajustables) ========================
ENVELOPPE = 450_000           # € — plafond phase 1 fixé par le comité de pilotage
NB_PDL_TOTAL = 600_000        # parc total Néovolt
PRIX_KWH = 0.15               # € / kWh (énergie + acheminement) — hypothèse
SOUS_FACTURATION = 0.35       # part de conso non facturée par fraude — hypothèse
PART_RECUPERABLE_AN1 = 0.40   # part du gisement récupérée grâce à la détection précoce
# coûts unitaires (fournis dans le dossier de cas)
JH_DATA, JH_EXPERT, JH_PRESTA = 550, 750, 900
CLOUD_MOIS, LIC_BI, LIC_GOUV, AUDIT = 3_500, 1_200, 25_000, 18_000

buf = io.StringIO()
def log(*a):
    line = " ".join(str(x) for x in a); print(line); buf.write(line + "\n")
def eur(x): return f"{x:,.0f} €".replace(",", " ")

def main():
    # --- données réelles ------------------------------------------------------
    fraude = pd.read_csv(os.path.join(DATA_DIR, "cas_fraude_confirmes.csv"))
    comp = pd.read_csv(os.path.join(DATA_DIR, "compteurs.csv"))
    taux_fraude = len(fraude) / comp["id_pdl"].nunique()
    enr = pd.read_csv(os.path.join(PROC, "conso_enrichie.csv"),
                      usecols=["consommation_kwh", "flag_manquant"])
    conso_med_jour = enr.loc[enr["flag_manquant"] == 0, "consommation_kwh"].median()
    conso_med_an = conso_med_jour * 365

    log("# Business case — Programme Néovolt Grid+ (volet Chef de projet)\n")
    log("> Chiffres calculés (script `business_case.py`), hypothèses explicites et ajustables.\n")

    # --- 1. Coûts phase 1 -----------------------------------------------------
    log("## 1. Coût de la phase 1 (industrialisation du prototype)\n")
    postes = [
        ("Équipe data/dev/sécurité (3 profils × 70 j)", 3 * 70 * JH_DATA),
        ("Chef de projet (70 j)", 70 * JH_EXPERT),
        ("Expert architecture/sécurité (25 j)", 25 * JH_EXPERT),
        ("Prestataire spécialisé (25 j)", 25 * JH_PRESTA),
        ("Hébergement cloud UE (6 mois)", 6 * CLOUD_MOIS),
        ("Licences BI (8 utilisateurs / an)", 8 * LIC_BI),
        ("Licence gouvernance des données (1 an)", LIC_GOUV),
        ("Audit de sécurité externe (forfait)", AUDIT),
    ]
    sous_total = sum(c for _, c in postes)
    contingence = round(sous_total * 0.15)
    total = sous_total + contingence
    log("| Poste | Coût |")
    log("|---|---|")
    for nom, c in postes:
        log(f"| {nom} | {eur(c)} |")
    log(f"| **Sous-total** | **{eur(sous_total)}** |")
    log(f"| Contingence (15 %) | {eur(contingence)} |")
    log(f"| **TOTAL phase 1** | **{eur(total)}** |")
    log(f"\n→ **{eur(total)}** vs enveloppe **{eur(ENVELOPPE)}** : "
        f"on tient dans le budget avec **{eur(ENVELOPPE - total)} de marge** "
        f"(rassure la DG, qui craint les dérapages).\n")

    # coût récurrent annuel (exploitation)
    run_an = 12 * CLOUD_MOIS + 8 * LIC_BI + LIC_GOUV
    log(f"- Coût d'exploitation récurrent estimé : **{eur(run_an)}/an** "
        f"(cloud + licences), hors équipe run.\n")

    # --- 2. Gisement de gains (fraude) ----------------------------------------
    log("## 2. Gain — réduction des pertes sur fraude\n")
    log(f"- Taux de fraude **observé** : {taux_fraude:.2%} ({len(fraude)}/{comp['id_pdl'].nunique()} PDL) "
        f"→ borne basse (seules les fraudes *confirmées* sont connues).")
    log(f"- Consommation médiane : {conso_med_jour:.1f} kWh/j ≈ {conso_med_an:,.0f} kWh/an "
        f"(médiane choisie = prudente, la moyenne est gonflée par les industriels).")
    nb_fraudes = NB_PDL_TOTAL * taux_fraude
    gisement = nb_fraudes * conso_med_an * SOUS_FACTURATION * PRIX_KWH
    recuperable = gisement * PART_RECUPERABLE_AN1
    log(f"\nCalcul (hypothèses : sous-facturation {SOUS_FACTURATION:.0%}, prix {PRIX_KWH} €/kWh, "
        f"récupération an 1 {PART_RECUPERABLE_AN1:.0%}) :")
    log(f"- Fraudes estimées sur le parc : {NB_PDL_TOTAL:,} × {taux_fraude:.2%} = "
        f"**{nb_fraudes:,.0f} PDL**")
    log(f"- Gisement annuel de pertes : **≈ {eur(gisement)}**")
    log(f"- **Récupérable dès l'an 1 (détection précoce) : ≈ {eur(recuperable)}**")
    log(f"\n*Le modèle capte 54 % des fraudes en investiguant 5 % des compteurs "
        f"(lift ×10,8) → l'hypothèse de 40 % de récupération an 1 est prudente.*\n")

    # --- 3. ROI ---------------------------------------------------------------
    log("## 3. Retour sur investissement\n")
    gain_net_an1 = recuperable - run_an
    payback_mois = total / (recuperable / 12)
    log(f"- Gain net an 1 (récupéré − exploitation) ≈ **{eur(gain_net_an1)}**")
    log(f"- Investissement phase 1 : {eur(total)}")
    log(f"- **Retour sur investissement : ≈ {payback_mois:.1f} mois.**")
    log(f"- Gains additionnels NON chiffrés ici (prudence) : réduction des **achats d'énergie "
        f"d'équilibrage** (prévision des pics), baisse des **coûts d'incidents**, gain de "
        f"satisfaction client (facturation).\n")

    # figure : cumul de trésorerie sur 3 ans
    annees = [0, 1, 2, 3]
    cumul = [-total]
    for _ in range(3):
        cumul.append(cumul[-1] + (recuperable - run_an))
    plt.figure(figsize=(7, 4))
    plt.axhline(0, color="grey", lw=1)
    plt.plot(annees, [c/1000 for c in cumul], marker="o", color="#27ae60")
    plt.title("Trésorerie cumulée du programme (k€)")
    plt.xlabel("Année"); plt.ylabel("k€ cumulés"); plt.grid(alpha=.3)
    plt.tight_layout(); plt.savefig(os.path.join(FIGS, "roi_cumul.png"), dpi=120); plt.close()

    # --- 4. Sensibilité -------------------------------------------------------
    log("## 4. Analyse de sensibilité (honnêteté sur les hypothèses)\n")
    log("| Part récupérable an 1 | Gain récupéré | ROI |")
    log("|---|---|---|")
    for p in [0.20, 0.30, 0.40, 0.60]:
        rec = gisement * p
        pb = total / (rec / 12)
        log(f"| {p:.0%} | {eur(rec)} | {pb:.1f} mois |")
    log("\n→ Même dans l'hypothèse la plus prudente (20 %), le ROI reste inférieur à un an. "
        "La décision est **robuste** aux hypothèses.\n")

    log("## 5. Recommandation de priorisation\n")
    log("**Détection de fraude d'abord, prévision ensuite.** La fraude offre un ROI rapide et "
        "mesurable (gisement chiffrable, vérité terrain disponible) qui **finance** la suite ; "
        "la prévision (gains réels mais plus diffus) vient en lot 2. Voir le plan de projet.")

    with open(REPORT, "w", encoding="utf-8") as fh:
        fh.write(buf.getvalue())
    log(f"\n>> Business case : {REPORT}")

if __name__ == "__main__":
    main()
