# 🧪 Smart Lab Report - 主包
# Smart Lab Report - Main Package

__version__ = "1.0.0"
__author__ = "KINGSTON-115"

from .core.engine import LabReportGenerator, ReportConfig, ExperimentData
from .generators.report_generator import ReportGenerator, ReportTemplate
from .generators.chart_generator import ChartGenerator, ChartConfig

__all__ = [
    "LabReportGenerator",
    "ReportConfig", 
    "ExperimentData",
    "ReportGenerator",
    "ReportTemplate",
    "ChartGenerator",
    "ChartConfig",
]
