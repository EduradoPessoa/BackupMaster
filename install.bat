@echo off
REM Script de instalação do BackupMaster para Windows

echo ========================================
echo  BackupMaster - Instalacao
echo ========================================
echo.

REM Verifica se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    echo Por favor, instale Python 3.8 ou superior de https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python encontrado
echo.

REM Cria ambiente virtual
echo Criando ambiente virtual...
python -m venv venv

REM Ativa ambiente virtual
echo Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM Atualiza pip
echo Atualizando pip...
python -m pip install --upgrade pip

REM Instala dependências
echo Instalando dependencias...
pip install -r requirements.txt

echo.
echo ========================================
echo  Instalacao concluida com sucesso!
echo ========================================
echo.
echo Para usar o BackupMaster:
echo.
echo 1. Interface Grafica (GUI):
echo    venv\Scripts\python.exe backupmaster_gui.py
echo.
echo 2. Linha de Comando (CLI):
echo    venv\Scripts\python.exe backupmaster_cli.py --help
echo.
echo Atalhos criados:
echo - run_gui.bat (Interface Grafica)
echo - run_cli.bat (Linha de Comando)
echo.

REM Cria atalhos
echo @echo off > run_gui.bat
echo call venv\Scripts\activate.bat >> run_gui.bat
echo python backupmaster_gui.py >> run_gui.bat

echo @echo off > run_cli.bat
echo call venv\Scripts\activate.bat >> run_cli.bat
echo python backupmaster_cli.py %%* >> run_cli.bat

pause
