# 🧪 批量报告生成器 - 支持批量处理
# Batch Report Generator - Support batch processing

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
import time

from .report_generator import ReportGenerator
from .word_generator import WordReportGenerator
from .pdf_generator import PDFGenerator, DataValidator
from .ai_engine import AILabAnalyzer


@dataclass
class BatchTask:
    """批量任务"""
    data_path: str
    title: str
    author: str = ""
    group: str = ""
    template: str = "physics_basic"
    output_format: str = "all"  # docx, html, pdf, all
    ai_analysis: bool = False
    ai_config: Dict = field(default_factory=dict)


@dataclass
class BatchResult:
    """批量处理结果"""
    task: BatchTask
    success: bool
    output_files: List[str] = field(default_factory=list)
    error: str = ""
    duration: float = 0.0


class BatchReportGenerator:
    """批量报告生成器"""
    
    def __init__(self, output_dir: str = "output/batch"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.results: List[BatchResult] = []
        self.validator = DataValidator()
    
    def load_tasks_from_csv(self, csv_path: str) -> List[BatchTask]:
        """从 CSV 加载批量任务"""
        df = pd.read_csv(csv_path)
        
        tasks = []
        for _, row in df.iterrows():
            task = BatchTask(
                data_path=row.get('data_path', ''),
                title=row.get('title', ''),
                author=row.get('author', ''),
                group=row.get('group', ''),
                template=row.get('template', 'physics_basic'),
                ai_analysis=row.get('ai_analysis', False)
            )
            tasks.append(task)
        
        return tasks
    
    def load_tasks_from_json(self, json_path: str) -> List[BatchTask]:
        """从 JSON 加载批量任务"""
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        tasks = []
        for item in data:
            task = BatchTask(
                data_path=item['data_path'],
                title=item['title'],
                author=item.get('author', ''),
                group=item.get('group', ''),
                template=item.get('template', 'physics_basic'),
                ai_analysis=item.get('ai_analysis', False)
            )
            tasks.append(task)
        
        return tasks
    
    def process_single_task(self, task: BatchTask) -> BatchResult:
        """处理单个任务"""
        start_time = time.time()
        result = BatchResult(task=task, success=False)
        
        try:
            # 验证数据
            validation = self.validator.validate(
                pd.read_csv(task.data_path) if task.data_path.endswith('.csv') 
                else pd.read_excel(task.data_path)
            )
            
            if not validation["valid"]:
                result.error = f"数据验证失败: {', '.join(validation['errors'])}"
                return result
            
            # 加载数据
            data = pd.read_csv(task.data_path) if task.data_path.endswith('.csv') \
                else pd.read_excel(task.data_path)
            
            # AI 分析（如果启用）
            ai_content = {}
            if task.ai_analysis:
                analyzer = AILabAnalyzer()
                if analyzer._available:
                    ai_result = analyzer.analyze_phenomenon(data, task.title)
                    ai_content = {
                        "conclusion": ai_result.conclusion,
                        "phenomenon": ai_result.phenomenon,
                        "suggestion": ai_result.suggestion
                    }
            
            # 生成 Word
            if task.output_format in ['docx', 'all']:
                word_gen = WordReportGenerator(task.template)
                doc = word_gen.generate_report(
                    title=task.title,
                    author=task.author,
                    group=task.group,
                    conclusion=ai_content.get("conclusion", "请填写结论..."),
                    data_summary={}
                )
                output_path = self.output_dir / f"{task.title}.docx"
                word_gen.save(str(output_path))
                result.output_files.append(str(output_path))
            
            # 生成 HTML
            if task.output_format in ['html', 'all']:
                gen = ReportGenerator(task.template)
                gen.summarize_data(data)
                report = gen.generate_report(task.title, task.author, task.group, data)
                output_path = self.output_dir / f"{task.title}.html"
                gen.save_report(report, str(output_path))
                result.output_files.append(str(output_path))
            
            result.success = True
            
        except Exception as e:
            result.error = str(e)
        
        result.duration = time.time() - start_time
        return result
    
    def process_batch(self, tasks: List[BatchTask], parallel: bool = False, 
                     max_workers: int = 4) -> List[BatchResult]:
        """批量处理任务"""
        self.results = []
        
        if parallel:
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = {executor.submit(self.process_single_task, t): t for t in tasks}
                for future in as_completed(futures):
                    result = future.result()
                    self.results.append(result)
                    print(f"  {'✅' if result.success else '❌'} {result.task.title} ({result.duration:.2f}s)")
        else:
            for task in tasks:
                print(f"  处理: {task.title}...")
                result = self.process_single_task(task)
                self.results.append(result)
                print(f"  {'✅' if result.success else '❌'} {result.task.title} ({result.duration:.2f}s)")
                if not result.success:
                    print(f"     错误: {result.error}")
        
        return self.results
    
    def generate_report(self) -> Dict:
        """生成处理报告"""
        total = len(self.results)
        success = sum(1 for r in self.results if r.success)
        failed = total - success
        total_time = sum(r.duration for r in self.results)
        
        report = {
            "summary": {
                "total": total,
                "success": success,
                "failed": failed,
                "total_time": f"{total_time:.2f}s",
                "avg_time": f"{total_time/total:.2f}s" if total > 0 else "0s"
            },
            "failed_tasks": [
                {"title": r.task.title, "error": r.error}
                for r in self.results if not r.success
            ]
        }
        
        return report


class ReportPreview:
    """报告预览生成器"""
    
    def __init__(self):
        self.templates = {
            "physics_basic": {
                "sections": ["实验目的", "实验原理", "实验仪器", "实验步骤", 
                            "数据处理", "误差分析", "结论与讨论"],
                "colors": {"primary": "#3498db", "secondary": "#2c3e50"}
            },
            "chemistry_basic": {
                "sections": ["实验目的", "实验原理", "试剂与仪器", "实验步骤",
                            "数据与观察", "计算", "误差分析", "结论"],
                "colors": {"primary": "#27ae60", "secondary": "#2c3e50"}
            },
            "biology_basic": {
                "sections": ["实验目的", "背景介绍", "材料与方法", 
                            "实验结果", "分析讨论", "结论"],
                "colors": {"primary": "#9b59b6", "secondary": "#2c3e50"}
            },
            "cs_algorithm": {
                "sections": ["问题描述", "算法设计", "时间复杂度分析", 
                            "实现代码", "测试用例", "实验结果", "讨论与优化"],
                "colors": {"primary": "#e74c3c", "secondary": "#2c3e50"}
            }
        }
    
    def generate_preview_html(self, template: str, data_info: Dict) -> str:
        """生成预览 HTML"""
        tmpl = self.templates.get(template, self.templates["physics_basic"])
        colors = tmpl["colors"]
        
        sections_html = ""
        for i, section in enumerate(tmpl["sections"]):
            sections_html += f"""
            <div class="section">
                <div class="section-number">{i+1}</div>
                <div class="section-title">{section}</div>
                <div class="section-placeholder">💡 点击编辑此部分内容</div>
            </div>
            """
        
        html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>报告预览 - {template}</title>
    <style>
        body {{
            font-family: 'Microsoft YaHei', sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .preview-container {{
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 40px;
        }}
        .header {{
            text-align: center;
            border-bottom: 3px solid {colors['primary']};
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            color: {colors['secondary']};
            margin: 0 0 10px 0;
        }}
        .meta {{
            color: #666;
            font-size: 14px;
        }}
        .section {{
            display: flex;
            align-items: center;
            padding: 15px;
            margin: 10px 0;
            background: #f8f9fa;
            border-radius: 6px;
            border-left: 4px solid {colors['primary']};
        }}
        .section-number {{
            background: {colors['primary']};
            color: white;
            width: 30 px;
            height: 30px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            margin-right: 15px;
        }}
        .section-title {{
            font-weight: bold;
            color: {colors['secondary']};
            flex: 1;
        }}
        .section-placeholder {{
            color: #999;
            font-size: 12px;
        }}
        .data-info {{
            background: #e8f4fd;
            padding: 15px;
            border-radius: 6px;
            margin-bottom: 20px;
        }}
        .data-info h3 {{
            margin: 0 0 10px 0;
            color: {colors['primary']};
        }}
        .chart-preview {{
            text-align: center;
            padding: 40px;
            background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%);
            border-radius: 6px;
            margin: 20px 0;
        }}
        .chart-placeholder {{
            color: #999;
            font-size: 14px;
        }}
        .status-badge {{
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 12px;
            margin: 5px;
        }}
        .status-ok {{ background: #d4edda; color: #155724; }}
        .status-warn {{ background: #fff3cd; color: #856404; }}
        .status-error {{ background: #f8d7da; color: #721c24; }}
    </style>
</head>
<body>
    <div class="preview-container">
        <div class="header">
            <h1>📄 报告预览</h1>
            <div class="meta">
                <span>模板: {template}</span> | 
                <span>章节数: {len(tmpl['sections'])}</span>
            </div>
        </div>
        
        <div class="data-info">
            <h3>📊 数据信息</h3>
            <p>数据行数: {data_info.get('rows', 'N/A')}</p>
            <p>数据列数: {data_info.get('columns', 'N/A')}</p>
            <p>数值列: {data_info.get('numeric_cols', 'N/A')}</p>
        </div>
        
        <div class="chart-preview">
            <div class="chart-placeholder">
                📈 图表预览区域<br>
                (运行报告生成后将显示实际图表)
            </div>
        </div>
        
        <h3>📑 报告章节</h3>
        {sections_html}
        
        <div style="text-align: center; margin-top: 30px;">
            <span class="status-badge status-ok">✅ 数据验证通过</span>
            <span class="status-badge status-warn">⚠️ 建议添加图表</span>
            <span class="status-badge status-ok">🎯 模板兼容</span>
        </div>
    </div>
</body>
</html>
        """
        return html
    
    def save_preview(self, html: str, output_path: str):
        """保存预览"""
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path).write_text(html, encoding='utf-8')
        print(f"✅ 预览已保存: {output_path}")


# 便捷函数
def batch_process(config_path: str, output_dir: str = "output/batch") -> Dict:
    """批量处理"""
    generator = BatchReportGenerator(output_dir)
    
    if config_path.endswith('.csv'):
        tasks = generator.load_tasks_from_csv(config_path)
    else:
        tasks = generator.load_tasks_from_json(config_path)
    
    print(f"🚀 开始批量处理 {len(tasks)} 个任务...")
    results = generator.process_batch(tasks)
    report = generator.generate_report()
    
    print(f"\n📊 处理完成:")
    print(f"   总数: {report['summary']['total']}")
    print(f"   成功: {report['summary']['success']}")
    print(f"   失败: {report['summary']['failed']}")
    print(f"   用时: {report['summary']['total_time']}")
    
    return report


def preview_report(template: str, data_info: Dict, output: str = "output/preview.html"):
    """生成报告预览"""
    preview = ReportPreview()
    html = preview.generate_preview_html(template, data_info)
    preview.save_preview(html, output)
    return output


if __name__ == "__main__":
    # 测试批量处理
    print("=== 批量处理测试 ===")
    
    # 创建测试任务
    tasks = [
        BatchTask(
            data_path="data/examples/欧姆定律数据.csv",
            title="欧姆定律验证实验",
            author="张三",
            group="物理1班"
        ),
        BatchTask(
            data_path="data/examples/欧姆定律数据.csv",
            title="第二次实验",
            author="李四",
            group="物理2班"
        )
    ]
    
    generator = BatchReportGenerator()
    results = generator.process_batch(tasks)
    
    print("\n=== 报告预览 ===")
    preview = ReportPreview()
    html = preview.generate_preview_html("physics_basic", {"rows": 10, "columns": 3, "numeric_cols": 2})
    preview.save_preview(html, "output/report_preview.html")
