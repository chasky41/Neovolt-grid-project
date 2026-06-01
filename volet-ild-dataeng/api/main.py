"""
Néovolt Grid+ — API de la plateforme data (volet ILD / Data Eng).

Expose les données nettoyées et les indicateurs métier de l'entrepôt aux autres
volets (Analyst, Data Scientist, dashboards) et aux applications décisionnelles.
Documentation interactive auto-générée sur /docs (Swagger) et /redoc.

Lancer (le dossier parent contient des tirets -> se placer DANS api/) :
    cd volet-ild-dataeng/api
    ..\\..\\.venv\\Scripts\\uvicorn.exe main:app --reload --port 8000
    # puis ouvrir http://127.0.0.1:8000/docs
Pré-requis : entrepôt construit (volet-ild-dataeng/build_warehouse.py).
"""
from __future__ import annotations
import os
import sqlite3
from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import RedirectResponse

# --- Localisation de l'entrepôt ----------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.normpath(os.path.join(HERE, "..", ".."))
DB_PATH = os.environ.get(
    "NEOVOLT_DB", os.path.join(PROJ, "data", "processed", "neovolt.db"))

app = FastAPI(
    title="Néovolt Grid+ — API plateforme data",
    description=(
        "Accès aux relevés de consommation nettoyés, aux référentiels et aux "
        "indicateurs métier (qualité, fraude, incidents). Prototype — volet "
        "Ingénierie Logiciel & Data Engineering."
    ),
    version="0.1.0",
)

def get_con() -> sqlite3.Connection:
    if not os.path.exists(DB_PATH):
        raise HTTPException(503, f"Entrepôt introuvable ({DB_PATH}). "
                                 f"Lance build_warehouse.py.")
    con = sqlite3.connect(DB_PATH, check_same_thread=False)
    con.row_factory = sqlite3.Row
    return con

def rows(con, sql, params=()):
    return [dict(r) for r in con.execute(sql, params).fetchall()]

# --- Endpoints ----------------------------------------------------------------
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse("/docs")

@app.get("/health", tags=["système"])
def health():
    """État de santé de l'API et de l'entrepôt."""
    con = get_con()
    n = con.execute("SELECT COUNT(*) FROM fact_consommation").fetchone()[0]
    bornes = con.execute(
        "SELECT MIN(date), MAX(date) FROM fact_consommation").fetchone()
    con.close()
    return {"status": "ok", "db": os.path.basename(DB_PATH),
            "releves": n, "periode": {"debut": bornes[0], "fin": bornes[1]}}

@app.get("/zones", tags=["référentiel"])
def zones():
    """Liste des zones et nombre de PDL par zone."""
    con = get_con()
    data = rows(con, """SELECT zone, COUNT(DISTINCT id_pdl) AS nb_pdl
                        FROM fact_consommation GROUP BY zone ORDER BY zone""")
    con.close()
    return data

@app.get("/pdl/{id_pdl}", tags=["référentiel"])
def pdl_info(id_pdl: str):
    """Fiche d'un point de livraison (compteur + client)."""
    con = get_con()
    r = rows(con, """SELECT c.*, cl.segment, cl.commune, cl.nb_personnes_foyer,
                            cl.surface_m2
                     FROM dim_compteur c
                     LEFT JOIN dim_client cl ON c.id_client = cl.id_client
                     WHERE c.id_pdl = ?""", (id_pdl,))
    con.close()
    if not r:
        raise HTTPException(404, f"PDL {id_pdl} introuvable.")
    return r[0]

@app.get("/pdl/{id_pdl}/consommation", tags=["consommation"])
def conso_pdl(id_pdl: str,
              debut: Optional[str] = Query(None, description="AAAA-MM-JJ"),
              fin: Optional[str] = Query(None, description="AAAA-MM-JJ")):
    """Série temporelle de consommation quotidienne d'un PDL (avec flags qualité)."""
    con = get_con()
    sql = """SELECT date, consommation_kwh, flag_zero, flag_aberrant, flag_manquant
             FROM fact_consommation WHERE id_pdl = ?"""
    params = [id_pdl]
    if debut:
        sql += " AND date >= ?"; params.append(debut)
    if fin:
        sql += " AND date <= ?"; params.append(fin)
    sql += " ORDER BY date"
    data = rows(con, sql, params)
    con.close()
    if not data:
        raise HTTPException(404, f"Aucun relevé pour le PDL {id_pdl}.")
    return {"id_pdl": id_pdl, "n": len(data), "releves": data}

@app.get("/consommation/par-zone", tags=["consommation"])
def conso_par_zone(zone: Optional[str] = None,
                   debut: Optional[str] = None, fin: Optional[str] = None):
    """Consommation quotidienne agrégée par zone (pour le dashboard exploitation réseau)."""
    con = get_con()
    sql = """SELECT zone, date, ROUND(SUM(consommation_kwh), 1) AS conso_kwh,
                    COUNT(*) AS nb_pdl
             FROM fact_consommation WHERE flag_manquant = 0"""
    params = []
    if zone:
        sql += " AND zone = ?"; params.append(zone)
    if debut:
        sql += " AND date >= ?"; params.append(debut)
    if fin:
        sql += " AND date <= ?"; params.append(fin)
    sql += " GROUP BY zone, date ORDER BY date, zone"
    data = rows(con, sql, params)
    con.close()
    return {"n": len(data), "points": data}

@app.get("/qualite", tags=["qualité"])
def qualite():
    """Indicateurs de qualité des données (part de relevés flagués)."""
    con = get_con()
    r = con.execute("""SELECT COUNT(*) n, SUM(flag_zero) z,
                              SUM(flag_aberrant) a, SUM(flag_manquant) m
                       FROM fact_consommation""").fetchone()
    con.close()
    n = r[0]
    return {"releves_total": n,
            "zeros": r[1], "aberrants": r[2], "manquants": r[3],
            "taux_exploitable": round(1 - r[3] / n, 4)}

@app.get("/fraude", tags=["métier"])
def fraude():
    """Cas de fraude confirmés (vérité terrain) — usage restreint, données sensibles."""
    con = get_con()
    cas = rows(con, "SELECT * FROM cas_fraude_confirmes ORDER BY date_detection")
    par_type = rows(con, """SELECT type_fraude, COUNT(*) n
                            FROM cas_fraude_confirmes GROUP BY type_fraude""")
    con.close()
    return {"nb_cas": len(cas), "par_type": par_type, "cas": cas}

@app.get("/incidents", tags=["métier"])
def incidents():
    """Synthèse des incidents réseau (pour le dashboard exploitation)."""
    con = get_con()
    par_type = rows(con, """SELECT type, COUNT(*) n,
                                   SUM(nb_pdl_impactes) pdl_impactes,
                                   ROUND(AVG(duree_minutes),1) duree_moy_min
                            FROM incidents_reseau GROUP BY type ORDER BY n DESC""")
    con.close()
    return {"par_type": par_type}
