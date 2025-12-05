#!/bin/bash
# Build script for macOS executables

echo "========================================"
echo " BackupMaster - Build Executables"
echo " Platform: macOS"
echo "========================================"
echo ""

# Check if PyInstaller is installed
if ! python3 -c "import PyInstaller" 2>/dev/null; then
    echo "[INFO] Installing PyInstaller..."
    pip3 install -r requirements-build.txt
fi

echo "[INFO] Building GUI application..."
pyinstaller --clean --noconfirm backupmaster_gui.spec

echo ""
echo "[INFO] Building CLI executable..."
pyinstaller --clean --noconfirm backupmaster_cli.spec

echo ""
echo "========================================"
echo " Build Complete!"
echo "========================================"
echo ""
echo "Applications created in dist/ folder:"
echo " - dist/BackupMaster.app (GUI - macOS App Bundle)"
echo " - dist/backupmaster (CLI)"
echo ""
echo "To test:"
echo " open dist/BackupMaster.app"
echo " ./dist/backupmaster --help"
echo ""

# Make CLI executable
chmod +x dist/backupmaster 2>/dev/null

echo "Ready to use!"
