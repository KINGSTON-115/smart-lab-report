# 🧪 Smart Lab Report - Core Engine
# 智能实验报告生成器 - 核心引擎

import os
import json
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

@dataclass
class ExperimentData:
    """实验数据容器"""
    raw_data: pd.DataFrame
    code_files: List[str] = field(default_factory=list)
    image_files: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass  
class ReportConfig:
    """报告配置"""
    template: str = "default"
    output_format: str = "pdf"  # pdf, markdown, html
    author: str = ""
    group: str = ""
    date: str = ""
    
class LabReportGenerator:
    """实验报告生成器主类"""
    
    def __init__(self, config: Optional[ReportConfig] = None):
        self.config = config or ReportConfig()
        self.templates = self._load_templates()
        
    def _load_templates(self) -> Dict:
        """加载报告模板"""
        template_dir = Path(__file__).parent / "templates"
        templates = {}
        for f in template_dir.glob("*.md"):
            templates[f.stem] = f.read_text()
        return templates
    
    def load_data(self, data_path: str) -> ExperimentData:
        """加载实验数据"""
        ext = Path(data_path).suffix.lower()
        if ext in ['.csv', '.xlsx']:
            df = pd.read_csv(data_path) if ext == '.csv' else pd.read_excel(data_path)
        elif ext == '.json':
            df = pd.json_normalize(json.load(open(data_path)))
        else:
            raise ValueError(f"不支持的数据格式: {ext}")
            
        return ExperimentData(raw_data=df)
    
    def load_code(self, code_path: str) -> str:
        """加载分析代码"""
        with open(code_path, 'r') as f:
            return f.read()
    
    def generate(self, title: str, description: str = "") -> str:
        """生成实验报告（Markdown格式）"""
        if not self.config.author:
            self.config.author = "匿名学生"
        if not self.config.date:
            self.config.date = datetime.now().strftime("%Y-%m-%d")
            
        template = self.templates.get(self.config.template, self.templates.get("default", DEFAULT_TEMPLATE))
        
        # 替换模板变量
        report = template.format(
            title=title,
            author=self.config.author,
            group=self.config.group,
            date=self.config.date,
            description=description,
            data_summary=self._summarize_data(),
            timestamp=datetime.now().isoformat()
        )
        return report
    
    def _summarize_data(self) -> str:
        """数据摘要"""
        return "数据统计将在此显示..."
    
    def save(self, report: str, output_path: str):
        """保存报告"""
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path).write_text(report)
        print(f"✅ 报告已保存: {output_path}")


# 默认报告模板
DEFAULT_TEMPLATE = """# {title}

**作者**: {author} | **组别**: {group} | **日期**: {date}

---

## 📋 实验概述

{description}

---

## 📊 实验数据

{data_summary}

---

## 📈 数据分析

*在此处自动生成图表和分析*

---

## 🔬 结论

*实验结论和分析...*

---

## 📝 误差分析

*误差来源及影响分析...*

---

*报告生成时间: {timestamp}*
"""


# CLI 入口点
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="智能实验报告生成器")
    parser.add_argument("--data", required=True, help="实验数据文件路径")
    parser.add_argument("--template", default="default", help="报告模板")
    parser.add_argument("--output", required=True, help="输出文件路径")
    parser.add_argument("--author", help="作者姓名")
    parser.add_argument("--title", required=True, help="实验标题")
    
    args = parser.parse_args()
    
    generator = LabReportGenerator(ReportConfig(
        template=args.template,
        author=args.author or ""
    ))
    
    data = generator.load_data(args.data)
    report = generator.generate(args.title)
    generator.save(report, args.output)
