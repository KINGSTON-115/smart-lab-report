# 🧪 Smart Lab Report - 主包
# Smart Lab Report - Main Package

__version__ = "1.0.0"
__author__ = "KINGSTON-115"

from .core.engine import LabReportGenerator, ReportConfig, ExperimentData
from .generators.report_generator import ReportGenerator, ReportTemplate
from .generators.chart_generator import ChartGenerator, ChartConfig
from .generators.word_generator import WordReportGenerator
from .generators.template_engine import TemplateEngine, UserTemplate
from .generators.ai_engine import AILabAnalyzer, AIConfig, AnalysisResult
from .generators.pdf_generator import PDFGenerator, PDFConfig, DataValidator
from .generators.batch_processor import BatchReportGenerator, BatchTask, ReportPreview

__all__ = [
    # Core
    "LabReportGenerator",
    "ReportConfig",
    "ExperimentData",
    # Generators
    "ReportGenerator",
    "ReportTemplate",
    "ChartGenerator",
    "ChartConfig",
    "WordReportGenerator",
    # Template & AI
    "TemplateEngine",
    "UserTemplate",
    "AILabAnalyzer",
    "AIConfig",
    "AnalysisResult",
    # PDF & Batch
    "PDFGenerator",
    "PDFConfig",
    "DataValidator",
    "BatchReportGenerator",
    "BatchTask",
    "ReportPreview",
]
