"""
Génère un PDF propre à partir d'un fichier Markdown (pour envoi au prof).
Markdown -> HTML (lib markdown) -> PDF (xhtml2pdf).

On utilise la police intégrée (Helvetica/WinAnsi) qui gère les accents français
et l'euro ; on nettoie au préalable les quelques caractères spéciaux non gérés.

Usage : .venv\\Scripts\\python.exe scripts/generer_pdf.py docs/EXPLICATIONS-PROJET.md
"""
from __future__ import annotations
import os, sys
import markdown
from xhtml2pdf import pisa

# Remplacements de caractères "typographiques" par des équivalents sûrs
REMP = {
    "’": "'", "‘": "'", "“": '"', "”": '"',
    "–": "-", "—": "-", "…": "...", "→": "->",
    "←": "<-", "×": "x", "œ": "oe", "Œ": "OE",
    "•": "-", "≈": "~", "≤": "<=", "≥": ">=",
    "→": "->", "€": "EUR",
}

CSS = """
@page { size: a4; margin: 2cm; }
body { font-family: Helvetica; font-size: 10.5px; line-height: 1.45; color: #222; }
h1 { font-size: 20px; color: #1a5276; border-bottom: 2px solid #1a5276; padding-bottom: 4px; }
h2 { font-size: 15px; color: #1a5276; margin-top: 16px; }
h3 { font-size: 12.5px; color: #2471a3; }
table { border-collapse: collapse; width: 100%; margin: 8px 0; }
th, td { border: 1px solid #999; padding: 4px 6px; font-size: 9.5px; text-align: left; }
th { background-color: #eaf2f8; }
code { background-color: #f4f4f4; font-size: 9.5px; }
strong { color: #000; }
"""

def nettoyer(t: str) -> str:
    for k, v in REMP.items():
        t = t.replace(k, v)
    # on garde le jeu cp1252 (accents FR + euro), on retire le reste (ex. emojis)
    return t.encode("cp1252", "ignore").decode("cp1252")

def convertir(md_path: str):
    with open(md_path, "r", encoding="utf-8") as f:
        texte = nettoyer(f.read())
    corps = markdown.markdown(texte, extensions=["tables", "fenced_code", "sane_lists"])
    html = f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{corps}</body></html>"
    pdf_path = os.path.splitext(md_path)[0] + ".pdf"
    with open(pdf_path, "w+b") as out:
        res = pisa.CreatePDF(html, dest=out)
    if res.err:
        print("ERREUR lors de la génération PDF"); sys.exit(1)
    print(f">> PDF généré : {pdf_path} ({os.path.getsize(pdf_path)/1024:.0f} Ko)")

if __name__ == "__main__":
    cible = sys.argv[1] if len(sys.argv) > 1 else "docs/EXPLICATIONS-PROJET.md"
    convertir(cible)
