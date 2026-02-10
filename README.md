# 🧪 Smart Lab Report - 智能实验报告生成器

> **做实验 2 小时，写报告 6 小时？让 AI 帮你写！**

[![GitHub Release](https://img.shields.io/github/release/KINGSTON-115/smart-lab-report.svg)](https://github.com/KINGSTON-115/smart-lab-report/releases)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🚀 一、立即使用（选择一种方式）

### 方式 A：在线 Web Demo（最简单！推荐！）

**无需安装，直接浏览器打开：**

1. 下载 `web_app.html` 文件
2. 浏览器直接打开
3. 选择数据 → 填写信息 → 生成报告

**Web Demo 特点：**
- ✨ 渐变动画效果
- 📱 响应式设计（手机/电脑都能用）
- 🎨 现代化 UI
- 🚀 秒级响应

### 方式 B：下载 Windows exe（推荐！）

1. **下载**：https://github.com/KINGSTON-115/smart-lab-report/releases
2. **双击** `SmartLabReport.exe` 运行
3. **选择数据** → 填写信息 → 生成报告

### 方式 C：源码运行（开发者）

```bash
# 克隆并运行
git clone https://github.com/KINGSTON-115/smart-lab-report.git
cd smart-lab-report
pip install -r requirements.txt
python gui.py  # 图形界面
python cli.py --help  # 命令行

### 方式 C：CLI 命令行

```bash
# 安装依赖
pip install -r requirements.txt

# 生成报告
python cli.py \
  --data data/examples/欧姆定律数据.csv \
  --title "欧姆定律验证实验" \
  --author "张三" \
  --output report.docx
```

---

## ✨ 二、核心功能

| 功能 | 说明 | 状态 |
|------|------|------|
| 🪟 Windows exe | 双击运行，无需 Python | ⏳ 构建中 |
| 📄 Word 输出 | 直接生成 `.docx` | ✅ 已完成 |
| 🤖 AI 分析 | GPT/Claude 自动分析 | ✅ 已完成 |
| 📊 自动绑图 | Matplotlib 图表嵌入 | ✅ 已完成 |
| 📚 14 个模板 | 物理/化学/生物/计算机/工程 | ✅ 已完成 |

---

## 📦 三、安装依赖

```txt
# requirements.txt
matplotlib>=3.8.0
pandas>=2.0.0
numpy>=1.24.0
jinja2>=3.1.0
python-docx>=1.1.0
openpyxl>=3.1.0
PySimpleGUI>=4.60.0
pyyaml>=6.0
```

安装：`pip install -r requirements.txt`

---

## 📖 四、使用说明

### 数据格式

| 格式 | 扩展名 | 示例 |
|------|--------|------|
| CSV | `.csv` | `电压,电流,电阻` |
| Excel | `.xlsx` | Excel 工作簿 |
| JSON | `.json` | JSON 数据 |

### 实验模板

```
templates/
├── physics/           🔬 物理实验
├── chemistry/         🧪 化学实验
├── biology/          🧬 生物实验
├── cs/               💻 计算机实验
└── engineering/      ⚙️ 工程实验
```

### AI 配置

```bash
# 设置 API Key
export OPENAI_API_KEY="your-key"
export ANTHROPIC_API_KEY="your-key"
```

---

## 📁 五、项目结构

```
smart-lab-report/
├── 📄 gui.py              # 图形界面
├── 📄 cli.py             # 命令行工具
├── 📦 src/generators/    # 核心模块
│   ├── ai_engine.py      # AI 分析
│   ├── chart_generator.py # 图表生成
│   ├── word_generator.py # Word 输出
│   └── ...
├── 📚 templates/         # 实验模板
├── 📊 data/examples/     # 示例数据
└── 📖 README.md          # 本文档
```

---

## 🤝 六、贡献指南

欢迎贡献代码！

1. Fork 本仓库
2. 创建分支：`git checkout -b feature/amazing-feature`
3. 提交更改：`git commit -m 'Add amazing feature'`
4. 推送到分支：`git push origin feature/amazing-feature`
5. 开启 Pull Request

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

## 🙏 致谢

- 感谢所有贡献者
- 灵感来源：大学实验报告之痛 😓

---

**让实验报告写作变得简单！** 🎉

<p align="center">
  <a href="https://github.com/KINGSTON-115/smart-lab-report">
    <img src="https://img.shields.io/github/stars/KINGSTON-115/smart-lab-report?style=social" alt="Stars">
  </a>
  <a href="https://github.com/KINGSTON-115/smart-lab-report/releases">
    <img src="https://img.shields.io/github/downloads/KINGSTON-115/smart-lab-report/total" alt="Downloads">
  </a>
</p>
