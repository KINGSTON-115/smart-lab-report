@echo off
chcp 65001 >nul
echo.
echo ============================================
echo   🧪 Smart Lab Report - Windows 打包脚本
echo ============================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未检测到 Python，请先安装 Python 3.10+
    echo    下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python 检测成功

REM 安装依赖
echo.
echo 📦 安装依赖...
pip install -r requirements.txt --break-system-packages

if errorlevel 1 (
    echo ❌ 依赖安装失败
    pause
    exit /b 1
)

echo ✅ 依赖安装完成

REM 检查 PyInstaller
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo.
    echo 📦 安装 PyInstaller...
    pip install pyinstaller --break-system-packages
)

echo.
echo 🔨 开始打包...
echo    这可能需要几分钟，请耐心等待...

REM 打包
pyinstaller ^
    --name "SmartLabReport" ^
    --onefile ^
    --windowed ^
    --icon="docs/icon.ico" ^
    --add-data "src;src" ^
    --add-data "data;data" ^
    --add-data "templates;templates" ^
    --hidden-import pandas ^
    --hidden-import matplotlib ^
    --hidden-import jinja2 ^
    --hidden-import docx ^
    --hidden-import PySimpleGUI ^
    gui.py

if errorlevel 1 (
    echo ❌ 打包失败
    pause
    exit /b 1
)

echo.
echo ============================================
echo   ✅ 打包完成！
echo ============================================
echo.
echo 📂 输出文件: dist\SmartLabReport.exe
echo.
echo 💡 使用方法:
echo    1. 双击 SmartLabReport.exe 打开程序
echo    2. 选择实验数据文件
echo    3. 填写报告信息
echo    4. 点击"生成报告"
echo.
pause
