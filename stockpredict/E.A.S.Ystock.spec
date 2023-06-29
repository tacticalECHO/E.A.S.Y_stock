# -*- mode: python ; coding: utf-8 -*-
import sys
sys.setrecursionlimit(sys.getrecursionlimit() * 5)

block_cipher = None


a = Analysis(
    ['main.py'],
    pathex=['curve.py', 'error_c.py','myMuti.py', 'read_out_toUI.py', 'stock_filter.py', 'stockget.py'],
    binaries=[],
    datas=[],
    hiddenimports=['PyQt5', 'numpy', 'sympy', 'akshare', 'pandas', 'multiprocessing', 'sklearn', 'PIL', 'cv2', 'qtawesome', 'json','mplfinance'],
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
    [],
    exclude_binaries=True,
    name='E.A.S.Ystock',
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
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='E.A.S.Ystock',
)
