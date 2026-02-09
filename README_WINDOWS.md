# 🪟 Windows 用户使用指南

## ⚠️ 重要说明

**GitHub Actions 正在自动构建 Windows exe，构建完成后会自动添加到 Release。**

预计构建时间：5-10 分钟

## 📥 下载地址

访问 GitHub Releases 下载：
```
https://github.com/KINGSTON-115/smart-lab-report/releases
```

## 🐛 临时解决方案（立即可用）

如果需要立即使用，可以：

### 方案 1：使用 Python 运行（推荐）
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

### 方案 2：等待 GitHub Actions 构建
Windows exe 正在自动构建，构建完成后会自动添加到 Release。

## 📖 使用方法

1. 下载 `SmartLabReport.exe`
2. 双击运行
3. 选择实验数据文件（CSV/Excel）
4. 填写报告信息
5. 点击「生成报告」

## ❓ 常见问题

**Q: 杀毒软件报警？**
A: 将程序添加到信任区，这是打包软件的正常行为。

**Q: 启动很慢？**
A: 首次启动需要 5-10 秒加载依赖，后续会变快。

**Q: 提示缺少 DLL？**
A: 请下载完整版本，Windows exe 已包含所有依赖。
