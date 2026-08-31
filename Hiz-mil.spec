# -*- mode: python ; coding: utf-8 -*-

import sys
import platform

block_cipher = None
current_os = platform.system()

ICON_DIR = os.path.join('Views', 'icon')
icon_file = None
if current_os == 'Windows':
    icon_file = os.path.join(ICON_DIR, 'app.ico')
elif current_os == 'Darwin':
    icon_file = os.path.join(ICON_DIR, 'app.icns')
elif current_os == 'Linux':
    icon_file = os.path.join(ICON_DIR, 'app.png')

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('Manuals', 'Manuals'),
            ('qss', 'qss'),
            ('Lang', 'Lang'),
            ('Readme.md', '.'),
            ('LICENSE', '.'),
            ('THIRD_PARTY_NOTICES.md', '.'),
            ('Views/icon', 'Views/icon'),
            ('Views/resources_rc.py', 'Views')],
    hiddenimports=['pandas', 'numpy', 'bottleneck'],
    collect_submodules=['PySide6'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='App',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_file
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='App',
)

if current_os == 'Darwin':
    app = BUNDLE(
        coll,
        name='App.app',
        icon=icon_file,
        bundle_identifier=None,
    )
