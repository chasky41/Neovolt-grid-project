@echo off
chcp 65001 >nul
cd /d "%~dp0"
set PY=.venv\Scripts\python.exe

echo ============================================================
echo   NEOVOLT GRID+  --  Preparation de la demo
echo ============================================================
echo.

if not exist "%PY%" (
  echo [ERREUR] L'environnement Python .venv est introuvable.
  echo Ouvre le GUIDE-DEMO.md, section "Installation une seule fois".
  pause
  exit /b 1
)

echo [1/6] Nettoyage des donnees...
"%PY%" scripts\02_nettoyage.py >nul || goto erreur
echo       OK

echo [2/6] Construction de l'entrepot de donnees...
"%PY%" volet-ild-dataeng\build_warehouse.py >nul || goto erreur
echo       OK

echo [3/6] Detection de fraude (modele)...
"%PY%" volet-datascience\detection_fraude.py >nul || goto erreur
echo       OK

echo [4/6] Analyses (consommation + reclamations)...
"%PY%" volet-analyst\analyse_descriptive.py >nul || goto erreur
"%PY%" volet-analyst\nlp_reclamations.py >nul || goto erreur
echo       OK

echo [5/6] Tableaux de bord + business case + SIEM...
"%PY%" volet-analyst\dashboard.py >nul || goto erreur
"%PY%" volet-cpid-pilotage\business_case.py >nul || goto erreur
"%PY%" volet-cpid-pilotage\dashboard_pilotage.py >nul || goto erreur
"%PY%" volet-cyber\analyse_journaux.py >nul || goto erreur
echo       OK

echo [6/6] Ouverture des tableaux de bord dans le navigateur...
start "" "volet-analyst\dashboards\1_dashboard_exploitation.html"
start "" "volet-analyst\dashboards\2_dashboard_finance.html"
start "" "volet-analyst\dashboards\3_dashboard_relation_client.html"
start "" "volet-cpid-pilotage\dashboard_pilotage.html"

echo.
echo ============================================================
echo   PRET POUR LA DEMO.
echo   Les 4 tableaux de bord viennent de s'ouvrir.
echo   Pour montrer l'API en direct : double-clique sur "lancer-api.bat".
echo ============================================================
pause
exit /b 0

:erreur
echo.
echo [ERREUR] Une etape a echoue. Voir GUIDE-DEMO.md section "Si ca plante".
pause
exit /b 1
