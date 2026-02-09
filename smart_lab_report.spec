# -*- mode: python ; coding: utf-8 -*-
"""
Smart Lab Report PyInstaller Spec File
Windows Executable Configuration
"""

block_cipher = None

a = Analysis(
    ['gui.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('src', 'src'),
        ('data', 'data'),
    ],
    hiddenimports=[
        'pandas',
        'pandas._libs',
        'matplotlib',
        'matplotlib.backends',
        'matplotlib.backends._backend_agg',
        'jinja2',
        'jinja2.utils',
        'docx',
        'docx.opc',
        'docx.oxml',
        'docx.oxml.ns',
        'docx.text',
        'docx.enum',
        'docx.enum.text',
        'docx.enum.table',
        'docx.enum.style',
        'docx.shape',
        'docx.table',
        'docx.styles',
        'docx.utils',
        'PySimpleGUI',
        'PySimpleGUI.PySimpleGUI',
        'numpy',
        'numpy.core',
        'numpy.core.multiarray',
        'PIL',
        'PIL._imaging',
        'fontTools',
        'fontTools.ttLib',
        'fontTools.ttLib.ttFont',
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

a.binaries += [
    ('matplotlib/mpl-data/fonts/ttf/DejaVuSans.ttf', 'mpl-data/fonts/ttf/DejaVuSans.ttf', 'DATA'),
]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='SmartLabReport',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # No console for GUI
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='docs/icon.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SmartLabReport',
)
