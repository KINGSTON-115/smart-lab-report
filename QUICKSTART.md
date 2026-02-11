# 🚀 Smart Lab Report - 快速入门指南

## 3 分钟上手

### 第 1 步：准备数据

创建一个 CSV 文件（或其他支持格式）：

```csv
电压(V),电流(A),电阻(Ω)
1.0,0.020,50.0
2.0,0.040,50.0
3.0,0.060,50.0
4.0,0.080,50.0
5.0,0.100,50.0
```

### 第 2 步：选择使用方式

| 方式 | 命令 | 适用 |
|------|------|------|
| 🌐 Web Demo | 双击 `web_app.html` | 所有人，最简单 |
| 💻 CLI | `python cli.py --data data.csv --title "实验报告"` | 开发者 |
| 🖱️ GUI | `python gui.py` | 桌面用户 |

### 第 3 步：生成报告

**Web Demo 截图预览：**

```
┌─────────────────────────────────────┐
│  🧪 Smart Lab Report                 │
│  ─────────────────────────────────  │
│                                     │
│  📁 第一步：选择实验数据              │
│  ┌─────────────────────────────┐    │
│  │ 📊 点击或拖拽文件到这里     │    │
│  └─────────────────────────────┘    │
│                                     │
│  📝 第二步：填写实验信息              │
│  ┌──────┬──────┬──────┐           │
│  │ 标题 │ 作者 │ 组别 │           │
│  └──────┴──────┴──────┘           │
│                                     │
│  🚀 第三步：生成报告                 │
│  ┌─────────────────────────────┐    │
│  │     🚀 一键生成报告          │    │
│  └─────────────────────────────┘    │
└─────────────────────────────────────┘
```

---

## 📖 详细用法

### CLI 命令行

```bash
# 基本用法
python cli.py \
  --data data/examples/欧姆定律数据.csv \
  --title "欧姆定律验证实验" \
  --author "张三"

# 指定模板
python cli.py \
  --data data.csv \
  --template chemistry_basic \
  --title "滴定实验"

# 生成图表
python cli.py \
  --data data.csv \
  --x "电压" \
  --y "电流" \
  --chart-type scatter

# 批量处理
python cli.py --batch
```

### GUI 图形界面

```bash
python gui.py
```

功能：
- 📁 文件选择器
- 👆 示例数据快捷按钮
- 📊 数据预览
- 📤 多格式输出

---

## 📁 支持的数据格式

| 格式 | 扩展名 | 说明 |
|------|--------|------|
| CSV | `.csv` | 逗号分隔值 |
| Excel | `.xlsx` | Excel 工作簿 |
| JSON | `.json` | JavaScript 对象表示法 |

---

## 📄 输出格式

| 格式 | 扩展名 | 特点 |
|------|--------|------|
| Word | `.docx` | 可编辑，适合打印 |
| HTML | `.html` | 响应式网页 |
| Markdown | `.md` | 笔记兼容 |
| PDF | `.pdf` | 正式提交 |

---

## 🎨 模板选择

### 物理实验 (`physics_basic`)
```
一、实验目的
二、实验原理
三、实验仪器
四、实验步骤
五、数据处理 ← 自动统计
六、误差分析
七、结论与讨论
```

### 化学实验 (`chemistry_basic`)
```
一、实验目的
二、实验原理
三、试剂与仪器
四、实验步骤
五、数据与观察 ← 自动统计
六、计算
七、误差分析
八、结论
```

### 生物实验 (`biology_basic`)
```
一、实验目的
二、背景介绍
三、材料与方法
四、实验结果 ← 自动统计
五、分析讨论
六、结论
```

### 计算机实验 (`cs_algorithm`)
```
一、问题描述
二、算法设计
三、时间复杂度分析 ← 自动统计
四、实现代码
五、测试用例
六、实验结果
七、讨论与优化
```

### 工程实验 (`engineering_basic`)
```
一、实验目的
二、理论依据
三、设备规格
四、实验程序
五、数据分析 ← 自动统计
六、性能评估
七、结论
```

---

## ⚙️ 高级选项

### 图表类型

```bash
--chart-type line      # 折线图
--chart-type scatter   # 散点图
--chart-type bar       # 柱状图
--chart-type histogram # 直方图
```

### 安静模式（减少输出）

```bash
python cli.py --data data.csv --title "报告" --quiet
```

---

## ❓ 常见问题

### Q: 找不到数据列？
A: 确保 CSV 文件有表头行，数值列会被自动检测。

### Q: 中文显示乱码？
A: 系统已配置中文字体，Windows 上效果最佳。

### Q: 如何自定义报告内容？
A: 修改 `templates/` 目录下的模板文件。

---

## 📦 项目结构

```
smart-lab-report/
├── 🧪 src/
│   └── generators/      # 核心生成器
│       ├── word_generator.py   # Word 报告
│       ├── report_generator.py # HTML 报告
│       ├── chart_generator.py  # 图表生成
│       └── ai_engine.py       # AI 分析
├── 📄 templates/        # 模板文件
├── 📁 data/
│   └── examples/       # 示例数据
├── 📂 output/          # 输出目录
├── 🌐 web_app.html    # Web Demo
├── 🖱️ gui.py          # 图形界面
├── 💻 cli.py           # 命令行
└── 📖 README.md       # 主文档
```

---

## 🤝 贡献指南

欢迎贡献代码！

1. Fork 本项目
2. 创建特性分支：`git checkout -b feature/AmazingFeature`
3. 提交更改：`git commit -m 'Add some AmazingFeature'`
4. 推送分支：`git push origin feature/AmazingFeature`
5. 发起 Pull Request

---

<p align="center">
  Made with ❤️ by <b>Coder2 (冶官坊)</b>
</p>
