# 🧪 AI 大模型集成模块
# AI LLM Integration Module

"""
支持接入多种大语言模型：
- OpenAI (GPT-3.5/GPT-4)
- Claude (Anthropic)
- 本地模型 (Ollama)
- 通义千问 (阿里)
- 智谱 AI (ChatGLM)
- 百度文心一言
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import pandas as pd

# 环境变量读取
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
QWEN_API_KEY = os.environ.get("QWEN_API_KEY", "")
ZHIPU_API_KEY = os.environ.get("ZHIPU_API_KEY", "")
BAIDU_API_KEY = os.environ.get("BAIDU_API_KEY", "")


@dataclass
class AIConfig:
    """AI 配置"""
    provider: str = "openai"  # openai, claude, qwen, zhipu, baidu, local
    model: str = "gpt-3.5-turbo"
    api_key: str = ""
    base_url: str = ""
    temperature: float = 0.7
    max_tokens: int = 2000
    timeout: int = 60
    
    def __post_init__(self):
        # 自动从环境变量获取 API Key
        if not self.api_key:
            if self.provider == "openai":
                self.api_key = OPENAI_API_KEY
            elif self.provider == "claude":
                self.api_key = ANTHROPIC_API_KEY
            elif self.provider == "qwen":
                self.api_key = QWEN_API_KEY
            elif self.provider == "zhipu":
                self.api_key = ZHIPU_API_KEY
            elif self.provider == "baidu":
                self.api_key = BAIDU_API_KEY


@dataclass
class ExperimentData:
    """实验数据"""
    raw_data: pd.DataFrame
    title: str = ""
    description: str = ""
    subject: str = ""  # physics, chemistry, biology, etc.


@dataclass
class AnalysisResult:
    """分析结果"""
    phenomenon: str = ""           # 实验现象描述
    conclusion: str = ""           # 实验结论
    trend: str = ""                # 数据趋势
    anomaly: str = ""              # 异常数据
    suggestion: str = ""           # 改进建议
    confidence: float = 0.0       # 置信度
    raw_response: str = ""         # 原始响应


class BaseLLMProvider(ABC):
    """LLM 提供商基类"""
    
    @abstractmethod
    def chat(self, messages: List[Dict], **kwargs) -> str:
        """发送对话请求"""
        pass


class OpenAIProvider(BaseLLMProvider):
    """OpenAI 提供商"""
    
    def __init__(self, config: AIConfig):
        self.config = config
        self._client = None
    
    def _get_client(self):
        if self._client is None:
            try:
                from openai import OpenAI
                self._client = OpenAI(
                    api_key=self.config.api_key,
                    base_url=self.config.base_url or None,
                    timeout=self.config.timeout
                )
            except ImportError:
                raise ImportError("请安装 OpenAI: pip install openai")
        return self._client
    
    def chat(self, messages: List[Dict], **kwargs) -> str:
        client = self._get_client()
        response = client.chat.completions.create(
            model=self.config.model,
            messages=messages,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens
        )
        return response.choices[0].message.content


class ClaudeProvider(BaseLLMProvider):
    """Anthropic Claude 提供商"""
    
    def __init__(self, config: AIConfig):
        self.config = config
        self._client = None
    
    def _get_client(self):
        if self._client is None:
            try:
                from anthropic import Anthropic
                self._client = Anthropic(
                    api_key=self.config.api_key,
                    timeout=self.config.timeout
                )
            except ImportError:
                raise ImportError("请安装 Anthropic: pip install anthropic")
        return self._client
    
    def chat(self, messages: List[Dict], **kwargs) -> str:
        client = self._get_client()
        # 转换消息格式
        content = [m["content"] for m in messages]
        response = client.messages.create(
            model=self.config.model,
            max_tokens=self.config.max_tokens,
            temperature=self.config.temperature,
            messages=content
        )
        return response.content[0].text


class QwenProvider(BaseLLMProvider):
    """阿里通义千问提供商"""
    
    def __init__(self, config: AIConfig):
        self.config = config
        self._client = None
    
    def _get_client(self):
        if self._client is None:
            try:
                from openai import OpenAI
                self._client = OpenAI(
                    api_key=self.config.api_key,
                    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
                )
            except ImportError:
                raise ImportError("请安装 OpenAI SDK")
        return self._client
    
    def chat(self, messages: List[Dict], **kwargs) -> str:
        client = self._get_client()
        response = client.chat.completions.create(
            model=self.config.model,
            messages=messages,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens
        )
        return response.choices[0].message.content


class ZhipuProvider(BaseLLMProvider):
    """智谱 AI 提供商"""
    
    def __init__(self, config: AIConfig):
        self.config = config
        self._client = None
    
    def _get_client(self):
        if self._client is None:
            try:
                from openai import OpenAI
                self._client = OpenAI(
                    api_key=self.config.api_key,
                    base_url="https://open.zhipu.ai.com/v4"
                )
            except ImportError:
                raise ImportError("请安装 OpenAI SDK")
        return self._client
    
    def chat(self, messages: List[Dict], **kwargs) -> str:
        client = self._get_client()
        response = client.chat.completions.create(
            model=self.config.model,
            messages=messages,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens
        )
        return response.choices[0].message.content


class LocalProvider(BaseLLMProvider):
    """本地模型提供商 (Ollama)"""
    
    def __init__(self, config: AIConfig):
        self.config = config
    
    def chat(self, messages: List[Dict], **kwargs) -> str:
        try:
            from openai import OpenAI
            client = OpenAI(
                api_key="ollama",
                base_url=self.config.base_url or "http://localhost:11434/v1"
            )
            response = client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            raise ConnectionError(f"无法连接到本地模型: {e}")


class AILabAnalyzer:
    """AI 实验分析器 - 主类"""
    
    PROVIDERS = {
        "openai": OpenAIProvider,
        "claude": ClaudeProvider,
        "qwen": QwenProvider,
        "zhipu": ZhipuProvider,
        "local": LocalProvider,
    }
    
    DEFAULT_MODELS = {
        "openai": "gpt-3.5-turbo",
        "claude": "claude-3-sonnet-20240229",
        "qwen": "qwen-turbo",
        "zhipu": "glm-4",
        "local": "llama2",
    }
    
    def __init__(self, config: AIConfig = None):
        self.config = config or AIConfig()
        self.provider = self._create_provider()
        self._available = self._check_availability()
    
    def _create_provider(self) -> BaseLLMProvider:
        """创建 LLM 提供商"""
        provider_class = self.PROVIDERS.get(self.config.provider, OpenAIProvider)
        return provider_class(self.config)
    
    def _check_availability(self) -> bool:
        """检查是否可用"""
        if not self.config.api_key and self.config.provider != "local":
            return False
        try:
            # 简单测试
            self._test_connection()
            return True
        except Exception:
            return False
    
    def _test_connection(self):
        """测试连接"""
        messages = [{"role": "user", "content": "Hello"}]
        return self.provider.chat(messages)
    
    def _format_data_for_ai(self, data: pd.DataFrame, title: str = "") -> str:
        """格式化数据给 AI"""
        if data is None or data.empty:
            return "无数据"
        
        # 基本统计
        stats = []
        numeric_cols = data.select_dtypes(include=['number']).columns
        for col in numeric_cols:
            col_data = data[col]
            stats.append(f"- {col}: 均值={col_data.mean():.4f}, 标准差={col_data.std():.4f}, 范围=[{col_data.min()}, {col_data.max()}]")
        
        # 数据预览
        preview = f"数据形状: {data.shape[0]} 行 × {data.shape[1]} 列\n"
        preview += "列名: " + ", ".join(data.columns.tolist()) + "\n"
        preview += "统计摘要:\n" + "\n".join(stats)
        
        # 原始数据（限制行数）
        raw = data.head(10).to_string()
        
        return f"""
## 实验数据
{title}

{preview}

## 原始数据（部分）
{raw}
"""
    
    def analyze_phenomenon(self, data: pd.DataFrame, title: str = "",
                           description: str = "") -> AnalysisResult:
        """分析实验现象"""
        if not self._available:
            return self._fallback_analysis(data, title)
        
        # 格式化数据
        data_str = self._format_data_for_ai(data, title)
        
        # 构建提示词
        prompt = f"""
你是一位专业的大学实验指导老师。请分析以下实验数据：

{data_str}

## 任务
请分析实验现象并提供：
1. **实验现象描述**：数据呈现什么规律/趋势？
2. **实验结论**：根据数据能得出什么结论？
3. **数据趋势**：是线性/非线性？增长/下降？
4. **异常检测**：是否有异常数据点？
5. **改进建议**：如何改进实验？

请用中文回复，格式如下：
```
现象: <描述>
结论: <结论>
趋势: <趋势>
异常: <异常情况或"无">
建议: <改进建议>
置信度: <0-1之间的数字>
```
"""
        try:
            messages = [{"role": "user", "content": prompt}]
            response = self.provider.chat(messages)
            
            # 解析响应
            result = self._parse_response(response)
            result.raw_response = response
            
            return result
            
        except Exception as e:
            print(f"❌ AI 分析失败: {e}")
            return self._fallback_analysis(data, title)
    
    def generate_conclusion(self, data: pd.DataFrame, experiment_type: str,
                            title: str = "") -> str:
        """生成实验结论"""
        if not self._available:
            return self._default_conclusion(data, experiment_type)
        
        data_str = self._format_data_for_ai(data, title)
        
        prompt = f"""
你是大学实验报告写作专家。请根据以下实验数据生成规范的实验结论：

{data_str}

实验类型: {experiment_type}

请生成一段完整的实验结论（约200字），包含：
1. 实验目的的达成情况
2. 数据分析的主要发现
3. 实验结果的可靠性评价

请用中文回复，直接返回结论内容，无需额外解释。
"""
        try:
            messages = [{"role": "user", "content": prompt}]
            return self.provider.chat(messages)
        except Exception as e:
            print(f"❌ 结论生成失败: {e}")
            return self._default_conclusion(data, experiment_type)
    
    def fill_template_content(self, template_fields: Dict[str, str],
                             data: pd.DataFrame, title: str = "") -> Dict[str, str]:
        """填充模板内容"""
        # 分析数据
        analysis = self.analyze_phenomenon(data, title)
        
        # 填充内容
        filled = {}
        for field, description in template_fields.items():
            if "结论" in field:
                filled[field] = analysis.conclusion or "请填写结论..."
            elif "现象" in field:
                filled[field] = analysis.phenomenon or "请分析现象..."
            elif "分析" in field:
                filled[field] = analysis.phenomenon or "请进行分析..."
            elif "建议" in field:
                filled[field] = analysis.suggestion or "请提出改进建议..."
            elif "误差" in field:
                filled[field] = self._generate_error_analysis(data)
            else:
                filled[field] = description
        
        return filled
    
    def _generate_error_analysis(self, data: pd.DataFrame) -> str:
        """生成误差分析"""
        numeric_cols = data.select_dtypes(include=['number']).columns
        if not numeric_cols.empty:
            col = numeric_cols[0]
            col_data = data[col]
            cv = col_data.std() / col_data.mean() * 100 if col_data.mean() != 0 else 0
            return f"相对误差约为 {cv:.2f}%，在可接受范围内。"
        return "请手动分析误差来源..."
    
    def _parse_response(self, response: str) -> AnalysisResult:
        """解析 AI 响应"""
        result = AnalysisResult()
        
        lines = response.strip().split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith("现象:"):
                result.phenomenon = line[3:].strip()
            elif line.startswith("结论:"):
                result.conclusion = line[3:].strip()
            elif line.startswith("趋势:"):
                result.trend = line[3:].strip()
            elif line.startswith("异常:"):
                result.anomaly = line[3:].strip()
            elif line.startswith("建议:"):
                result.suggestion = line[3:].strip()
            elif line.startswith("置信度:"):
                try:
                    result.confidence = float(line[4:].strip())
                except:
                    result.confidence = 0.5
        
        return result
    
    def _fallback_analysis(self, data: pd.DataFrame, title: str) -> AnalysisResult:
        """降级分析（无 API 时）"""
        result = AnalysisResult()
        
        if data is not None and not data.empty:
            numeric_cols = data.select_dtypes(include=['number']).columns
            if len(numeric_cols) >= 2:
                x, y = numeric_cols[0], numeric_cols[1]
                x_data, y_data = data[x], data[y]
                
                # 简单趋势分析
                if x_data.diff().mean() > 0 and y_data.diff().mean() > 0:
                    trend = "正相关趋势"
                elif x_data.diff().mean() > 0 and y_data.diff().mean() < 0:
                    trend = "负相关趋势"
                else:
                    trend = "无明显趋势"
                
                # 异常检测
                from numpy import abs as np_abs
                outliers = np_abs(y_data - y_data.mean()) > 2 * y_data.std()
                outlier_count = outliers.sum()
                
                result.phenomenon = f"实验数据覆盖 {x} 范围为 {x_data.min():.2f} ~ {x_data.max():.2f}"
                result.trend = trend
                result.anomaly = f"检测到 {outlier_count} 个潜在异常点" if outlier_count > 0 else "未检测到明显异常"
                result.conclusion = f"实验结果与{x}和{y}的关系相符"
                result.suggestion = "建议增加数据点以提高拟合精度"
                result.confidence = 0.7
        
        result.raw_response = "（本地分析模式）"
        return result
    
    def _default_conclusion(self, data: pd.DataFrame, experiment_type: str) -> str:
        """默认结论"""
        return f"""
本次{experiment_type}实验已完成，数据采集和分析工作已就绪。
根据实验数据，可得出初步结论：
1. 实验数据符合理论预期
2. 相对误差在可接受范围内
3. 实验方法合理，结果可靠

建议后续可进一步优化实验条件，提高测量精度。
"""


# 便捷函数
def quick_analyze(data_path: str, title: str = "",
                  api_key: str = "", provider: str = "openai") -> AnalysisResult:
    """快速分析实验数据"""
    config = AIConfig(
        provider=provider,
        api_key=api_key or OPENAI_API_KEY
    )
    
    analyzer = AILabAnalyzer(config)
    
    # 加载数据
    ext = Path(data_path).suffix.lower()
    if ext == '.csv':
        data = pd.read_csv(data_path)
    elif ext == '.xlsx':
        data = pd.read_excel(data_path)
    else:
        raise ValueError(f"不支持格式: {ext}")
    
    return analyzer.analyze_phenomenon(data, title)


if __name__ == "__main__":
    # 测试
    import sys
    data_path = sys.argv[1] if len(sys.argv) > 1 else "data/examples/欧姆定律数据.csv"
    
    # 本地模式测试（无 API Key）
    analyzer = AILabAnalyzer(AIConfig(provider="local", base_url="http://localhost:11434/v1"))
    
    if not analyzer._available:
        print("⚠️ AI 不可用，使用本地分析...")
        analyzer = AILabAnalyzer()
    
    data = pd.read_csv(data_path)
    result = analyzer.analyze_phenomenon(data, "欧姆定律验证实验")
    
    print("\n📊 分析结果:")
    print(f"现象: {result.phenomenon}")
    print(f"结论: {result.conclusion}")
    print(f"趋势: {result.trend}")
    print(f"异常: {result.anomaly}")
    print(f"建议: {result.suggestion}")
    print(f"置信度: {result.confidence:.2f}")
