# 🧪 Smart Lab Report - Windows 快速启动

## ⚡ 最快方式：本地运行（无需等待）

```bash
# 1. 安装 Python 3.10+
# https://www.python.org/downloads/

# 2. 克隆并运行
git clone https://github.com/KINGSTON-115/smart-lab-report.git
cd smart-lab-report
pip install -r requirements.txt
python gui.py
```

## 📦 如果想生成 Windows exe（需要 Windows 系统）

在 **Windows 电脑**上：

```bash
# 1. 克隆项目
git clone https://github.com/KINGSTON-115/smart-lab-report.git
cd smart-lab-report

# 2. 安装依赖
pip install -r requirements.txt

# 3. 打包exe
pip install pyinstaller
pyinstaller --onefile --windowed --name "SmartLabReport" gui_simple.py

# 生成的exe在 dist/SmartLabReport.exe
```

## 🔧 GitHub Actions 构建（自动）

项目已配置 GitHub Actions 自动构建 Windows exe：
- **状态**: 正在修复触发问题
- **预计**: 修复完成后自动构建
- **下载**: https://github.com/KINGSTON-115/smart-lab-report/releases

## 📞 如果你有 Windows 电脑

可以帮我运行打包命令，这样所有用户都能用到：

```cmd
git clone https://github.com/KINGSTON-115/smart-lab-report.git
cd smart-lab-report
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --onefile --windowed --name "SmartLabReport" gui_simple.py
```

运行后把 `dist/SmartLabReport.exe` 上传到 Release 即可！

## ❓ 问题排查

| 问题 | 解决方案 |
|------|----------|
| pip 找不到 | 使用 `python -m pip` |
| 依赖安装失败 | `pip install --upgrade pip` |
| 打包失败 | 确保 Windows 系统 + Python 3.10 |

**GitHub**: https://github.com/KINGSTON-115/smart-lab-report
