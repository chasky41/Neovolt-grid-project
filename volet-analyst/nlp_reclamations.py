"""
Néovolt Grid+ — Analyse de texte des réclamations (volet Data Analyst, NLP).

3000 réclamations en texte libre + note de satisfaction (1-5). Objectif : faire parler
le verbatim client — quels sujets dominent, lesquels font chuter la satisfaction — pour
la relation client et l'éthique (RGPD).

Approche (sans dépendance lourde : ni NLTK ni spaCy requis) :
  1. Normalisation du texte (minuscule, sans accents).
  2. Thèmes métier par mots-clés (interprétable, défendable).
  3. Thèmes data-driven : TF-IDF + KMeans (vérification croisée).
  4. Satisfaction par thème et par canal → priorités d'action.

Sorties : figures/*.png, dashboards/kpi_reclamations_*.csv, docs/analyse-reclamations.md
Usage : .venv\\Scripts\\python.exe volet-analyst/nlp_reclamations.py
"""
from __future__ import annotations
import os, io, sys, unicodedata
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
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

sns.set_theme(style="whitegrid")
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
DATA_DIR = os.environ.get("NEOVOLT_DATA", os.path.normpath(os.path.join(PROJ, "..", "donnees")))
FIGS = os.path.join(HERE, "figures"); os.makedirs(FIGS, exist_ok=True)
DASH = os.path.join(HERE, "dashboards"); os.makedirs(DASH, exist_ok=True)
REPORT = os.path.join(PROJ, "docs", "analyse-reclamations.md")
RANDOM_STATE = 42

# Stopwords français compacts (suffisant pour du verbatim court)
STOP = set("""au aux avec ce ces dans de des du elle en et eux il je la le les leur lui ma
mais me meme mes moi mon ne nos notre nous on ou par pas pour qu que qui sa se ses son sur
ta te tes toi ton tu un une vos votre vous c d j l a m n s t y est suis es sommes etes sont
ai as avons avez ont ete a fait faire tres plus tout toute tous bien cela ca donc car
alors aussi alors quand comme alors si non oui merci bonjour madame monsieur cordialement""".split())

THEMES = {
    "coupure/panne": ["coupure", "panne", "interruption", "noir", "delestage", "courant"],
    "facturation": ["facture", "facturation", "prelevement", "montant", "rembours", "tarif",
                    "estimation", "regularisation", "paiement"],
    "donnees/RGPD": ["rgpd", "donnee", "donnees", "consentement", "personnel", "privee", "accord"],
    "compteur": ["compteur", "releve", "index", "communicant", "linky"],
    "relation client": ["technicien", "accueil", "conseiller", "attente", "rappel", "joindre",
                        "interlocuteur", "reponse"],
    "raccordement": ["raccordement", "branchement", "mise en service", "delai", "intervention"],
}

def strip_accents(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn")

buf = io.StringIO()
def log(*a):
    line = " ".join(str(x) for x in a); print(line); buf.write(line + "\n")

def main():
    log("# Analyse des réclamations clients (NLP) — Néovolt Grid+ (volet Data Analyst)\n")
    df = pd.read_csv(os.path.join(DATA_DIR, "reclamations.csv"))
    df["txt"] = df["texte"].fillna("").map(lambda s: strip_accents(s.lower()))
    log(f"- {len(df):,} réclamations, satisfaction moyenne **{df['satisfaction'].mean():.2f}/5** "
        f"(médiane {df['satisfaction'].median():.0f}).")
    insat = (df['satisfaction'] <= 2).mean()
    log(f"- Part de clients insatisfaits (note ≤ 2) : **{insat:.0%}**.\n")

    # ---------- 1. Thèmes métier par mots-clés --------------------------------
    log("## 1. Thèmes dominants (catégorisation métier)\n")
    for theme, kws in THEMES.items():
        pattern = "|".join(kws)
        df[theme] = df["txt"].str.contains(pattern, regex=True).astype(int)
    theme_cols = list(THEMES.keys())
    freq = df[theme_cols].sum().sort_values(ascending=False)
    log("| Thème | Nb réclamations | Part | Satisfaction moyenne |")
    log("|---|---|---|---|")
    rows_sat = {}
    for theme in freq.index:
        sub = df[df[theme] == 1]
        sat = sub["satisfaction"].mean()
        rows_sat[theme] = sat
        log(f"| {theme} | {int(freq[theme])} | {freq[theme]/len(df):.0%} | {sat:.2f}/5 |")
    log("")
    # figure : fréquence des thèmes
    plt.figure(figsize=(8, 4))
    sns.barplot(x=freq.values, y=freq.index, color="#c45")
    plt.title("Fréquence des thèmes de réclamation"); plt.xlabel("Nb de réclamations")
    plt.tight_layout(); plt.savefig(os.path.join(FIGS, "06_themes_reclamations.png"), dpi=120); plt.close()
    # figure : satisfaction par thème
    sat_serie = pd.Series(rows_sat).sort_values()
    plt.figure(figsize=(8, 4))
    colors = ["#c0392b" if v < df["satisfaction"].mean() else "#27ae60" for v in sat_serie.values]
    sns.barplot(x=sat_serie.values, y=sat_serie.index, hue=sat_serie.index,
                palette=colors, legend=False)
    plt.axvline(df["satisfaction"].mean(), color="grey", ls="--", label="moyenne globale")
    plt.title("Satisfaction moyenne par thème (rouge = sous la moyenne)")
    plt.xlabel("Satisfaction /5"); plt.legend(); plt.tight_layout()
    plt.savefig(os.path.join(FIGS, "07_satisfaction_par_theme.png"), dpi=120); plt.close()

    worst = sat_serie.idxmin()
    log(f"- **Thème le plus pénalisant : « {worst} » ({sat_serie.min():.2f}/5)** → priorité relation client.")
    log(f"- Le thème « donnees/RGPD » concerne {int(freq.get('donnees/RGPD',0))} réclamations : "
        f"signal de conformité à ne pas négliger (lien volet éthique/DPO).\n")

    # ---------- 2. Thèmes data-driven (TF-IDF + KMeans) -----------------------
    log("## 2. Vérification data-driven (TF-IDF + KMeans, k=6)\n")
    vec = TfidfVectorizer(stop_words=list(STOP), max_features=400, min_df=5)
    X = vec.fit_transform(df["txt"])
    km = KMeans(n_clusters=6, random_state=RANDOM_STATE, n_init=10).fit(X)
    df["cluster_txt"] = km.labels_
    terms = np.array(vec.get_feature_names_out())
    centers = km.cluster_centers_
    log("Top mots-clés par cluster (thèmes émergents) :\n")
    for c in range(6):
        top = terms[centers[c].argsort()[::-1][:6]]
        sat_c = df[df["cluster_txt"] == c]["satisfaction"].mean()
        n_c = (df["cluster_txt"] == c).sum()
        log(f"- Cluster {c} ({n_c} récl., satisf {sat_c:.2f}/5) : {', '.join(top)}")
    log("")

    # ---------- 3. Satisfaction par canal -------------------------------------
    log("## 3. Satisfaction par canal\n")
    by_canal = df.groupby("canal")["satisfaction"].agg(["mean", "count"]).round(2)
    for canal, r in by_canal.iterrows():
        log(f"- {canal} : {r['mean']:.2f}/5 ({int(r['count'])} réclamations)")
    log("")

    # ---------- Exports --------------------------------------------------------
    freq.reset_index().rename(columns={"index": "theme", 0: "nb"}).to_csv(
        os.path.join(DASH, "kpi_reclamations_themes.csv"), index=False)
    pd.Series(rows_sat).reset_index().rename(
        columns={"index": "theme", 0: "satisfaction_moy"}).to_csv(
        os.path.join(DASH, "kpi_reclamations_satisfaction.csv"), index=False)

    log("## Recommandations (data storytelling)\n")
    log(f"1. **Agir en priorité sur « {worst} »** : c'est le thème le plus corrélé à "
        f"l'insatisfaction. Un plan d'action ciblé remonterait la satisfaction globale.")
    log("2. **Tracer les réclamations RGPD** comme un indicateur de conformité suivi par le DPO.")
    log("3. **Relier réclamations « coupure » et incidents réseau** (volet exploitation) pour "
        "vérifier que les zones les plus touchées correspondent aux incidents enregistrés.")
    log("\n## Figures produites\n")
    log("- `06_themes_reclamations.png`, `07_satisfaction_par_theme.png`")

    with open(REPORT, "w", encoding="utf-8") as fh:
        fh.write(buf.getvalue())
    log(f"\n>> Rapport : {REPORT}")

if __name__ == "__main__":
    main()
