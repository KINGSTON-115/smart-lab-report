# 🧪 Smart Lab Report - 智能实验报告生成器

> **做实验 2 小时，写报告 6 小时？让 AI 帮你写！**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📌 项目简介

一个从**实验数据/代码/图像**自动生成规范实验报告的工具，让大学生专注于实验本身，而非繁琐的报告写作。

## ✨ 核心亮点

| 特性 | 说明 |
|------|------|
| 🖱️ **一键操作** | Windows exe 双击即用，无需安装 Python |
| 📄 **Word 输出** | 直接生成 `.docx`，符合中国大学生习惯 |
| 🤖 **AI 增强** | 可选接入大模型，自动分析实验现象 |
| 📊 **自动绑图** | 智能绑定 Matplotlib 图表 |
| 🎓 **多学科模板** | 物理/化学/生物/计算机/工程全覆盖 |

## 🚀 快速开始

### Windows 用户（推荐）

**方式一：下载 exe**

1. 从 [Releases](https://github.com/KINGSTON-115/smart-lab-report/releases) 下载 `SmartLabReport.exe`
2. 双击运行，选择数据 → 填写信息 → 生成报告

**方式二：源码运行**

```cmd
git clone https://github.com/KINGSTON-115/smart-lab-report.git
cd smart-lab-report
pip install -r requirements.txt
python gui.py
```

### Linux/Mac 用户

```bash
git clone https://github.com/KINGSTON-115/smart-lab-report.git
cd smart-lab-report
pip install -r requirements.txt
python gui.py
```

### CLI 使用

```bash
# 生成物理实验报告
python cli.py \
  --data data/examples/欧姆定律数据.csv \
  --title "欧姆定律验证实验" \
  --author "张三" \
  --output report.docx
```

## 📖 使用教程

### 1. 准备数据

支持 **CSV / Excel / JSON** 格式：

```csv
电压(V),电流(A),电阻(Ω)
1.0,0.020,50.0
2.0,0.040,50.0
3.0,0.060,50.0
4.0,0.080,50.0
5.0,0.100,50.0
```

### 2. 打开程序

- Windows：双击 `SmartLabReport.exe`
- 终端：`python gui.py`

### 3. 生成报告

```
📁 选择数据文件
📝 填写标题/作者/组别
📊 选择图表参数
📤 选择输出格式（Word/HTML）
🚀 点击生成
```

## 📁 项目结构

```
smart-lab-report/
├── src/
│   ├── core/engine.py          # 核心引擎
│   ├── generators/
│   │   ├── chart_generator.py   # 图表生成
│   │   ├── report_generator.py  # HTML报告
│   │   ├── word_generator.py    # Word文档 ⭐
│   │   └── ai_analyzer.py       # AI分析（可选）
│   └── tests/                   # 测试用例
├── data/
│   └── examples/                # 示例数据
├── gui.py                       # GUI界面 ⭐
├── cli.py                       # 命令行工具
├── main.py                      # Windows入口
├── requirements.txt             # 依赖配置
├── build.bat                    # Windows打包脚本
└── README.md
```

## 🎓 支持的实验模板

| 模板 | 适用学科 | 章节 |
|------|---------|------|
| `physics_basic` | 物理 | 目的→原理→仪器→步骤→数据→误差→结论 |
| `chemistry_basic` | 化学 | 目的→原理→试剂→步骤→观察→计算→误差→结论 |
| `biology_basic` | 生物 | 目的→背景→材料→结果→分析→结论 |
| `cs_algorithm` | 计算机 | 问题→算法→复杂度→代码→测试→结果→讨论 |
| `engineering_basic` | 工程 | 目的→理论→规格→程序→分析→评估→结论 |

## 🛠️ 技术栈

| 技术 | 用途 |
|------|------|
| Python 3.10+ | 主语言 |
| PySimpleGUI | Windows GUI |
| python-docx | Word 文档 |
| Matplotlib | 图表生成 |
| Pandas | 数据处理 |
| Jinja2 | 模板引擎 |

## 📦 依赖安装

```txt
matplotlib>=3.8.0
pandas>=2.0.0
numpy>=1.24.0
jinja2>=3.1.0
python-docx>=1.1.0
openpyxl>=3.1.0
PySimpleGUI>=4.60.0
pyyaml>=6.0
```

## 🔨 Windows 打包

```cmd
.\build.bat
```

输出：`dist/SmartLabReport.exe`

## 🤝 贡献指南

欢迎提交 Issue 和 PR！

1. Fork 本仓库
2. 创建分支：`git checkout -b feature/amazing-feature`
3. 提交更改：`git commit -m 'Add amazing feature'`
4. 推送到分支：`git push origin feature/amazing-feature`
5. 开启 Pull Request

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

## 🙏 致谢

- 感谢所有贡献者
- 灵感来源：大学实验报告之痛 😓

---

**让实验报告写作变得简单！** 🎉

---

<p align="center">
  <a href="https://github.com/KINGSTON-115/smart-lab-report">
    <img src="https://img.shields.io/github/stars/KINGSTON-115/smart-lab-report?style=social" alt="Stars">
  </a>
  <a href="https://github.com/KINGSTON-115/smart-lab-report/issues">
    <img src="https://img.shields.io/github/issues/KINGSTON-115/smart-lab-report" alt="Issues">
  </a>
</p>
