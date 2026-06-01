@echo off
chcp 65001 >nul
cd /d "%~dp0"

if not exist "data\processed\neovolt.db" (
  echo [ERREUR] L'entrepot n'existe pas encore.
  echo Double-clique d'abord sur "demarrer-demo.bat".
  pause
  exit /b 1
)

echo ============================================================
echo   NEOVOLT GRID+  --  API en direct
echo   Adresse : http://127.0.0.1:8000/docs
echo   (si la page montre une erreur, attends 3 sec et appuie sur F5)
echo   Pour ARRETER l'API : ferme cette fenetre ou Ctrl+C
echo ============================================================

REM Ouvre le navigateur (si erreur de connexion : attends 3 sec puis F5)
start "" "http://127.0.0.1:8000/docs"

cd volet-ild-dataeng\api
"..\..\.venv\Scripts\uvicorn.exe" main:app --port 8000
pause
