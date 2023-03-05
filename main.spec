# -*- mode: python ; coding: utf-8 -*-


block_cipher = None

import os
spec_root = os.path.realpath(SPECPATH)
options = []
from PyInstaller.utils.hooks import collect_submodules, collect_data_files
tf_hidden_imports = collect_submodules('vosk')
tf_datas = collect_data_files('vosk', subdir=None, include_py_files=True)


a = Analysis(
    ['main.py'],
    pathex=['voiceChat/Lib/site-packages'],
    binaries=[],
    datas=[('./model', './model'), ('voiceChat/Lib/site-packages/vosk', './vosk')],
    hiddenimports=tf_hidden_imports +[],
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
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
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
    name='main',
)
