"""
Néovolt Grid+ — Exploration et diagnostic qualité des données (Jour 1).

Objectif : produire un état des lieux factuel et chiffré des 10 jeux de données
fournis, pour alimenter (1) la note de cadrage, (2) la note qualité du Data Analyst,
(3) le chiffrage ROI du Chef de projet, (4) le périmètre sécurité du volet Cyber.

Usage :
    python scripts/01_exploration_qualite.py
Le rapport est affiché en console ET écrit dans docs/diagnostic-qualite-donnees.md
"""
from __future__ import annotations
import os
import sys
import io
import pandas as pd
import numpy as np

# --- Localisation des données (configurable) ---------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
# Données fournies par l'examen, à côté du projet
DEFAULT_DATA = os.path.normpath(os.path.join(PROJ, "..", "donnees"))
DATA_DIR = os.environ.get("NEOVOLT_DATA", DEFAULT_DATA)

OUT_MD = os.path.join(PROJ, "docs", "diagnostic-qualite-donnees.md")

FILES = [
    "clients.csv", "compteurs.csv", "releves_consommation.csv",
    "releves_horaires_echantillon.csv", "meteo.csv", "incidents_reseau.csv",
    "reclamations.csv", "journaux_securite.csv", "actifs_si.csv",
    "cas_fraude_confirmes.csv",
]

# Capture la sortie pour double affichage (console + markdown)
buf = io.StringIO()
def out(*args):
    line = " ".join(str(a) for a in args)
    print(line)
    buf.write(line + "\n")

def load(name: str) -> pd.DataFrame:
    return pd.read_csv(os.path.join(DATA_DIR, name), encoding="utf-8")

def section(title: str):
    out("\n" + "=" * 78)
    out(title)
    out("=" * 78)

def quality_block(df: pd.DataFrame, name: str):
    out(f"\n### {name}")
    out(f"- Lignes : {len(df):,} | Colonnes : {len(df.columns)}")
    out(f"- Colonnes : {list(df.columns)}")
    # Doublons
    dup = df.duplicated().sum()
    out(f"- Lignes dupliquées (toutes colonnes) : {dup}")
    # Manquants
    miss = df.isna().sum()
    miss = miss[miss > 0]
    if len(miss):
        for c, n in miss.items():
            out(f"  - manquants `{c}` : {n} ({n/len(df):.1%})")
    else:
        out("  - aucun manquant détecté (sur valeurs NaN ; attention aux vides/0 implicites)")

def main():
    out("# Diagnostic qualité des données — Néovolt Grid+")
    out(f"_Source : `{DATA_DIR}`_\n")
    if not os.path.isdir(DATA_DIR):
        out(f"!! Dossier de données introuvable : {DATA_DIR}")
        out("   Définis NEOVOLT_DATA=<chemin> ou place les CSV dans ../donnees")
        sys.exit(1)

    # 1) Tour d'horizon qualité de chaque fichier
    section("1. TOUR D'HORIZON QUALITÉ (tous fichiers)")
    dfs = {}
    for f in FILES:
        try:
            dfs[f] = load(f)
            quality_block(dfs[f], f)
        except Exception as e:
            out(f"\n### {f}\n- ERREUR de lecture : {e}")

    # 2) Focus relevés de consommation (coeur du projet)
    section("2. FOCUS — releves_consommation.csv")
    rc = dfs.get("releves_consommation.csv")
    if rc is not None:
        rc["date"] = pd.to_datetime(rc["date"], errors="coerce")
        out(f"- Période : {rc['date'].min().date()} -> {rc['date'].max().date()}")
        out(f"- Nb PDL distincts : {rc['id_pdl'].nunique()}")
        out(f"- Nb zones : {rc['zone'].nunique()} -> {sorted(rc['zone'].dropna().unique())}")
        c = rc["consommation_kwh"]
        out(f"- Conso kWh : min={c.min():.2f} | médiane={c.median():.2f} | "
            f"moy={c.mean():.2f} | max={c.max():.2f}")
        out(f"- Valeurs négatives : {(c < 0).sum()} | nulles (==0) : {(c == 0).sum()} | "
            f"manquantes : {c.isna().sum()}")
        # Aberrants par méthode IQR
        q1, q3 = c.quantile(0.25), c.quantile(0.75)
        iqr = q3 - q1
        haut = q3 + 3 * iqr
        out(f"- Seuil aberrant (Q3 + 3*IQR) = {haut:.1f} kWh/j -> "
            f"{(c > haut).sum()} relevés au-dessus ({(c>haut).mean():.2%})")
        # Doublons (pdl, date)
        d2 = rc.duplicated(subset=["id_pdl", "date"]).sum()
        out(f"- Doublons (id_pdl, date) : {d2}")
        # Complétude temporelle : jours attendus vs présents (échantillon)
        jours = (rc["date"].max() - rc["date"].min()).days + 1
        attendus = jours * rc["id_pdl"].nunique()
        out(f"- Complétude : {len(rc):,} relevés / {attendus:,} attendus "
            f"({len(rc)/attendus:.1%}) sur {jours} jours")

    # 3) Référentiel compteurs / clients
    section("3. RÉFÉRENTIEL compteurs.csv & clients.csv")
    cp = dfs.get("compteurs.csv")
    if cp is not None:
        out("- Répartition type_compteur :")
        for k, v in cp["type_compteur"].value_counts().items():
            out(f"    {k}: {v} ({v/len(cp):.1%})")
        out("- Répartition statut :")
        for k, v in cp["statut"].value_counts().items():
            out(f"    {k}: {v}")
        out("- Répartition type_client :")
        for k, v in cp["type_client"].value_counts().items():
            out(f"    {k}: {v}")
    cl = dfs.get("clients.csv")
    if cl is not None:
        out("- Répartition segment client :")
        for k, v in cl["segment"].value_counts().items():
            out(f"    {k}: {v}")

    # 4) Fraude (labels) — base du ROI
    section("4. FRAUDE — cas_fraude_confirmes.csv (vérité terrain)")
    fr = dfs.get("cas_fraude_confirmes.csv")
    if fr is not None and cp is not None:
        out(f"- Nb fraudes confirmées : {len(fr)}")
        out("- Types de fraude :")
        for k, v in fr["type_fraude"].value_counts().items():
            out(f"    {k}: {v}")
        out("- Statuts :")
        for k, v in fr["statut"].value_counts().items():
            out(f"    {k}: {v}")
        taux = len(fr) / cp["id_pdl"].nunique()
        out(f"- Taux de fraude observé (échantillon) : {len(fr)}/{cp['id_pdl'].nunique()} "
            f"= {taux:.2%}")

    # 5) Réclamations (NLP)
    section("5. RÉCLAMATIONS — reclamations.csv")
    re = dfs.get("reclamations.csv")
    if re is not None:
        out(f"- Nb réclamations : {len(re)}")
        out("- Canaux :")
        for k, v in re["canal"].value_counts().items():
            out(f"    {k}: {v}")
        out("- Satisfaction (1-5) :")
        for k, v in re["satisfaction"].value_counts().sort_index().items():
            out(f"    note {k}: {v}")
        # mots-clés sensibles
        txt = re["texte"].str.lower()
        for kw in ["rgpd", "fraude", "donnee", "consentement", "panne", "coupure"]:
            out(f"  - réclamations contenant '{kw}' : {txt.str.contains(kw, na=False).sum()}")

    # 6) Incidents réseau (coût/ROI)
    section("6. INCIDENTS RÉSEAU — incidents_reseau.csv")
    inc = dfs.get("incidents_reseau.csv")
    if inc is not None:
        out(f"- Nb incidents : {len(inc)}")
        out("- Types :")
        for k, v in inc["type"].value_counts().items():
            out(f"    {k}: {v}")
        out(f"- Durée (min) : médiane={inc['duree_minutes'].median():.0f} | "
            f"max={inc['duree_minutes'].max():.0f}")
        out(f"- Total PDL impactés (cumul) : {inc['nb_pdl_impactes'].sum():,}")
        out("- Causes :")
        for k, v in inc["cause"].value_counts().items():
            out(f"    {k}: {v}")

    # 7) Journaux sécurité (volet Cyber / SIEM)
    section("7. JOURNAUX SÉCURITÉ — journaux_securite.csv")
    js = dfs.get("journaux_securite.csv")
    if js is not None:
        js["horodatage"] = pd.to_datetime(js["horodatage"], errors="coerce")
        out(f"- Période : {js['horodatage'].min()} -> {js['horodatage'].max()}")
        out(f"- Nb événements : {len(js):,}")
        out(f"- Utilisateurs distincts : {js['utilisateur'].nunique()} | "
            f"IP sources distinctes : {js['source_ip'].nunique()}")
        out("- Résultats :")
        for k, v in js["resultat"].value_counts().items():
            out(f"    {k}: {v} ({v/len(js):.1%})")
        out("- Types d'événements (top) :")
        for k, v in js["type_evenement"].value_counts().head(12).items():
            out(f"    {k}: {v}")
        # Signaux d'attaque : échecs de connexion par IP
        if "echec" in " ".join(js["resultat"].dropna().unique()).lower():
            ech = js[js["resultat"].str.contains("echec", case=False, na=False)]
            out(f"- Événements en échec : {len(ech):,}")
            top_ip = ech["source_ip"].value_counts().head(5)
            out("  - Top IP sources d'échecs (suspicion brute force) :")
            for k, v in top_ip.items():
                out(f"      {k}: {v} échecs")

    # 8) Actifs SI (cartographie risque)
    section("8. ACTIFS SI — actifs_si.csv")
    ac = dfs.get("actifs_si.csv")
    if ac is not None:
        out(f"- Nb actifs : {len(ac)}")
        out("- Par criticité :")
        for k, v in ac["criticite"].value_counts().items():
            out(f"    {k}: {v}")
        out("- Par exposition :")
        for k, v in ac["exposition"].value_counts().items():
            out(f"    {k}: {v}")
        sens = ac[ac["donnees_sensibles"].astype(str).str.lower() == "oui"]
        out(f"- Actifs avec données sensibles : {len(sens)} -> "
            f"{list(sens['id_actif'])}")

    # Écriture du rapport markdown
    os.makedirs(os.path.dirname(OUT_MD), exist_ok=True)
    with open(OUT_MD, "w", encoding="utf-8") as fh:
        fh.write(buf.getvalue())
    out(f"\n>> Rapport écrit dans : {OUT_MD}")

if __name__ == "__main__":
    main()
