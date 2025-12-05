@echo off
REM Script para inicializar repositório Git e preparar para GitHub

echo ========================================
echo  BackupMaster - Inicializar Git
echo ========================================
echo.

REM Verifica se Git está instalado
git --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Git nao encontrado!
    echo Por favor, instale Git de https://git-scm.com/
    pause
    exit /b 1
)

echo [OK] Git encontrado
echo.

REM Inicializa repositório
echo Inicializando repositorio Git...
git init

REM Adiciona todos os arquivos
echo Adicionando arquivos...
git add .

REM Primeiro commit
echo Criando primeiro commit...
git commit -m "Initial commit: BackupMaster v1.0.0 - Sistema Profissional de Backup"

echo.
echo ========================================
echo  Repositorio Git inicializado!
echo ========================================
echo.
echo Proximos passos:
echo.
echo 1. Crie um repositorio no GitHub:
echo    https://github.com/new
echo.
echo 2. Configure o remote:
echo    git remote add origin https://github.com/SEU-USUARIO/backupmaster.git
echo.
echo 3. Envie para o GitHub:
echo    git branch -M main
echo    git push -u origin main
echo.
echo Ou execute:
echo    setup_github.bat
echo.

pause
