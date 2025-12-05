# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for BackupMaster GUI
Builds standalone executable for Windows, Linux, and Mac
"""

block_cipher = None

a = Analysis(
    ['backupmaster_gui.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'backupmaster',
        'backupmaster.core',
        'backupmaster.auth',
        'backupmaster.telemetry',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='BackupMaster',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon file here if you have one
)

# For macOS, create .app bundle
if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='BackupMaster.app',
        icon=None,
        bundle_identifier='com.backupmaster.app',
        info_plist={
            'NSPrincipalClass': 'NSApplication',
            'NSHighResolutionCapable': 'True',
        },
    )
