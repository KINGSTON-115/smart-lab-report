# 🧪 智能实验报告生成器 (Smart Lab Report)

> **做实验 2 小时，写报告 6 小时？让 AI 帮你写！**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📌 项目简介

一个从**实验数据/代码/图像**自动生成规范实验报告的工具，让大学生专注于实验本身，而非繁琐的报告写作。

## 🎯 核心功能

### 基础功能
- 📄 **多格式支持**: 读取 CSV/Excel/JSON 数据、Python/Matlab 代码、图像文件
- 📝 **模板生成**: 自动填充实验指导书模板（结论、分析、误差分析）
- 📊 **图表生成**: 自动绑定 Matplotlib 绘图，生成可视化图表
- 📖 **多格式输出**: Markdown / PDF / HTML

### 进阶功能 (AI 增强)
- 🤖 **智能分析**: 接入大模型自动解释实验现象
- 💡 **异常检测**: 自动标记异常数据点
- 📈 **趋势预测**: 基于历史数据预测实验趋势

## 🚀 快速开始

### 安装

```bash
git clone https://github.com/KINGSTON-115/smart-lab-report.git
cd smart-lab-report
pip install -r requirements.txt
```

### 使用示例

```python
from smart_lab_report import LabReportGenerator

# 初始化生成器
generator = LabReportGenerator(
    template="physics_basic",  # 物理实验基础模板
    data_path="data/circuits.csv",
    code_path="src/analysis.py"
)

# 生成报告
report = generator.generate(
    title="电路实验 - 欧姆定律验证",
    author="张三",
    group="物理1班第3组"
)

# 保存为 PDF
report.save("output/欧姆定律实验报告.pdf")
```

## 📁 项目结构

```
smart-lab-report/
├── src/
│   ├── core/           # 核心引擎
│   ├── generators/     # 报告生成器
│   ├── utils/          # 工具函数
│   ├── templates/      # 报告模板
│   └── tests/         # 测试用例
├── data/
│   └── examples/       # 示例数据
├── scripts/            # CLI 脚本
├── docs/              # 文档
├── requirements.txt
└── README.md
```

## 🎓 支持的实验类型

| 学科 | 示例实验 | 数据格式 |
|------|---------|----------|
| 物理 | 欧姆定律、受迫振动 | CSV, Excel |
| 化学 | 滴定分析、光谱测定 | JSON, CSV |
| 生物 | 细胞计数、PCR 数据 | Excel, CSV |
| 计算机 | 算法复杂度、机器学习 | Python 代码 |
| 工程 | 电路设计、材料测试 | CSV, MATLAB |

## 🛠️ 技术栈

- **Python 3.10+** - 主语言
- **Matplotlib / Seaborn** - 图表生成
- **WeasyPrint / ReportLab** - PDF 输出
- **Pandas / NumPy** - 数据处理
- **LangChain / OpenAI** - AI 分析（可选）

## 📦 依赖安装

```txt
matplotlib>=3.8.0
pandas>=2.0.0
numpy>=1.24.0
jinja2>=3.1.0
weasyprint>=60.0
pyyaml>=6.0
```

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启 Pull Request

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE)

## 🙏 致谢

- 感谢所有贡献者
- 灵感来源：大学实验报告之痛 😓

---

**让实验报告写作变得简单！** 🎉
