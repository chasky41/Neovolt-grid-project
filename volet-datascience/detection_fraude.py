"""
Néovolt Grid+ — Détection d'anomalies / fraude sur les compteurs (volet Data Scientist).

Problème : repérer tôt les points de livraison (PDL) suspects (sous-comptage,
branchement illicite, compteur trafiqué) parmi 700 PDL, avec seulement 24 fraudes
confirmées comme vérité terrain -> on traite cela comme de la DÉTECTION D'ANOMALIES
NON SUPERVISÉE (Isolation Forest), pas de la classification supervisée (trop peu de
labels). Les 24 cas servent à ÉVALUER, pas à entraîner.

Démarche :
  1. Feature engineering : un profil de consommation par PDL (24 mois de relevés propres).
  2. Score d'anomalie : Isolation Forest sur les features standardisées.
  3. Règles métier explicables (sous-comptage = chute durable ; ratio conso/puissance bas...).
  4. Score combiné -> liste priorisée de PDL à investiguer.
  5. Évaluation honnête sur les 24 fraudes : précision/rappel @top-N, average precision, lift.
  6. Éthique : score = AIDE à la décision, PAS verdict. Humain dans la boucle (cf. rapport).

Sorties :
  - volet-datascience/suspects_priorises.csv   (PDL triés + raisons explicables)
  - volet-datascience/models/isolation_forest.joblib + features.csv  (MLOps)
  - volet-datascience/figures/evaluation_fraude.png
  - docs/rapport-detection-fraude.md

Usage : .venv\\Scripts\\python.exe volet-datascience/detection_fraude.py
"""
from __future__ import annotations
import os
import io
import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")   # éviter les crashs cp1252 sur la console Windows
except Exception:
    pass
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import average_precision_score
import joblib

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
DATA_DIR = os.environ.get("NEOVOLT_DATA", os.path.normpath(os.path.join(PROJ, "..", "donnees")))
PROC = os.path.join(PROJ, "data", "processed")
MODELS = os.path.join(HERE, "models"); os.makedirs(MODELS, exist_ok=True)
FIGS = os.path.join(HERE, "figures"); os.makedirs(FIGS, exist_ok=True)
REPORT = os.path.join(PROJ, "docs", "rapport-detection-fraude.md")
RANDOM_STATE = 42

buf = io.StringIO()
def log(*a):
    line = " ".join(str(x) for x in a); print(line); buf.write(line + "\n")

def lin_slope(y):
    """Pente normalisée d'une tendance linéaire (robuste aux NaN)."""
    y = pd.Series(y).dropna().values
    if len(y) < 30 or np.nanmean(y) == 0:
        return 0.0
    x = np.arange(len(y))
    slope = np.polyfit(x, y, 1)[0]
    return slope / (np.mean(y) + 1e-9)   # pente relative (par jour)

def build_features(enr: pd.DataFrame) -> pd.DataFrame:
    log("## 1. Feature engineering (1 profil par PDL)\n")
    enr = enr.sort_values(["id_pdl", "date"])
    feats = []
    # moitié de période pour mesurer une chute durable (signature sous-comptage)
    date_med = enr["date"].quantile(0.5)
    for pdl, g in enr.groupby("id_pdl"):
        c = g["consommation_kwh"]
        c_valid = c.dropna()
        first = g[g["date"] < date_med]["consommation_kwh"].mean()
        last = g[g["date"] >= date_med]["consommation_kwh"].mean()
        # corrélation conso/température (un chauffage électrique décorrélé = suspect)
        sub = g[["consommation_kwh", "temp_moyenne_c"]].dropna()
        corr_temp = sub["consommation_kwh"].corr(sub["temp_moyenne_c"]) if len(sub) > 30 else 0.0
        puiss = g["puissance_souscrite_kva"].iloc[0]
        feats.append({
            "id_pdl": pdl,
            "type_client": g["type_client"].iloc[0],
            "segment": g["segment"].iloc[0],
            "conso_moy": c_valid.mean(),
            "conso_med": c_valid.median(),
            "conso_cv": c_valid.std() / (c_valid.mean() + 1e-9),
            "pct_zero": g["flag_zero"].mean(),
            "pct_manquant": g["flag_manquant"].mean(),
            "pct_aberrant": g["flag_aberrant"].mean(),
            "ratio_puissance": (c_valid.mean() / puiss) if puiss else np.nan,
            "corr_temp": corr_temp if pd.notna(corr_temp) else 0.0,
            "trend": lin_slope(c.values),
            "ratio_chute": (last / first) if (first and first > 0) else 1.0,
        })
    f = pd.DataFrame(feats)
    log(f"- {len(f)} PDL profilés, {f.shape[1]-3} variables explicatives")
    log(f"- Variables : conso_moy/med/cv, pct_zero/manquant/aberrant, ratio_puissance, "
        f"corr_temp, trend, ratio_chute (conso 2e moitié / 1re moitié)\n")
    return f

def main():
    log("# Rapport — Détection d'anomalies / fraude (volet Data Scientist)\n")
    enr_path = os.path.join(PROC, "conso_enrichie.csv")
    if not os.path.exists(enr_path):
        raise SystemExit("Lance d'abord scripts/02_nettoyage.py (conso_enrichie.csv manquant).")
    enr = pd.read_csv(enr_path, parse_dates=["date"],
                      usecols=["id_pdl", "date", "consommation_kwh", "flag_zero",
                               "flag_manquant", "flag_aberrant", "temp_moyenne_c",
                               "puissance_souscrite_kva", "type_client", "segment"])
    fraude = pd.read_csv(os.path.join(DATA_DIR, "cas_fraude_confirmes.csv"))
    fraude_pdl = set(fraude["id_pdl"])

    f = build_features(enr)
    # Consommation RELATIVE au groupe de pairs : un industriel se compare aux industriels.
    # -> évite de flaguer un PDL juste parce qu'il consomme beaucoup (magnitude != fraude).
    f["conso_moy_rel"] = f["conso_moy"] / f.groupby("type_client")["conso_moy"].transform("median")
    f["is_fraude"] = f["id_pdl"].isin(fraude_pdl).astype(int)
    base_rate = f["is_fraude"].mean()
    log(f"- Vérité terrain : {f['is_fraude'].sum()} fraudes / {len(f)} PDL "
        f"(taux de base {base_rate:.2%})\n")

    # ---- 2. Isolation Forest -------------------------------------------------
    log("## 2. Modèle — Isolation Forest (non supervisé)\n")
    # Features SCALE-INVARIANTES (signatures de comportement, pas de taille) :
    feat_cols = ["conso_moy_rel", "conso_cv", "pct_zero", "pct_manquant",
                 "pct_aberrant", "ratio_puissance", "corr_temp", "trend", "ratio_chute"]
    X = f[feat_cols].replace([np.inf, -np.inf], np.nan)
    X = X.fillna(X.median())
    Xs = StandardScaler().fit_transform(X)
    iso = IsolationForest(n_estimators=300, contamination=0.06,
                          random_state=RANDOM_STATE)
    iso.fit(Xs)
    # score d'anomalie : plus haut = plus suspect
    f["score_anomalie"] = -iso.decision_function(Xs)
    log("- IsolationForest(n_estimators=300, contamination=0.06, random_state=42)")
    log("- Score = -decision_function (normalisé plus bas), trié décroissant = priorité d'enquête\n")

    # ---- 3. Règles métier explicables ---------------------------------------
    log("## 3. Règles métier explicables (transparence de la décision)\n")
    def raisons(r):
        out = []
        if r["ratio_chute"] < 0.6:
            out.append(f"chute durable de conso (-{(1-r['ratio_chute'])*100:.0f}%)")
        if r["ratio_puissance"] < f["ratio_puissance"].quantile(0.05):
            out.append("conso très faible vs puissance souscrite")
        if r["pct_zero"] > 0.20:
            out.append(f"{r['pct_zero']*100:.0f}% de jours à zéro")
        if r["type_client"] != "industriel" and r["corr_temp"] > -0.05 and r["conso_moy"] > 5:
            out.append("conso décorrélée de la température")
        return "; ".join(out) if out else "profil atypique (modèle)"
    f["raisons"] = f.apply(raisons, axis=1)
    log("- Indicateurs : chute durable (sous-comptage), ratio conso/puissance, % jours à zéro,")
    log("  décorrélation à la température. Chaque suspect est accompagné de SA raison.\n")

    # ---- 4. Évaluation honnête ----------------------------------------------
    log("## 4. Évaluation sur les 24 fraudes confirmées\n")
    f = f.sort_values("score_anomalie", ascending=False).reset_index(drop=True)
    f["rang"] = np.arange(1, len(f) + 1)
    ap = average_precision_score(f["is_fraude"], f["score_anomalie"])
    log(f"- **Average Precision (PR-AUC) : {ap:.3f}** (vs {base_rate:.3f} en aléatoire)")
    log("")
    log("| Top-N investigués | Fraudes captées | Rappel | Précision | Lift vs aléatoire |")
    log("|---|---|---|---|---|")
    total_fraude = int(f["is_fraude"].sum())
    for n in [25, 35, 50, 70, 100]:
        top = f.head(n)
        capt = int(top["is_fraude"].sum())
        rappel = capt / total_fraude
        prec = capt / n
        lift = prec / base_rate
        log(f"| {n} ({n/len(f):.0%}) | {capt}/{total_fraude} | {rappel:.0%} | {prec:.0%} | ×{lift:.1f} |")
    log("")

    # Figure : capture cumulée des fraudes selon le nb de PDL investigués
    cum = f["is_fraude"].cumsum() / total_fraude
    plt.figure(figsize=(7, 4.5))
    plt.plot(f["rang"], cum * 100, label="Modèle (Isolation Forest)")
    plt.plot([0, len(f)], [0, 100], "--", color="grey", label="Aléatoire")
    plt.axvline(35, color="red", ls=":", lw=1, label="Budget enquête = 5% (35 PDL)")
    plt.xlabel("Nombre de PDL investigués (par ordre de suspicion)")
    plt.ylabel("% des fraudes connues captées")
    plt.title("Néovolt — Efficacité de la priorisation des enquêtes fraude")
    plt.legend(); plt.grid(alpha=.3); plt.tight_layout()
    fig_path = os.path.join(FIGS, "evaluation_fraude.png")
    plt.savefig(fig_path, dpi=120); plt.close()
    log(f"- Figure : `volet-datascience/figures/evaluation_fraude.png`\n")

    # ---- 5. Sorties / MLOps --------------------------------------------------
    cols_out = ["rang", "id_pdl", "type_client", "segment", "score_anomalie",
                "is_fraude", "raisons", "conso_moy", "ratio_puissance",
                "ratio_chute", "pct_zero", "corr_temp"]
    out = f[cols_out].copy()
    out["score_anomalie"] = out["score_anomalie"].round(4)
    out.to_csv(os.path.join(HERE, "suspects_priorises.csv"), index=False)
    joblib.dump(iso, os.path.join(MODELS, "isolation_forest.joblib"))
    f[["id_pdl"] + feat_cols + ["is_fraude"]].to_csv(
        os.path.join(MODELS, "features.csv"), index=False)
    log("## 5. Artefacts produits (MLOps)\n")
    log("- `suspects_priorises.csv` : 700 PDL triés par suspicion + raison explicable")
    log("- `models/isolation_forest.joblib` : modèle versionné")
    log("- `models/features.csv` : table de features (reproductibilité de l'expérience)")

    log("\n## 6. Top 10 des PDL à investiguer en priorité\n")
    log("| Rang | PDL | Type | Score | Connu fraude | Raison |")
    log("|---|---|---|---|---|---|")
    for _, r in out.head(10).iterrows():
        log(f"| {r['rang']} | {r['id_pdl']} | {r['type_client']} | {r['score_anomalie']} | "
            f"{'OUI' if r['is_fraude'] else '—'} | {r['raisons']} |")

    log("\n## 7. Limites & éthique (à défendre)\n")
    log("- Le score est une **aide à la priorisation**, pas un verdict : décision finale humaine "
        "(exigence RGPD sur la décision automatisée).")
    log("- Risque de **faux positifs** : un logement vacant ou un changement de vie (télétravail, "
        "déménagement) ressemble à une chute de conso. Coût d'un faux positif (client accusé à tort) "
        "≠ coût d'un faux négatif (fraude manquée).")
    log("- **Biais** : vérifier que le modèle ne sur-cible pas un segment (ex. petits foyers). "
        "Une AIPD est requise avant tout usage réel.")
    log("- 24 labels seulement : l'évaluation est indicative, pas une garantie de performance en réel.")

    with open(REPORT, "w", encoding="utf-8") as fh:
        fh.write(buf.getvalue())
    log(f"\n>> Rapport : {REPORT}")

if __name__ == "__main__":
    main()
