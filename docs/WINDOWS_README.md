# 🧪 Smart Lab Report - Windows 使用指南
# Smart Lab Report - Windows User Guide

## 📦 一键使用（推荐）

### 方法 1：下载 exe（最简单）

1. **下载安装包**
   
   从 GitHub Releases 页面下载：
   ```
   https://github.com/KINGSTON-115/smart-lab-report/releases
   ```
   
   下载文件：`SmartLabReport.exe`

2. **双击运行**
   
   ```
   SmartLabReport.exe
   ```

3. **使用步骤**
   
   ```
   ① 点击「浏览」选择实验数据（CSV/Excel/JSON）
   ② 填写报告标题、作者、组别
   ③ 选择实验模板（物理/化学/生物/计算机/工程）
   ④ 设置图表参数（X轴、Y轴、图表类型）
   ⑤ 选择输出格式（Word/HTML/Markdown）
   ⑥ 点击「生成报告」
   ```

### 方法 2：从源码运行

1. **安装 Python**
   
   下载地址：https://www.python.org/downloads/
   
   版本要求：Python 3.10+

2. **克隆项目**
   ```cmd
   git clone https://github.com/KINGSTON-115/smart-lab-report.git
   cd smart-lab-report
   ```

3. **安装依赖**
   ```cmd
   pip install -r requirements.txt
   ```

4. **运行程序**
   ```cmd
   python gui.py
   ```

---

## 🔧 数据格式要求

### 支持的文件格式

| 格式 | 扩展名 | 说明 |
|------|--------|------|
| CSV | `.csv` | 逗号分隔值，推荐使用 |
| Excel | `.xlsx` | Microsoft Excel 文件 |
| JSON | `.json` | JavaScript 对象表示法 |

### CSV 数据示例

```csv
电压(V),电流(A),电阻(Ω)
1.0,0.020,50.0
2.0,0.040,50.0
3.0,0.060,50.0
4.0,0.080,50.0
5.0,0.100,50.0
```

### 数据要求

- ✅ 第一行为列标题
- ✅ 数值型数据
- ✅ 无合并单元格
- ✅ 编码为 UTF-8

---

## 📝 使用教程

### 示例：生成物理实验报告

1. **准备数据文件** `欧姆定律数据.csv`
   ```csv
   电压(V),电流(A)
   1.0,0.020
   2.0,0.040
   3.0,0.060
   4.0,0.080
   5.0,0.100
   ```

2. **打开程序**，选择该文件

3. **填写信息**
   - 标题：欧姆定律验证实验
   - 作者：张三
   - 组别：物理1班第3组
   - 模板：物理实验基础模板

4. **设置图表**
   - X轴：电压(V)
   - Y轴：电流(A)
   - 类型：散点图

5. **生成报告**，选择输出格式（Word）

6. **打开输出文件**，填写缺失内容（实验目的、原理等）

---

## ❓ 常见问题

### Q: 生成的 Word 报告里图表是白色的？
A: 这是字体警告，不影响实际使用。图表已正确生成。

### Q: 支持 PDF 输出吗？
A: 目前支持 Word 和 HTML。PDF 可以在 Word 中另存为 PDF。

### Q: 能自动分析实验现象吗？
A: 需要安装 AI 依赖。运行 `pip install langchain openai` 后可用。

### Q: 图表中文显示乱码？
A: 这是服务器环境的中文字体问题。Windows 本地运行不会出现。

### Q: 报错 "ModuleNotFoundError"？
A: 缺少依赖，运行 `pip install -r requirements.txt`

---

## 📞 反馈

- **GitHub Issues**: https://github.com/KINGSTON-115/smart-lab-report/issues
- **功能建议**: 欢迎提交 Issue

---

**让实验报告写作变得简单！** 🎉
