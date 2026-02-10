# 🧪 Smart Lab Report - 智能实验报告生成器

> **做实验 2 小时，写报告 6 小时？让 AI 帮你写！**

[![GitHub Release](https://img.shields.io/github/release/KINGSTON-115/smart-lab-report.svg)](https://github.com/KINGSTON-115/smart-lab-report/releases)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🚀 一、立即使用（3 种方式）

### 🌐 方式 A：在线 Web Demo（最推荐！）

```
下载 web_app.html → 浏览器打开 → 点点点 → 完成！
```

| 特点 | 说明 |
|------|------|
| ✨ 渐变动画 | 视觉效果流畅 |
| 📱 响应式 | 手机电脑都能用 |
| 👆 新手引导 | 4 步教程上手 |
| ⚡ 秒级响应 | 无需等待 |

### 💻 方式 B：Windows exe（推荐！）

```
1. 下载: https://github.com/KINGSTON-115/smart-lab-report/releases
2. 双击: SmartLabReport.exe
3. 选择数据 → 填写信息 → 生成报告
```

| 输出格式 | 文件类型 | 适用场景 |
|----------|----------|----------|
| 📄 Word | `.docx` | 打印提交 |
| 🌐 HTML | `.html` | 网页分享 |
| 📝 Markdown | `.md` | 笔记存档 |
| 📑 PDF | `.pdf` | 正式提交 |

### 🔧 方式 C：源码运行（开发者）

```bash
# 1. 克隆项目
git clone https://github.com/KINGSTON-115/smart-lab-report.git
cd smart-lab-report

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行方式
python gui.py              # 🖱️ 图形界面
python cli.py --help       # 💻 命令行
python web_app.html       # 🌐 浏览器打开
```

---

## ✨ 二、核心功能

| 功能 | 图标 | 状态 | 说明 |
|------|------|------|------|
| 一键生成 | 🚀 | ✅ | 选择数据 → 自动生成 |
| Word 输出 | 📄 | ✅ | `.docx` 格式 |
| HTML 网页 | 🌐 | ✅ | 响应式页面 |
| AI 分析 | 🤖 | ✅ | 自动趋势分析 |
| 智能绑图 | 📊 | ✅ | 折线/散点/柱状/直方图 |
| 多学科模板 | 📚 | ✅ | 5 种专业模板 |
| 数据验证 | ✅ | ✅ | 缺失值/异常值检测 |

### 📚 学科模板

| 模板 | 学科 | 适用实验 |
|------|------|----------|
| 🔬 `physics_basic` | 物理 | 欧姆定律、受迫振动 |
| 🧪 `chemistry_basic` | 化学 | 滴定分析、合成实验 |
| 🧬 `biology_basic` | 生物 | 显微镜观察、PCR |
| 💻 `cs_algorithm` | 计算机 | 排序算法、复杂度分析 |
| ⚙️ `engineering_basic` | 工程 | 电路设计、材料测试 |

### 📊 数据格式支持

```
✅ CSV    Excel (.xlsx)    JSON    数据框 (DataFrame)
```

---

## 📖 三、使用教程

### 快速上手（4 步）

```
📁 选择数据  →  📝 填写信息  →  📤 选择格式  →  🚀 生成报告
```

### CLI 命令行示例

```bash
# 基本用法
python cli.py \
  --data data/examples/欧姆定律数据.csv \
  --title "欧姆定律验证实验" \
  --author "张三" \
  --output report.docx

# 自定义模板
python cli.py \
  --data data.csv \
  --template chemistry_basic \
  --title "滴定分析实验"

# 查看帮助
python cli.py --help
```

### Web Demo 界面

```
┌─────────────────────────────────────────────────────────┐
│  🧪 Smart Lab Report                                    │
│  ─────────────────────────────────────────────────────  │
│                                                         │
│  📁 第一步：选择实验数据                                 │
│  ┌─────────────────────────────────────────────────┐   │
│  │  📊 点击或拖拽文件到这里                         │   │
│  │  支持 CSV、Excel、JSON 格式                     │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  📝 第二步：填写实验信息                                 │
│  ┌──────┬──────┬──────┬──────┐                        │
│  │ 标题 │ 作者 │ 组别 │ 模板 │                        │
│  └──────┴──────┴──────┴──────┘                        │
│                                                         │
│  📤 第三步：选择输出格式                                  │
│  ☐ Word  ☐ HTML  ☐ Markdown  ☐ PDF                   │
│                                                         │
│  🚀 第四步：生成报告                                     │
│  ┌─────────────────────────────┐                       │
│  │    🚀 一键生成报告           │                       │
│  └─────────────────────────────┘                       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 四、应用场景

| 场景 | 说明 |
|------|------|
| 📝 大学实验报告 | 物理/化学/生物实验报告 |
| 🔬 科研数据记录 | 实验数据分析与可视化 |
| 📊 实验图表生成 | 自动绑图、统计分析 |
| 📈 项目报告 | 算法复杂度分析报告 |

---

## 📦 五、项目结构

```
smart-lab-report/
├── 🧪 src/                     # 核心代码
│   ├── generators/            # 生成器
│   │   ├── word_generator.py  # Word 报告
│   │   ├── report_generator.py # HTML 报告
│   │   ├── chart_generator.py  # 图表生成
│   │   └── ai_engine.py        # AI 分析
│   └── validators/             # 验证器
├── 📄 templates/               # 模板文件
├── 📁 data/                    # 示例数据
├── 📂 output/                  # 输出目录
├── 🌐 web_app.html             # Web 演示
├── 🖱️ gui.py                   # 图形界面
├── 💻 cli.py                    # 命令行
└── 📖 README.md                 # 本文档
```

---

## 🤝 六、贡献指南

欢迎贡献代码！

1. **Fork** 项目
2. **创建** 分支 (`git checkout -b feature/AmazingFeature`)
3. **提交** 修改 (`git commit -m 'Add some AmazingFeature'`)
4. **推送** 分支 (`git push origin feature/AmazingFeature`)
5. **发起** Pull Request

---

## 📄 七、许可证

MIT License - 开源免费，放心使用！

---

## 🙏 八、致谢

- [python-docx](https://python-docx.readthedocs.io/) - Word 文档生成
- [Matplotlib](https://matplotlib.org/) - 数据可视化
- [Jinja2](https://jinja.palletsprojects.com/) - 模板引擎
- [Pandas](https://pandas.pydata.org/) - 数据处理

---

<p align="center">
  <b>Made with ❤️ by Coder2 (冶官坊)</b><br>
  <a href="https://github.com/KINGSTON-115/smart-lab-report">
    🌟 Star us on GitHub!
  </a>
</p>
