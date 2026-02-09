@echo off
chcp 65001 >nul
echo.
echo ============================================
echo   🧪 Smart Lab Report - Windows 打包工具
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

REM 切换到脚本目录
cd /d "%~dp0"

REM 安装依赖
echo.
echo 📦 检查依赖...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    pip install pyinstaller -q
)

REM 清理旧文件
echo.
echo 🧹 清理旧文件...
if exist "dist" rmdir /s /q dist
if exist "build" rmdir /s /q build

REM 打包（简化版 - 确保零 bug）
echo.
echo 🔨 开始打包（简化稳定版）...
echo    这可能需要 1-3 分钟...

pyinstaller ^
    --onefile ^
    --windowed ^
    --name "SmartLabReport" ^
    --clean ^
    --noconfirm ^
    gui_simple.py

if errorlevel 1 (
    echo ❌ 打包失败
    pause
    exit /b 1
)

REM 复制模板和数据
echo.
echo 📂 复制资源文件...
if exist "templates" (
    mkdir "dist\templates" 2>nul
    xcopy /e /i /y "templates" "dist\templates" >nul
)
if exist "data" (
    mkdir "dist\data" 2>nul
    xcopy /e /i /y "data" "dist\data" >nul
)

REM 创建 README
echo.
echo 📝 创建使用说明...

(
echo 🧪 Smart Lab Report - 使用说明
echo.
echo 一、使用方法
echo    1. 双击 SmartLabReport.exe 打开程序
echo    2. 选择实验数据文件（CSV/Excel）
echo    3. 填写报告信息
echo    4. 选择输出格式
echo    5. 点击生成报告
echo.
echo 二、支持的格式
echo    - 输入: .csv, .xlsx
echo    - 输出: .docx, .html, .md
echo.
echo 三、依赖
echo    - Python 3.10+
echo    - PySimpleGUI, pandas, matplotlib, python-docx
echo.
echo 四、注意事项
echo    - 确保数据文件格式正确
echo    - 首次运行可能需要几秒钟启动
echo.
echo 五、故障排除
echo    - 如果程序无法启动，请检查 Python 环境
echo    - 确保没有杀毒软件阻止程序运行
echo.
echo ============================================
echo   GitHub: https://github.com/KINGSTON-115/smart-lab-report
echo ============================================
) > "dist\使用说明.txt"

echo.
echo ============================================
echo   ✅ 打包完成！
echo ============================================
echo.
echo 📦 输出文件:
echo    dist\SmartLabReport.exe
echo.
echo 💡 使用方法:
echo    1. 将 dist 文件夹分享给用户
echo    2. 用户双击 SmartLabReport.exe 即可运行
echo    3. 无需安装 Python 或任何依赖！
echo.
echo ⚠️ 注意事项:
echo    - 首次启动可能需要 5-10 秒
echo    - 杀毒软件可能误报，建议添加到信任区
echo.
echo 📖 详细文档: README.md
echo.
pause
