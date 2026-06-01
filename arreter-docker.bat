@echo off
chcp 65001 >nul
cd /d "%~dp0volet-ild-dataeng"
echo Arret et suppression propre du conteneur "neovolt-api"...
docker compose down
echo.
echo Termine. Le conteneur a disparu de Docker Desktop (c'est normal).
pause
