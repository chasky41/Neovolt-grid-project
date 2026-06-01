"""
Néovolt Grid+ — Analyse SIEM des journaux de sécurité (volet Cybersécurité).

47 824 événements (mars→mai 2026). On applique des RÈGLES DE DÉTECTION de type SOC
sur journaux_securite.csv pour faire ressortir les signaux d'attaque réels, plutôt
que de réciter des bonnes pratiques génériques.

Règles implémentées :
  R1  Brute force        : IP source avec un nombre anormal d'échecs de connexion.
  R2  IP externes        : activité depuis des IP hors plan d'adressage interne (10.x).
  R3  Compromission      : une IP qui échoue en rafale PUIS réussit (prise de contrôle).
  R4  Compte sur-exposé  : utilisateur vu depuis un nombre anormal d'IP sources.
  R5  Exfiltration       : exports de données massifs / hors heures ouvrées.
  R6  Élévation/sondage  : pics d'accès refusés et de modifications de configuration.

Sorties : volet-cyber/figures/*.png, docs/rapport-siem.md
Usage : .venv\\Scripts\\python.exe volet-cyber/analyse_journaux.py
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
import seaborn as sns

sns.set_theme(style="whitegrid")
HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
DATA_DIR = os.environ.get("NEOVOLT_DATA", os.path.normpath(os.path.join(PROJ, "..", "donnees")))
FIGS = os.path.join(HERE, "figures"); os.makedirs(FIGS, exist_ok=True)
REPORT = os.path.join(PROJ, "docs", "rapport-siem.md")

buf = io.StringIO()
def log(*a):
    line = " ".join(str(x) for x in a); print(line); buf.write(line + "\n")

def is_interne(ip: str) -> bool:
    return str(ip).startswith("10.")

def main():
    log("# Rapport SIEM — Détection sur les journaux de sécurité (volet Cyber)\n")
    js = pd.read_csv(os.path.join(DATA_DIR, "journaux_securite.csv"))
    js["horodatage"] = pd.to_datetime(js["horodatage"], errors="coerce")
    js["heure"] = js["horodatage"].dt.hour
    js["jour"] = js["horodatage"].dt.date
    js["interne"] = js["source_ip"].map(is_interne)
    js["echec"] = js["resultat"].str.contains("echec", case=False, na=False)
    n = len(js)
    log(f"- Période : {js['horodatage'].min()} → {js['horodatage'].max()}")
    log(f"- {n:,} événements | {js['utilisateur'].nunique()} utilisateurs | "
        f"{js['source_ip'].nunique()} IP sources distinctes")
    log(f"- Taux d'échec global : {js['echec'].mean():.1%} "
        f"({int(js['echec'].sum()):,} échecs)\n")

    # --- R2 : IP externes -----------------------------------------------------
    log("## R2 — Activité depuis des IP externes (hors 10.x)\n")
    ext = js[~js["interne"]]
    log(f"- {ext['source_ip'].nunique()} IP externes pour {len(ext):,} événements "
        f"({len(ext)/n:.1%} du trafic).")
    top_ext = ext["source_ip"].value_counts().head(5)
    for ip, c in top_ext.items():
        ech = js[(js["source_ip"] == ip)]["echec"].mean()
        log(f"  - {ip} : {c} événements, {ech:.0%} d'échec")
    log("")

    # --- R1 : Brute force -----------------------------------------------------
    log("## R1 — Brute force (échecs de connexion par IP)\n")
    fail = js[js["echec"]]
    top_fail = fail["source_ip"].value_counts().head(8)
    log("| IP source | Échecs | Interne ? |")
    log("|---|---|---|")
    for ip, c in top_fail.items():
        log(f"| {ip} | {c} | {'oui' if is_interne(ip) else '**NON (externe)**'} |")
    bf_ip = top_fail.index[0]
    log(f"\n- **Suspect principal : {bf_ip}** avec {top_fail.iloc[0]} échecs "
        f"(vs médiane {fail['source_ip'].value_counts().median():.0f} par IP).")

    # --- R3 : Compromission (échecs puis succès depuis la même IP) ------------
    log("\n## R3 — Tentative de compromission (échecs en rafale puis succès)\n")
    succ_bf = js[(js["source_ip"] == bf_ip) & (~js["echec"])]
    if len(succ_bf):
        log(f"- ⚠️ L'IP {bf_ip} a aussi **{len(succ_bf)} connexion(s) RÉUSSIE(S)** "
            f"sur le(s) compte(s) : {sorted(succ_bf['utilisateur'].unique())} "
            f"→ signature de **compte potentiellement compromis**, à traiter en priorité.")
    else:
        log(f"- L'IP {bf_ip} n'a aucune connexion réussie (brute force a priori échouée, "
            f"mais à bloquer).")

    # --- R4 : comptes vus depuis trop d'IP ------------------------------------
    log("\n## R4 — Comptes vus depuis un nombre anormal d'IP sources\n")
    ip_par_user = js.groupby("utilisateur")["source_ip"].nunique().sort_values(ascending=False)
    log(f"- Anomalie structurelle : {js['utilisateur'].nunique()} utilisateurs mais "
        f"{js['source_ip'].nunique()} IP → en moyenne "
        f"{js['source_ip'].nunique()/js['utilisateur'].nunique():.0f} IP/utilisateur "
        f"(attendu : quelques-unes). Signature de partage de comptes ou de proxy/rotation d'IP.")
    for u, c in ip_par_user.head(5).items():
        log(f"  - {u} : {c} IP sources distinctes")

    # --- R5 : exfiltration (exports) ------------------------------------------
    log("\n## R5 — Exports de données (risque d'exfiltration / RGPD)\n")
    exp = js[js["type_evenement"].str.contains("export", case=False, na=False)]
    log(f"- {len(exp):,} exports de données au total.")
    exp_user = exp["utilisateur"].value_counts().head(5)
    for u, c in exp_user.items():
        log(f"  - {u} : {c} exports")
    nuit = exp[(exp["heure"] < 6) | (exp["heure"] >= 22)]
    log(f"- Exports hors heures ouvrées (22h–6h) : **{len(nuit)}** "
        f"({len(nuit)/max(len(exp),1):.0%}) → à investiguer (exfiltration possible).")

    # --- R6 : accès refusés & modifications de config -------------------------
    log("\n## R6 — Sondage de privilèges & modifications de configuration\n")
    refus = js[js["type_evenement"].str.contains("refus", case=False, na=False)]
    modif = js[js["type_evenement"].str.contains("config", case=False, na=False)]
    log(f"- Accès refusés : {len(refus):,} | Modifications de config : {len(modif):,}")
    modif_nuit = modif[(modif["heure"] < 6) | (modif["heure"] >= 22)]
    log(f"- Modifications de config hors heures ouvrées : {len(modif_nuit)} "
        f"(changement furtif possible).")

    # --- Figures --------------------------------------------------------------
    plt.figure(figsize=(8, 4))
    cc = ["#c0392b" if not is_interne(ip) else "#7f8c8d" for ip in top_fail.index]
    sns.barplot(x=top_fail.values, y=top_fail.index, hue=top_fail.index,
                palette=cc, legend=False)
    plt.title("Top IP sources par nombre d'échecs (rouge = externe)")
    plt.xlabel("Nb d'échecs de connexion"); plt.tight_layout()
    plt.savefig(os.path.join(FIGS, "siem_brute_force.png"), dpi=120); plt.close()

    by_hour = js.groupby(["heure", "echec"]).size().unstack(fill_value=0)
    plt.figure(figsize=(9, 4))
    by_hour.plot(kind="bar", stacked=True, color=["#27ae60", "#c0392b"],
                 ax=plt.gca())
    plt.title("Événements par heure de la journée (vert = succès, rouge = échec)")
    plt.xlabel("Heure"); plt.ylabel("Nb d'événements")
    plt.legend(["succès", "échec"]); plt.tight_layout()
    plt.savefig(os.path.join(FIGS, "siem_par_heure.png"), dpi=120); plt.close()

    daily_fail = fail.groupby("jour").size()
    plt.figure(figsize=(9, 3.5))
    daily_fail.plot(color="#c0392b")
    plt.title("Échecs de connexion par jour"); plt.ylabel("Nb d'échecs"); plt.xlabel("")
    plt.tight_layout(); plt.savefig(os.path.join(FIGS, "siem_echecs_jour.png"), dpi=120); plt.close()

    # --- Synthèse des règles SIEM (livrable SOC) ------------------------------
    log("\n## Règles de détection à industrialiser (SIEM/SOC)\n")
    log("| ID | Règle | Seuil proposé | Sévérité |")
    log("|---|---|---|---|")
    log("| R1 | Échecs de connexion répétés depuis une même IP | > 20 / heure | Haute |")
    log("| R2 | Connexion depuis IP hors plan d'adressage interne | tout événement | Moyenne |")
    log("| R3 | Échecs en rafale puis succès (même IP/compte) | motif | **Critique** |")
    log("| R4 | Compte authentifié depuis > N IP distinctes | > 5 / jour | Moyenne |")
    log("| R5 | Export de données hors heures ouvrées | tout export 22h–6h | Haute |")
    log("| R6 | Modification de configuration hors heures ouvrées | tout événement | Haute |")
    log("\n→ Conforme à l'exigence NIS 2 : notification d'un incident majeur **sous 24 h** "
        "(voir runbook). Détection à brancher sur un SIEM (ex. Elastic) en cible.")

    log("\n## Figures produites\n")
    log("- `siem_brute_force.png`, `siem_par_heure.png`, `siem_echecs_jour.png`")

    with open(REPORT, "w", encoding="utf-8") as fh:
        fh.write(buf.getvalue())
    log(f"\n>> Rapport : {REPORT}")

if __name__ == "__main__":
    main()
