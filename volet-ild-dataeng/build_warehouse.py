"""
Néovolt Grid+ — Construction de l'entrepôt de données (volet ILD / Data Eng).

Charge les données NETTOYÉES + les référentiels dans une base relationnelle unique,
qui sert de source unique de vérité à l'API et aux volets Analyst / Data Scientist.

Choix techniques (assumés) :
  - SQLite pour le PROTOTYPE : zéro installation, fichier unique, requêtable en SQL
    standard. En cible (industrialisation), la même logique vise PostgreSQL hébergé
    en UE (souveraineté) — le code SQLAlchemy/pandas est portable (réversibilité).
  - Schéma en étoile léger : une table de faits (consommation) + des dimensions
    (compteur, client, météo) + des tables métier (incidents, réclamations, fraude, actifs).

Pré-requis : avoir exécuté scripts/02_nettoyage.py (génère data/processed/releves_propres.csv).
Usage : .venv\\Scripts\\python.exe volet-ild-dataeng/build_warehouse.py
"""
from __future__ import annotations
import os
import sqlite3
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
DATA_DIR = os.environ.get("NEOVOLT_DATA", os.path.normpath(os.path.join(PROJ, "..", "donnees")))
PROC = os.path.join(PROJ, "data", "processed")
DB_PATH = os.path.join(PROC, "neovolt.db")

def main():
    clean = os.path.join(PROC, "releves_propres.csv")
    if not os.path.exists(clean):
        raise SystemExit("Lance d'abord scripts/02_nettoyage.py (releves_propres.csv manquant).")

    print(f">> Entrepôt cible : {DB_PATH}")
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)          # build idempotent
    con = sqlite3.connect(DB_PATH)

    # Table de faits : consommation nettoyée
    fact = pd.read_csv(clean, parse_dates=["date"])
    fact.to_sql("fact_consommation", con, index=False, if_exists="replace")

    # Dimensions & tables métier (référentiels bruts)
    tables = {
        "dim_compteur": "compteurs.csv",
        "dim_client": "clients.csv",
        "dim_meteo": "meteo.csv",
        "incidents_reseau": "incidents_reseau.csv",
        "reclamations": "reclamations.csv",
        "cas_fraude_confirmes": "cas_fraude_confirmes.csv",
        "actifs_si": "actifs_si.csv",
    }
    for tbl, csv in tables.items():
        df = pd.read_csv(os.path.join(DATA_DIR, csv))
        df.to_sql(tbl, con, index=False, if_exists="replace")

    # Index pour des requêtes API rapides
    cur = con.cursor()
    cur.executescript("""
        CREATE INDEX IF NOT EXISTS idx_fact_pdl  ON fact_consommation(id_pdl);
        CREATE INDEX IF NOT EXISTS idx_fact_date ON fact_consommation(date);
        CREATE INDEX IF NOT EXISTS idx_fact_zone ON fact_consommation(zone);
        CREATE INDEX IF NOT EXISTS idx_comp_pdl  ON dim_compteur(id_pdl);
        CREATE INDEX IF NOT EXISTS idx_meteo_zd  ON dim_meteo(zone, date);
    """)
    con.commit()

    # Récapitulatif (on récupère d'abord la liste, pour ne pas invalider le curseur)
    print("\nTables chargées :")
    names = [r[0] for r in cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall()]
    for name in names:
        n = cur.execute(f"SELECT COUNT(*) FROM '{name}'").fetchone()[0]
        print(f"  - {name:<26} {n:>8,} lignes")
    con.close()
    print("\n>> Entrepôt construit avec succès.")

if __name__ == "__main__":
    main()
