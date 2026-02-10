# 🧪 PDF 生成器 - 支持输出 PDF 格式
# PDF Generator - Support PDF output

import os
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import tempfile

# PDF 生成可选依赖（延迟导入，避免启动时失败）
WEASYPRINT_AVAILABLE = False
REPORTLAB_AVAILABLE = False

def _check_dependencies():
    """检查 PDF 依赖是否可用"""
    global WEASYPRINT_AVAILABLE, REPORTLAB_AVAILABLE
    
    # 检查 WeasyPrint
    try:
        from weasyprint import HTML, CSS
        WEASYPRINT_AVAILABLE = True
    except (ImportError, OSError):
        WEASYPRINT_AVAILABLE = False
    
    # 检查 ReportLab
    try:
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.lib import colors
        REPORTLAB_AVAILABLE = True
    except ImportError:
        REPORTLAB_AVAILABLE = False

# 启动时检查依赖
_check_dependencies()

@dataclass
class PDFConfig:
    """PDF 配置"""
    page_size: str = "A4"
    margin: float = 0.5
    title: str = ""
    author: str = ""
    font_family: str = "Helvetica"
    font_size: int = 10


class PDFGenerator:
    """PDF 报告生成器"""
    
    SUPPORTED_ENGINES = ["weasyprint", "reportlab", "html"]
    
    def __init__(self, engine: str = "reportlab"):
        self.engine = self._detect_engine()
        self.config = PDFConfig()
    
    def _detect_engine(self) -> str:
        """检测可用的引擎"""
        _check_dependencies()
        if WEASYPRINT_AVAILABLE:
            return "weasyprint"
        elif REPORTLAB_AVAILABLE:
            return "reportlab"
        else:
            return "html"
    
    def set_config(self, config: PDFConfig):
        self.config = config
    
    def generate_from_html(self, html_content: str, output_path: str) -> str:
        """生成 PDF（自动选择引擎）"""
        output_path = str(output_path)
        
        # WeasyPrint
        if self.engine == "weasyprint" and WEASYPRINT_AVAILABLE:
            return self._html_to_pdf_weasyprint(html_content, output_path)
        # ReportLab
        elif self.engine == "reportlab" and REPORTLAB_AVAILABLE:
            return self._html_to_pdf_reportlab(html_content, output_path)
        # 降级
        else:
            return self._html_print_to_pdf(html_content, output_path)
    
    def _html_to_pdf_weasyprint(self, html_content: str, output_path: str) -> str:
        """使用 WeasyPrint 生成 PDF"""
        if not WEASYPRINT_AVAILABLE:
            raise ImportError("WeasyPrint 不可用")
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
            f.write(html_content)
            html_path = f.name
        
        try:
            from weasyprint import HTML
            html_doc = HTML(filename=html_path)
            html_doc.write_pdf(output_path)
            os.unlink(html_path)
            return output_path
        except Exception as e:
            if os.path.exists(html_path):
                os.unlink(html_path)
            raise e
    
    def _html_to_pdf_reportlab(self, html_content: str, output_path: str) -> str:
        """使用 ReportLab 生成 PDF"""
        if not REPORTLAB_AVAILABLE:
            raise ImportError("ReportLab 不可用")
        
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        styles = getSampleStyleSheet()
        
        story = [
            Paragraph(html_content[:100] + "...", styles['Normal']),
            Spacer(1, 12)
        ]
        
        doc.build(story)
        return output_path
    
    def _html_print_to_pdf(self, html_content: str, output_path: str) -> str:
        """降级方案：保存 HTML"""
        html_path = output_path.replace('.pdf', '.html')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"⚠️ PDF 引擎不可用，已保存 HTML: {html_path}")
        return html_path


class DataValidator:
    """数据验证器"""
    
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
        
        # 检查数值列
        numeric_cols = data.select_dtypes(include=['number']).columns
        if len(numeric_cols) == 0:
            self.warnings.append("未发现数值列，可能影响图表生成")
        
        # 检查异常值
        for col in numeric_cols:
            q1 = data[col].quantile(0.25)
            q3 = data[col].quantile(0.75)
            iqr = q3 - q1
            lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
            outliers = ((data[col] < lower) | (data[col] > upper)).sum()
            if outliers > 0:
                self.warnings.append(f"列 '{col}' 发现 {outliers} 个潜在异常值")
        
        return self._result()
    
    def _result(self) -> Dict:
        return {
            "valid": len(self.errors) == 0,
            "warnings": self.warnings,
            "errors": self.errors,
            "info": self.info
        }


# 便捷函数
def validate_data(data_path: str) -> Dict:
    """验证数据文件"""
    ext = Path(data_path).suffix.lower()
    if ext == '.csv':
        data = pd.read_csv(data_path)
    elif ext == '.xlsx':
        data = pd.read_excel(data_path)
    else:
        raise ValueError(f"不支持格式: {ext}")
    
    validator = DataValidator()
    return validator.validate(data)
