@echo off
chcp 65001 >nul
cd /d "%~dp0"

if not exist "data\processed\neovolt.db" (
  echo [ERREUR] La base n'existe pas encore.
  echo Double-clique d'abord sur "demarrer-demo.bat".
  pause
  exit /b 1
)

echo ============================================================
echo   NEOVOLT GRID+  --  Lancement du conteneur DOCKER
echo ============================================================
echo Construction de l'image et demarrage du conteneur "neovolt-api"...
cd volet-ild-dataeng
docker compose up -d --build
if errorlevel 1 goto erreur

echo.
echo ============================================================
echo   Conteneur "neovolt-api" DEMARRE.
echo   1) Ouvre Docker Desktop  ^>  Containers  : il est en VERT (running).
echo   2) Page web (s'ouvre toute seule) : http://127.0.0.1:8000/docs
echo      (si erreur, attends 3 sec et appuie sur F5)
echo   Pour l'ARRETER : double-clique sur "arreter-docker.bat".
echo ============================================================
start "" "http://127.0.0.1:8000/docs"
pause
exit /b 0

:erreur
echo.
echo [ERREUR] Docker n'a pas pu demarrer le conteneur.
echo Verifie que Docker Desktop est bien lance (icone baleine, "Engine running").
pause
exit /b 1
