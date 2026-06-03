@echo off
chcp 65001 >nul
cd /d "%~dp0"
set PY=.venv\Scripts\python.exe

echo ============================================================
echo   NEOVOLT GRID+  --  Generation des PDF (a envoyer au prof)
echo ============================================================

if not exist "%PY%" (
  echo [ERREUR] .venv introuvable. Voir GUIDE-DEMO.md.
  pause
  exit /b 1
)

echo Generation du PDF d'explication...
"%PY%" scripts\generer_pdf.py docs\EXPLICATIONS-PROJET.md
echo Generation du PDF du dossier projet...
"%PY%" scripts\generer_pdf.py docs\dossier-projet.md

echo.
echo ============================================================
echo   PDF crees dans le dossier "docs".
echo   - docs\EXPLICATIONS-PROJET.pdf
echo   - docs\dossier-projet.pdf
echo ============================================================
start "" "docs"
pause
