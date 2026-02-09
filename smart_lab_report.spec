# -*- mode: python ; coding: utf-8 -*-
"""
Smart Lab Report - Windows Executable Configuration
Windows 可执行文件打包配置

使用方法:
  pyinstaller smart_lab_report.spec
  
或直接:
  pyinstaller --onefile --windowed gui.py
"""

import os
import sys

block_cipher = None

def get_package_data():
    """收集需要打包的数据文件"""
    datas = []
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    # 打包模板目录
    for subdir in ['templates', 'data']:
        src = os.path.join(base_path, subdir)
        if os.path.exists(src):
            datas.append((subdir, subdir))
    
    return datas

def get_hidden_imports():
    """收集所有需要的隐式导入"""
    return [
        # 核心库
        'pandas', 'pandas._libs', 'pandas._libs.tslibs',
        'numpy', 'numpy.core', 'numpy.core._methods', 'numpy.core._multiarray_umath',
        'matplotlib', 'matplotlib.backends', 'matplotlib.backends._backend_agg',
        'matplotlib.ft2font', 'matplotlib._path', 'matplotlib._mathtext',
        
        # 模板引擎
        'jinja2', 'jinja2.utils', 'jinja2.loaders', 'jinja2.compiler',
        
        # Word 文档
        'docx', 'docx.opc', 'docx.oxml', 'docx.oxml.ns',
        'docx.text', 'docx.enum', 'docx.enum.text', 'docx.enum.table',
        'docx.enum.style', 'docx.shape', 'docx.table', 'docx.styles', 'docx.utils',
        
        # Excel 支持
        'openpyxl', 'openpyxl.workbook', 'openpyxl.worksheet', 'openpyxl.reader',
        'openpyxl.styles', 'openpyxl.utils', 'openpyxl.utils.cell',
        
        # GUI
        'PySimpleGUI', 'tkinter', 'tkinter.ttk',
        'tkinter.filedialog', 'tkinter.messagebox', 'tkinter.simpledialog',
        'tkinter.colorchooser', 'tkinter.font',
        
        # YAML
        'yaml', 'yaml.safe_load', 'yaml.constructor',
        
        # 图像
        'PIL', 'PIL._imaging', 'PIL.PngImagePlugin', 'PIL.Image',
        'fontTools', 'fontTools.ttLib', 'fontTools.ttLib.ttFont',
        
        # 系统库
        'ctypes', 'ctypes.wintypes',
        'email.utils', 'http.cookies',
        'urllib.parse', 'urllib.request',
        'xml.etree', 'xml.etree.ElementTree',
        'subprocess', 'socket', 'struct',
        
        # JSON
        'json', 'json.decoder', 'json.encoder',
    ]

a = Analysis(
    ['gui.py'],
    pathex=[os.path.dirname(os.path.abspath(__file__))],
    binaries=[],
    datas=get_package_data(),
    hiddenimports=get_hidden_imports(),
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # 排除测试相关
        'test', 'unittest', 'pytest', 'nose', 'doctest',
        # 排除调试相关
        'debug', 'pdb', 'pdb', 'ipdb', 'rdb',
        # 排除不需要的numpy子模块
        'numpy.distutils', 'numpy.f2py', 'numpy.distutils.cpuinfo',
        # 排除文档工具
        'sphinx', 'sphinxcontrib',
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
    [],
    exclude_binaries=True,
    name='SmartLabReport',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # GUI 程序不需要控制台
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch='x86_64',
    codesign_identity=None,
    entitlements_file=None,
    # 尝试使用图标，如果不存在则跳过
    icon=None,  # 稍后手动添加图标
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

# Windows 兼容层
if os.name == 'nt':
    import win32com.client
    
    # 添加版本信息
    import win32api
