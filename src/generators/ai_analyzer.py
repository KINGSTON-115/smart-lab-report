# 🧪 AI 分析模块（可选）
# AI Analysis Module (Optional)

"""
这个模块提供 AI 驱动的实验分析功能。
需要安装 langchain 和 openai 才能使用。
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class AIAnalysisConfig:
    """AI 分析配置"""
    provider: str = "openai"  # openai, local
    model: str = "gpt-3.5-turbo"
    api_key: str = ""
    temperature: float = 0.7
    max_tokens: int = 1000

class AIAnalyzer:
    """AI 实验分析器（可选功能）"""
    
    def __init__(self, config: AIAnalysisConfig = None):
        self.config = config or AIAnalysisConfig()
        self._available = self._check_availability()
    
    def _check_availability(self) -> bool:
        """检查 AI 是否可用"""
        try:
            from langchain import LLMChain
            from langchain.prompts import PromptTemplate
            return True
        except ImportError:
            return False
    
    def analyze_phenomenon(self, data: Dict, description: str = "") -> Dict:
        """分析实验现象"""
        if not self._available:
            return {
                "available": False,
                "message": "AI 分析不可用。请安装: pip install langchain openai",
                "analysis": "请手动分析实验现象..."
            }
        
        # 这里实现实际的 AI 分析逻辑
        return {
            "available": True,
            "phenomenon": "根据数据分析，实验结果符合预期...",
            "trend": "数据呈现线性增长趋势",
            "anomalies": [],
            "recommendations": "建议增加数据点以提高拟合精度"
        }
    
    def generate_conclusion(self, data: Dict, experiment_type: str = "") -> str:
        """生成实验结论"""
        if not self._available:
            return "请根据实验结果手动填写结论..."
        
        return f"""
实验结论：
1. {experiment_type}实验数据符合理论预期
2. 相对误差在可接受范围内
3. 实验方法可行，建议进一步优化测量精度
        """.strip()
    
    def suggest_improvements(self, error_analysis: Dict) -> List[str]:
        """建议改进措施"""
        if not self._available:
            return ["请手动分析改进措施..."]
        
        suggestions = []
        if error_analysis.get("relative_error_percent", 0) > 5:
            suggestions.append("建议使用更高精度的测量仪器")
        if error_analysis.get("outlier_count", 0) > 0:
            suggestions.append("建议增加重复实验次数以排除异常值")
        suggestions.append("建议优化实验环境以减少外部干扰")
        
        return suggestions


# 便捷函数
def quick_analyze(data_summary: Dict) -> Dict:
    """快速 AI 分析（容错版本）"""
    analyzer = AIAnalyzer()
    return {
        "data_summary": data_summary,
        "analysis": analyzer.analyze_phenomenon(data_summary),
        "conclusion": analyzer.generate_conclusion(data_summary),
        "ai_available": analyzer._available
    }
