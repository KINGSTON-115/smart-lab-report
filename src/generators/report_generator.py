# 🧪 报告生成器 - 多模板支持
# Report Generator - Multi-template support

import os
import json
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass, field
from datetime import datetime
from jinja2 import Template, Environment, BaseLoader
import base64
from io import BytesIO

from .chart_generator import ChartGenerator, ChartConfig

@dataclass
class ReportSection:
    """报告章节配置"""
    name: str  # 章节标识符
    title: str  # 章节标题
    content: str = ""  # 章节内容（可选）
    required: bool = True  # 是否必需

@dataclass
class ReportTemplate:
    """报告模板配置"""
    name: str
    display_name: str
    description: str
    sections: List[ReportSection] = field(default_factory=list)
    subjects: List[str] = field(default_factory=list)  # 适用学科
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ReportTemplate':
        return cls(
            name=data['name'],
            display_name=data['display_name'],
            description=data['description'],
            sections=[ReportSection(**s) for s in data.get('sections', [])],
            subjects=data.get('subjects', [])
        )

class ReportGenerator:
    """报告生成器 - 支持多模板"""
    
    TEMPLATE_REGISTRY = {
        "physics_basic": ReportTemplate(
            name="physics_basic",
            display_name="物理实验基础模板",
            description="适用于大学物理实验（力学、热学、光学等）",
            subjects=["physics"],
            sections=[
                ReportSection(name="experiment_purpose", title="一、实验目的"),
                ReportSection(name="experiment_principle", title="二、实验原理"),
                ReportSection(name="experiment_apparatus", title="三、实验仪器"),
                ReportSection(name="experiment_steps", title="四、实验步骤"),
                ReportSection(name="data_processing", title="五、数据处理"),
                ReportSection(name="error_analysis", title="六、误差分析"),
                ReportSection(name="conclusion", title="七、结论与讨论"),
            ]
        ),
        "chemistry_basic": ReportTemplate(
            name="chemistry_basic",
            display_name="化学实验基础模板",
            description="适用于无机化学、有机化学、分析化学实验",
            subjects=["chemistry"],
            sections=[
                ReportSection(name="experiment_purpose", title="一、实验目的"),
                ReportSection(name="experiment_principle", title="二、实验原理"),
                ReportSection(name="experiment_reagents", title="三、试剂与仪器"),
                ReportSection(name="experiment_steps", title="四、实验步骤"),
                ReportSection(name="data_observation", title="五、数据与观察"),
                ReportSection(name="calculation", title="六、计算"),
                ReportSection(name="error_analysis", title="七、误差分析"),
                ReportSection(name="conclusion", title="八、结论"),
            ]
        ),
        "biology_basic": ReportTemplate(
            name="biology_basic",
            display_name="生物实验基础模板",
            description="适用于生物学实验（细胞、生化、分子等）",
            subjects=["biology"],
            sections=[
                ReportSection(name="experiment_purpose", title="一、实验目的"),
                ReportSection(name="background", title="二、背景介绍"),
                ReportSection(name="materials", title="三、材料与方法"),
                ReportSection(name="results", title="四、实验结果"),
                ReportSection(name="analysis", title="五、分析讨论"),
                ReportSection(name="conclusion", title="六、结论"),
            ]
        ),
        "cs_algorithm": ReportTemplate(
            name="cs_algorithm",
            display_name="计算机算法实验模板",
            description="适用于数据结构、算法设计、机器学习实验",
            subjects=["computer_science"],
            sections=[
                ReportSection(name="problem_statement", title="一、问题描述"),
                ReportSection(name="algorithm_design", title="二、算法设计"),
                ReportSection(name="complexity", title="三、时间复杂度分析"),
                ReportSection(name="implementation", title="四、实现代码"),
                ReportSection(name="test_cases", title="五、测试用例"),
                ReportSection(name="results", title="六、实验结果"),
                ReportSection(name="discussion", title="七、讨论与优化"),
            ]
        ),
        "engineering_basic": ReportTemplate(
            name="engineering_basic",
            display_name="工程实验基础模板",
            description="适用于电路、材料、工程力学实验",
            subjects=["engineering"],
            sections=[
                ReportSection(name="experiment_objective", title="一、实验目的"),
                ReportSection(name="theoretical_basis", title="二、理论依据"),
                ReportSection(name="equipment_specs", title="三、设备规格"),
                ReportSection(name="experimental_procedure", title="四、实验程序"),
                ReportSection(name="data_analysis", title="五、数据分析"),
                ReportSection(name="performance_eval", title="六、性能评估"),
                ReportSection(name="conclusion", title="七、结论"),
            ]
        ),
    }
    
    def __init__(self, template_name: str = "physics_basic"):
        self.template_name = template_name
        self.template = self.TEMPLATE_REGISTRY.get(template_name, self.TEMPLATE_REGISTRY["physics_basic"])
        self.charts = []
        self.data_summary = {}
        
    def load_data(self, data_path: str) -> pd.DataFrame:
        """加载实验数据"""
        ext = Path(data_path).suffix.lower()
        if ext == '.csv':
            data = pd.read_csv(data_path)
        elif ext == '.xlsx':
            data = pd.read_excel(data_path)
        elif ext == '.json':
            data = pd.read_json(data_path)
        else:
            raise ValueError(f"不支持格式: {ext}")
        return data
    
    def add_chart(self, data: pd.DataFrame, x_col: str, y_col: str, 
                  config: ChartConfig = None, section: str = "data_processing") -> str:
        """添加图表到报告
        
        Args:
            data: DataFrame 数据
            x_col: X轴列名
            y_col: Y轴列名
            config: 图表配置
            section: 要绑定的章节
        
        Returns:
            chart_id: 图表标识符
        """
        chart_gen = ChartGenerator(data)
        result = chart_gen.generate(x_col, [y_col], config)
        chart_id = f"chart_{len(self.charts) + 1}"
        
        self.charts.append({
            "id": chart_id,
            "section": section,
            "image_base64": result["image_base64"],
            "save_path": result.get("save_path", ""),
            "config": config
        })
        return chart_id
    
    def summarize_data(self, data: pd.DataFrame) -> Dict[str, Any]:
        """生成数据摘要"""
        summary = {
            "shape": {"rows": len(data), "columns": len(data.columns)},
            "columns": [],
            "statistics": {}
        }
        
        for col in data.columns:
            col_data = data[col]
            if pd.api.types.is_numeric_dtype(col_data):
                summary["columns"].append({
                    "name": col,
                    "type": "numeric",
                    "null_count": int(col_data.isnull().sum()),
                    "mean": float(col_data.mean()) if not col_data.empty else None,
                    "std": float(col_data.std()) if not col_data.empty else None,
                    "min": float(col_data.min()) if not col_data.empty else None,
                    "max": float(col_data.max()) if not col_data.empty else None,
                })
                summary["statistics"][col] = {
                    "mean": float(col_data.mean()),
                    "std": float(col_data.std()),
                    "cv": float(col_data.std() / col_data.mean() * 100) if col_data.mean() != 0 else None
                }
            else:
                summary["columns"].append({
                    "name": col,
                    "type": "categorical",
                    "unique_count": int(col_data.nunique()),
                    "null_count": int(col_data.isnull().sum()),
                    "top_values": col_data.value_counts().head(5).to_dict()
                })
        
        self.data_summary = summary
        return summary
    
    def generate_report(self, title: str, author: str = "", group: str = "",
                       data: pd.DataFrame = None, **kwargs) -> str:
        """生成完整实验报告"""
        date = datetime.now().strftime("%Y-%m-%d")
        
        # 渲染章节
        sections_html = ""
        for section in self.template.sections:
            section_content = self._render_section(section, data, **kwargs)
            sections_html += f"""
            <section id="{section.name}">
                <h2>{section.title}</h2>
                {section_content}
            </section>
            """
        
        # 图表 HTML
        charts_html = ""
        for chart in self.charts:
            charts_html += f"""
            <figure id="{chart['id']}">
                <img src="{chart['image_base64']}" alt="{chart['config'].title if chart['config'] else '图表'}" />
                <figcaption>{chart['config'].title if chart['config'] else '实验图表'}</figcaption>
            </figure>
            """
        
        # 构建完整报告
        report = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - 实验报告</title>
    <style>
        body {{ 
            font-family: 'Microsoft YaHei', 'SimHei', sans-serif; 
            max-width: 800px; 
            margin: 0 auto; 
            padding: 20px;
            line-height: 1.6;
            color: #333;
        }}
        h1 {{ 
            text-align: center; 
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        .meta {{
            text-align: center;
            color: #666;
            margin-bottom: 30px;
        }}
        section {{ margin: 30px 0; }}
        h2 {{
            color: #2980b9;
            border-left: 4px solid #3498db;
            padding-left: 10px;
        }}
        figure {{
            text-align: center;
            margin: 20px 0;
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
        }}
        img {{ max-width: 100%; height: auto; }}
        figcaption {{
            color: #666;
            font-size: 0.9em;
            margin-top: 10px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 10px;
            text-align: center;
        }}
        th {{ background: #3498db; color: white; }}
        code {{
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Consolas', monospace;
        }}
        .data-table table {{
            width: 100%;
        }}
        .data-table th, .data-table td {{
            font-size: 0.9em;
        }}
        .stats {{
            background: #ecf0f1;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
        }}
    </style>
</head>
<body>
    <header>
        <h1>{title}</h1>
        <div class="meta">
            <p><strong>作者</strong>: {author or "匿名学生"} | 
               <strong>组别</strong>: {group or "未分配"} | 
               <strong>日期</strong>: {date}</p>
            <p><em>模板: {self.template.display_name}</em></p>
        </div>
    </header>
    
    <main>
        {sections_html}
    </main>
    
    <footer>
        <hr>
        <p style="text-align: center; color: #999;">
            报告生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | 
            Powered by <a href="https://github.com/KINGSTON-115/smart-lab-report">Smart Lab Report</a>
        </p>
    </footer>
</body>
</html>
        """
        return report
    
    def _render_section(self, section: ReportSection, data: pd.DataFrame = None, **kwargs) -> str:
        """渲染单个章节"""
        content = section.content or ""
        
        # 根据章节类型动态生成内容
        if section.name == "data_processing" and data is not None:
            if self.data_summary:
                content = self._render_data_summary()
        elif section.name == "conclusion":
            content = kwargs.get("conclusion", "*请根据实验结果填写结论...*")
        elif section.name == "error_analysis":
            content = kwargs.get("error_analysis", "*请分析实验误差来源...*")
        
        return content or f"<p>请在此处填写{section.title}内容...</p>"
    
    def _render_data_summary(self) -> str:
        """渲染数据摘要"""
        html = '<div class="data-table"><table><thead><tr><th>列名</th><th>类型</th><th>均值</th><th>标准差</th><th>变异系数(%)</th></tr></thead><tbody>'
        
        for col, stats in self.data_summary.get("statistics", {}).items():
            cv = stats.get("cv", 0)
            html += f"<tr><td>{col}</td><td>数值</td><td>{stats.get('mean', 'N/A'):.4f}</td><td>{stats.get('std', 'N/A'):.4f}</td><td>{cv:.2f}%</td></tr>"
        
        html += '</tbody></table></div>'
        
        # 统计摘要
        if self.data_summary.get("statistics"):
            html += '<div class="stats"><strong>统计摘要：</strong>'
            for col, stats in self.data_summary["statistics"].items():
                html += f'<br>{col}: 均值={stats["mean"]:.4f}, 标准差={stats["std"]:.4f}'
            html += '</div>'
        
        return html
    
    def save_report(self, report: str, output_path: str):
        """保存报告为 HTML"""
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path).write_text(report, encoding='utf-8')
        print(f"✅ 报告已保存: {output_path}")
        
        # 同时生成 Markdown 版本
        md_path = str(Path(output_path).with_suffix('.md'))
        self._save_markdown(report, md_path)
    
    def _save_markdown(self, html: str, md_path: str):
        """保存 Markdown 版本"""
        # 简单转换
        import re
        md = html
        md = re.sub(r'<h1[^>]*>(.*?)</h1>', r'# \1\n', md)
        md = re.sub(r'<h2[^>]*>(.*?)</h2>', r'## \1\n', md)
        md = re.sub(r'<section[^>]*>(.*?)</section>', r'\1', md, flags=re.DOTALL)
        md = re.sub(r'<[^>]+>', '', md)  # 移除剩余标签
        md = re.sub(r'&nbsp;', ' ', md)
        md = re.sub(r'\n{3,}', '\n\n', md)
        
        Path(md_path).write_text(md, encoding='utf-8')
        print(f"✅ Markdown 版本已保存: {md_path}")


# 便捷函数
def generate_physics_report(data_path: str, title: str, author: str = "", group: str = "",
                           output: str = "output/report.html") -> str:
    """快速生成物理实验报告"""
    generator = ReportGenerator("physics_basic")
    data = generator.load_data(data_path)
    generator.summarize_data(data)
    
    # 添加图表
    numeric_cols = data.select_dtypes(include=['number']).columns.tolist()
    if len(numeric_cols) >= 2:
        generator.add_chart(data, numeric_cols[0], numeric_cols[1], 
                          ChartConfig(title=f"{numeric_cols[0]} vs {numeric_cols[1]}", 
                                     chart_type="scatter"))
    
    report = generator.generate_report(title, author, group, data)
    generator.save_report(report, output)
    return report


if __name__ == "__main__":
    import sys
    
    # 测试
    data_path = "data/examples/欧姆定律数据.csv"
    output = generate_physics_report(
        data_path=data_path,
        title="欧姆定律验证实验",
        author="张三",
        group="物理1班第3组",
        output="output/欧姆定律实验报告.html"
    )
    print(f"报告生成成功！")
