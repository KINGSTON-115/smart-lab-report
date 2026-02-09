# 🪟 Smart Lab Report - Windows 使用指南

## 📥 获取 Windows 可执行文件

### 方式一：GitHub Release（推荐）

访问以下地址下载 Windows exe：
```
https://github.com/KINGSTON-115/smart-lab-report/releases
```

> **注意**：GitHub Actions 正在自动构建 Windows exe，构建完成后会自动添加到 Release。构建时间约 5-10 分钟。

### 方式二：使用 Python 立即运行（无需等待）

```bash
# 1. 安装 Python 3.10+
# 下载地址: https://www.python.org/downloads/

# 2. 克隆项目
git clone https://github.com/KINGSTON-115/smart-lab-report.git
cd smart-lab-report

# 3. 安装依赖
pip install -r requirements.txt

# 4. 运行程序
python gui.py
```

## 📖 使用方法

### 图形界面（推荐）

1. 运行 `gui.py` 或 `SmartLabReport.exe`
2. 点击「浏览」选择数据文件（CSV/Excel）
3. 填写报告信息（标题、作者、组别）
4. 选择实验模板
5. 点击「生成报告」

### 命令行

```bash
python cli.py --data 数据文件.csv --title "实验报告" --author "你的名字" --output 报告.docx
```

## 📊 支持的数据格式

| 格式 | 扩展名 | 说明 |
|------|--------|------|
| CSV | `.csv` | 逗号分隔值 |
| Excel | `.xlsx` | Excel 工作簿 |
| JSON | `.json` | JSON 数据 |

## 📝 支持的实验模板

| 学科 | 模板 |
|------|------|
| 🔬 物理 | 欧姆定律、力学、光学 |
| 🧪 化学 | 滴定分析、合成实验 |
| 🧬 生物 | 显微镜观察、PCR |
| 💻 计算机 | 排序算法、机器学习 |
| ⚙️ 工程 | 电路、材料力学 |

## 🤖 AI 分析配置

如需使用 AI 分析功能，需要配置 API Key：

```python
# 设置环境变量
export OPENAI_API_KEY="your-api-key"
# 或
export ANTHROPIC_API_KEY="your-api-key"
```

支持的 AI 服务：
- OpenAI (GPT-3.5/4)
- Claude (Anthropic)
- 通义千问 (阿里云)
- 智谱 AI (ChatGLM)
- 本地模型 (Ollama)

## ❓ 常见问题

**Q: 杀毒软件报警？**
A: 将程序添加到信任区，这是 PyInstaller 打包软件的正常行为。

**Q: 启动很慢？**
A: 首次启动需要 5-10 秒加载依赖。

**Q: 提示缺少 DLL？**
A: 请确保下载了完整的 exe 文件。

**Q: 图表中文显示乱码？**
A: 这是服务器环境的问题，本地 Windows 运行正常。

## 📞 支持

- **GitHub**: https://github.com/KINGSTON-115/smart-lab-report
- **Issues**: https://github.com/KINGSTON-115/smart-lab-report/issues

---

**让实验报告写作变得简单！** 🎉
