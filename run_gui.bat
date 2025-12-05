@echo off
echo ============================================================
echo BackupMaster - Launcher com Debug
echo ============================================================
echo.

REM Ativa ambiente virtual se existir
if exist venv\Scripts\activate.bat (
    echo Ativando ambiente virtual...
    call venv\Scripts\activate.bat
)

echo Executando BackupMaster...
echo.

python backupmaster_gui.py 2>&1

echo.
echo ============================================================
echo Aplicacao encerrada
echo Exit Code: %ERRORLEVEL%
echo ============================================================
echo.
pause
