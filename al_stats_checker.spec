# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['al_stats_checker.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\simad\\OneDrive\\Desktop\\scraper\\ship_stats_data', 'ship_stats_data'), ('C:\\Users\\simad\\AppData\\Roaming\\Python\\Python313\\site-packages\\pyfiglet', 'pyfiglet')],
    hiddenimports=[],
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
    a.binaries,
    a.datas,
    [],
    name='al_stats_checker',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
