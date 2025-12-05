@echo off
REM Build script for Windows executables

echo ========================================
echo  BackupMaster - Build Executables
echo  Platform: Windows
echo ========================================
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo [INFO] Installing PyInstaller...
    pip install -r requirements-build.txt
)

echo [INFO] Building GUI executable...
pyinstaller --clean --noconfirm backupmaster_gui.spec

echo.
echo [INFO] Building CLI executable...
pyinstaller --clean --noconfirm backupmaster_cli.spec

echo.
echo ========================================
echo  Build Complete!
echo ========================================
echo.
echo Executables created in dist/ folder:
echo  - dist\BackupMaster.exe (GUI)
echo  - dist\backupmaster.exe (CLI)
echo.
echo To test:
echo  dist\BackupMaster.exe
echo  dist\backupmaster.exe --help
echo.

pause
