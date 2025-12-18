# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Document Management Client.
"""

import sys
from pathlib import Path

block_cipher = None

# Get the directory where this spec file is located
import os
try:
    spec_root = Path(SPECPATH)
except NameError:
    # Fallback if SPECPATH is not available - use current working directory
    # This assumes the spec file is run from the project root directory
    spec_root = Path(os.getcwd())

# Collect all data files
datas = [
    # Include icon if it exists
    (str(spec_root / 'icon.png'), '.') if (spec_root / 'icon.png').exists() else None,
]

# Filter out None values
datas = [d for d in datas if d is not None]

# Hidden imports for PyInstaller to detect
hiddenimports = [
    # PyQt5 modules
    'PyQt5.QtCore',
    'PyQt5.QtGui',
    'PyQt5.QtWidgets',
    'PyQt5.QtPrintSupport',
    # Application modules
    'ui.main_window',
    'ui.file_browser',
    'ui.location_dialog',
    'ui.scanner_dialog',
    'ui.styles',
    'services.file_watcher',
    'services.folder_manager',
    'services.scanner_service',
    'utils.config',
    # Watchdog
    'watchdog',
    'watchdog.observers',
    'watchdog.events',
    'watchdog.observers.polling',
    # PIL/Pillow
    'PIL',
    'PIL.Image',
    'PIL.ImageQt',
    'PIL.ImageTk',
    # pyinsane2 (scanner support - optional)
    'pyinsane2',
    'pyinsane2.sane',
    'pyinsane2.sane.abstract',
    'pyinsane2.sane.rawapi',
    'pyinsane2.sane.daemon',
    'pyinsane2.wia',
    'pyinsane2.wia.abstract',
    'pyinsane2.wia.rawapi',
]

a = Analysis(
    ['main.py'],
    pathex=[str(spec_root)],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # Exclude unnecessary modules to reduce size
        'tkinter',
        'matplotlib',
        'numpy',
        'scipy',
        'pandas',
    ],
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
    name='DocumentManagementClient',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Enable UPX compression to reduce file size
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False if sys.platform == 'win32' else True,  # No console on Windows, console on Linux for debugging
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(spec_root / 'build' / 'windows' / 'icon.ico') if (spec_root / 'build' / 'windows' / 'icon.ico').exists() else None,
)

