# 🧪 PDF 生成器 - 支持输出 PDF 格式
# PDF Generator - Support PDF output

import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import tempfile

# 尝试导入依赖
try:
    from weasyprint import HTML, CSS
    WEASYPRINT_AVAILABLE = True
except ImportError:
    WEASYPRINT_AVAILABLE = False
    print("⚠️ WeasyPrint 不可用，将使用 html2pdf 方案")

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


@dataclass
class PDFConfig:
    """PDF 配置"""
    page_size: str = "A4"  # A4, Letter
    margin: float = 0.5  # 英寸
    title: str = ""
    author: str = ""
    font_family: str = "Helvetica"
    font_size: int = 10
    header_text: str = ""
    footer_text: str = ""


class PDFGenerator:
    """PDF 报告生成器"""
    
    SUPPORTED_ENGINES = ["weasyprint", "reportlab", "html"]
    
    def __init__(self, engine: str = "weasyprint"):
        self.engine = engine if engine in self.SUPPORTED_ENGINES else self._detect_engine()
        self.config = PDFConfig()
    
    def _detect_engine(self) -> str:
        """检测可用的引擎"""
        if WEASYPRINT_AVAILABLE:
            return "weasyprint"
        elif REPORTLAB_AVAILABLE:
            return "reportlab"
        else:
            return "html"  # 降级方案
    
    def set_config(self, config: PDFConfig):
        """设置配置"""
        self.config = config
    
    def html_to_pdf_weasyprint(self, html_content: str, output_path: str) -> str:
        """使用 WeasyPrint 生成 PDF"""
        if not WEASYPRINT_AVAILABLE:
            raise ImportError("WeasyPrint 不可用，请安装: pip install weasyprint")
        
        # 创建临时 HTML 文件
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', 
                                         delete=False, encoding='utf-8') as f:
            f.write(html_content)
            html_path = f.name
        
        try:
            # 生成 PDF
            html_doc = HTML(filename=html_path)
            html_doc.write_pdf(output_path)
            
            # 清理临时文件
            os.unlink(html_path)
            
            return output_path
        except Exception as e:
            # 清理临时文件
            if os.path.exists(html_path):
                os.unlink(html_path)
            raise e
    
    def html_to_pdf_reportlab(self, html_content: str, output_path: str) -> str:
        """使用 ReportLab 生成 PDF（从 HTML）"""
        if not REPORTLAB_AVAILABLE:
            raise ImportError("ReportLab 不可用，请安装: pip install reportlab")
        
        # 解析 HTML（简化版）
        from html.parser import HTMLParser
        
        class SimpleHTMLParser(HTMLParser):
            def __init__(self):
                super().__init__()
                self.elements = []
                self.styles = getSampleStyleSheet()
            
            def handle_starttag(self, tag, attrs):
                if tag == 'h1':
                    self.elements.append(Paragraph("TITLE", self.styles['Heading1']))
                elif tag == 'h2':
                    self.elements.append(Paragraph("SUBTITLE", self.styles['Heading2']))
                elif tag == 'p':
                    self.elements.append(Paragraph("TEXT", self.styles['Normal']))
                elif tag == 'br':
                    self.elements.append(Spacer(1, 12))
            
            def handle_data(self, data):
                if self.elements and hasattr(self.elements[-1], 'text'):
                    self.elements[-1].text += data.strip()
        
        parser = SimpleHTMLParser()
        parser.feed(html_content)
        
        # 创建 PDF
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        doc.build(parser.elements)
        
        return output_path
    
    def generate_from_html(self, html_content: str, output_path: str) -> str:
        """生成 PDF（自动选择引擎）"""
        output_path = str(output_path)
        
        if self.engine == "weasyprint":
            return self.html_to_pdf_weasyprint(html_content, output_path)
        elif self.engine == "reportlab":
            return self.html_to_pdf_reportlab(html_content, output_path)
        else:
            # 降级：使用浏览器打印
            return self._html_print_to_pdf(html_content, output_path)
    
    def _html_print_to_pdf(self, html_content: str, output_path: str) -> str:
        """降级方案：提示用户使用浏览器打印"""
        # 保存 HTML，提示用户打印
        html_path = output_path.replace('.pdf', '.html')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"⚠️ PDF 引擎不可用，已保存 HTML 文件: {html_path}")
        print("   请使用浏览器打开并打印为 PDF")
        
        return html_path


class DataValidator:
    """数据验证器 - 检查数据质量"""
    
    def __init__(self):
        self.warnings = []
        self.errors = []
        self.info = []
    
    def validate(self, data: 'pd.DataFrame') -> Dict:
        """验证数据"""
        self.warnings = []
        self.errors = []
        self.info = []
        
        if data is None or data.empty:
            self.errors.append("数据为空")
            return self._result()
        
        # 检查缺失值
        null_count = data.isnull().sum().sum()
        if null_count > 0:
            self.warnings.append(f"发现 {null_count} 个缺失值")
        
        # 检查重复行
        duplicates = data.duplicated().sum()
        if duplicates > 0:
            self.warnings.append(f"发现 {duplicates} 重复行")
        
        # 检查数据类型
        numeric_cols = data.select_dtypes(include=['number']).columns
        if len(numeric_cols) == 0:
            self.warnings.append("未发现数值列，可能影响图表生成")
        
        # 检查异常值（使用 IQR 方法）
        for col in numeric_cols:
            q1 = data[col].quantile(0.25)
            q3 = data[col].quantile(0.75)
            iqr = q3 - q1
            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr
            outliers = ((data[col] < lower) | (data[col] > upper)).sum()
            if outliers > 0:
                self.warnings.append(f"列 '{col}' 发现 {outliers} 个潜在异常值")
        
        # 检查数据量
        if len(data) < 5:
            self.warnings.append("数据点较少（< 5），可能影响统计分析")
        elif len(data) > 1000:
            self.info.append("数据量较大，可能影响处理速度")
        
        # 检查方差
        for col in numeric_cols:
            if data[col].std() == 0:
                self.errors.append(f"列 '{col}' 的标准差为 0，数据无变化")
        
        return self._result()
    
    def _result(self) -> Dict:
        """返回结果"""
        return {
            "valid": len(self.errors) == 0,
            "warnings": self.warnings,
            "errors": self.errors,
            "info": self.info,
            "summary": self._generate_summary()
        }
    
    def _generate_summary(self) -> str:
        """生成摘要"""
        lines = []
        if self.warnings:
            lines.append(f"⚠️ 警告 ({len(self.warnings)} 项):")
            for w in self.warnings[:3]:
                lines.append(f"   - {w}")
        if self.errors:
            lines.append(f"❌ 错误 ({len(self.errors)} 项):")
            for e in self.errors[:3]:
                lines.append(f"   - {e}")
        if self.info:
            lines.append(f"ℹ️ 提示 ({len(self.info)} 项):")
            for i in self.info[:3]:
                lines.append(f"   - {i}")
        
        if not lines:
            lines.append("✅ 数据验证通过，未发现问题")
        
        return "\n".join(lines)
    
    def get_report(self) -> str:
        """获取验证报告"""
        return self._generate_summary()


class ExperimentTemplateLibrary:
    """实验模板库 - 内置模板集合"""
    
    TEMPLATES = {
        # 物理实验
        "physics_ohms_law": {
            "name": "欧姆定律验证实验",
            "category": "物理",
            "variables": ["title", "author", "group", "date", "purpose", "principle", 
                         "apparatus", "steps", "conclusion", "error_analysis"],
            "description": "适用于电路实验，验证欧姆定律 V=IR"
        },
        "physics_pendulum": {
            "name": "单摆实验",
            "category": "物理",
            "variables": ["title", "author", "group", "date", "purpose", "principle",
                         "apparatus", "steps", "conclusion", "error_analysis"],
            "description": "测量重力加速度的单摆实验"
        },
        "physics_optics": {
            "name": "光学实验",
            "category": "物理",
            "variables": ["title", "author", "group", "date", "purpose", "principle",
                         "apparatus", "steps", "conclusion", "error_analysis"],
            "description": "适用于折射、反射、干涉等光学实验"
        },
        
        # 化学实验
        "chemistry_titration": {
            "name": "滴定分析实验",
            "category": "化学",
            "variables": ["title", "author", "group", "date", "purpose", "principle",
                         "reagents", "steps", "calculation", "conclusion"],
            "description": "酸碱滴定、氧化还原滴定等"
        },
        "chemistry_synthesis": {
            "name": "合成实验",
            "category": "化学",
            "variables": ["title", "author", "group", "date", "purpose", "principle",
                         "materials", "steps", "yield", "purity", "conclusion"],
            "description": "有机合成、无机合成实验"
        },
        
        # 生物实验
        "biology_microscopy": {
            "name": "显微镜观察实验",
            "category": "生物",
            "variables": ["title", "author", "group", "date", "purpose", "principle",
                         "materials", "observations", "images", "conclusion"],
            "description": "细胞、组织观察实验"
        },
        "biology_pcr": {
            "name": "PCR 实验",
            "category": "生物",
            "variables": ["title", "author", "group", "date", "purpose", "principle",
                         "materials", "steps", "results", "analysis", "conclusion"],
            "description": "聚合酶链式反应实验"
        },
        
        # 计算机实验
        "cs_sorting": {
            "name": "排序算法实验",
            "category": "计算机",
            "variables": ["title", "author", "group", "date", "problem", "algorithm",
                         "complexity", "code", "test_cases", "results"],
            "description": "排序算法实现与比较"
        },
        "cs_ml": {
            "name": "机器学习实验",
            "category": "计算机",
            "variables": ["title", "author", "group", "date", "problem", "dataset",
                         "model", "features", "metrics", "results", "discussion"],
            "description": "机器学习模型训练与评估"
        },
        
        # 工程实验
        "engineering_circuit": {
            "name": "电路实验",
            "category": "工程",
            "variables": ["title", "author", "group", "date", "objective", "theory",
                         "equipment", "procedure", "measurements", "analysis"],
            "description": "电路设计与测试实验"
        },
        "engineering_material": {
            "name": "材料力学实验",
            "category": "工程",
            "variables": ["title", "author", "group", "date", "objective", "theory",
                         "specimens", "procedure", "data", "stress_strain", "conclusion"],
            "description": "材料强度、硬度测试实验"
        }
    }
    
    def get_template(self, template_id: str) -> Dict:
        """获取模板"""
        return self.TEMPLATES.get(template_id)
    
    def list_templates(self, category: str = None) -> List[Dict]:
        """列出模板"""
        templates = []
        for tid, t in self.TEMPLATES.items():
            if category is None or t["category"] == category:
                templates.append({
                    "id": tid,
                    "name": t["name"],
                    "category": t["category"],
                    "description": t["description"]
                })
        return templates
    
    def generate_template_content(self, template_id: str, data: Dict) -> str:
        """生成模板内容"""
        template = self.get_template(template_id)
        if not template:
            return ""
        
        # 生成 Markdown 模板
        content = f"# {data.get('title', template['name'])}\n\n"
        content += f"**作者**: {data.get('author', '{{author}}')}\n"
        content += f"**组别**: {data.get('group', '{{group}}')}\n"
        content += f"**日期**: {data.get('date', '{{date}}')}\n\n"
        
        content += "---\n\n"
        
        for var in template["variables"]:
            if var in ["purpose", "principle", "steps", "conclusion", "error_analysis"]:
                section_map = {
                    "purpose": "## 一、实验目的",
                    "principle": "## 二、实验原理",
                    "steps": "## 三、实验步骤",
                    "conclusion": "## 四、实验结论",
                    "error_analysis": "## 五、误差分析"
                }
                content += f"{section_map.get(var, f'## {var}')}\n\n"
                content += f"{{{{{var}}}}}\n\n"
        
        return content


# 便捷函数
def validate_data(data_path: str) -> Dict:
    """验证数据文件"""
    import pandas as pd
    
    ext = Path(data_path).suffix.lower()
    if ext == '.csv':
        data = pd.read_csv(data_path)
    elif ext == '.xlsx':
        data = pd.read_excel(data_path)
    else:
        raise ValueError(f"不支持格式: {ext}")
    
    validator = DataValidator()
    return validator.validate(data)


def quick_pdf(html_path: str, output: str = None) -> str:
    """快速生成 PDF"""
    if output is None:
        output = str(Path(html_path).with_suffix('.pdf'))
    
    generator = PDFGenerator()
    generator.generate_from_html(Path(html_path).read_text(encoding='utf-8'), output)
    
    return output


if __name__ == "__main__":
    import pandas as pd
    
    # 测试数据验证
    print("=== 数据验证测试 ===")
    data = pd.DataFrame({
        'x': [1, 2, 3, 4, 5, 1000],  # 1000 是异常值
        'y': [2, 4, 5, 4, 5, 6]
    })
    
    validator = DataValidator()
    result = validator.validate(data)
    
    print(result["summary"])
    
    # 列出模板
    print("\n=== 实验模板库 ===")
    lib = ExperimentTemplateLibrary()
    templates = lib.list_templates("物理")
    for t in templates:
        print(f"  - {t['name']} ({t['id']})")
