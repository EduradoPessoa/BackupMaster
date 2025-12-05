#!/bin/bash
# Build script for Linux executables

echo "========================================"
echo " BackupMaster - Build Executables"
echo " Platform: Linux"
echo "========================================"
echo ""

# Check if PyInstaller is installed
if ! python3 -c "import PyInstaller" 2>/dev/null; then
    echo "[INFO] Installing PyInstaller..."
    pip3 install -r requirements-build.txt
fi

echo "[INFO] Building GUI executable..."
pyinstaller --clean --noconfirm backupmaster_gui.spec

echo ""
echo "[INFO] Building CLI executable..."
pyinstaller --clean --noconfirm backupmaster_cli.spec

echo ""
echo "========================================"
echo " Build Complete!"
echo "========================================"
echo ""
echo "Executables created in dist/ folder:"
echo " - dist/BackupMaster (GUI)"
echo " - dist/backupmaster (CLI)"
echo ""
echo "To test:"
echo " ./dist/BackupMaster"
echo " ./dist/backupmaster --help"
echo ""

# Make executables executable
chmod +x dist/BackupMaster 2>/dev/null
chmod +x dist/backupmaster 2>/dev/null

echo "Executables are now executable!"
