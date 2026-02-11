# 🧪 图表生成器 - 自动绑定数据可视化
# Chart Generator - Auto-bind data visualization

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # 无头模式

# 设置支持中文的字体
import matplotlib.font_manager as fm
import os

# 查找可用的中文字体
CHINESE_FONTS = [
    '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',  # 文泉驿正黑
    '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',  # Noto Sans CJK
]

FONT_PATH = None
for font_path in CHINESE_FONTS:
    if os.path.exists(font_path):
        FONT_PATH = font_path
        break

if FONT_PATH:
    # 注册字体
    fm.fontManager.addfont(FONT_PATH)
    prop = fm.FontProperties(fname=FONT_PATH)
    FONT_NAME = prop.get_name()
    plt.rcParams['font.sans-serif'] = [FONT_NAME]
    plt.rcParams['axes.unicode_minus'] = False
else:
    FONT_NAME = 'DejaVu Sans'
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import base64
from io import BytesIO

@dataclass
class ChartConfig:
    """图表配置"""
    title: str = ""
    xlabel: str = ""
    ylabel: str = ""
    figsize: tuple = (8, 6)
    style: str = "default"  # default, science, ggplot, seaborn
    chart_type: str = "line"  # line, scatter, bar, histogram
    color: str = "blue"
    grid: bool = True
    legend: bool = True
    save_path: str = ""

class ChartGenerator:
    """图表生成器 - 自动从数据生成专业图表"""
    
    CHART_STYLES = {
        "default": plt.style.available[0] if plt.style.available else "default",
        "science": "science",
        "ggplot": "ggplot",
        "seaborn": "seaborn-v0_8-whitegrid"
    }
    
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.figures = []
        
    def generate(self, x_col: str, y_cols: List[str], config: ChartConfig = None) -> Dict[str, str]:
        """自动生成图表
        
        Args:
            x_col: X轴列名
            y_cols: Y轴列名列表
            config: 图表配置
        
        Returns:
            Dict: {"image_base64": "...", "save_path": "..."}
        """
        config = config or ChartConfig()
        
        # 设置样式
        if config.style != "default" and config.style in self.CHART_STYLES:
            try:
                plt.style.use(self.CHART_STYLES[config.style])
            except:
                pass
        
        fig, ax = plt.subplots(figsize=config.figsize)
        
        x = self.data[x_col]
        
        for y_col in y_cols:
            y = self.data[y_col]
            
            if config.chart_type == "line":
                ax.plot(x, y, color=config.color, label=y_col, linewidth=2, marker='o', markersize=4)
            elif config.chart_type == "scatter":
                ax.scatter(x, y, color=config.color, label=y_col, s=50, alpha=0.7)
            elif config.chart_type == "bar":
                ax.bar(x, y, color=config.color, label=y_col, alpha=0.7)
            elif config.chart_type == "histogram":
                ax.hist(y, bins=20, color=config.color, alpha=0.7, label=y_col)
        
        # 设置标签
        ax.set_title(config.title or f"{y_cols[0]} vs {x_col}", fontsize=14, fontweight='bold')
        ax.set_xlabel(config.xlabel or x_col, fontsize=12)
        ax.set_ylabel(", ".join(y_cols) if len(y_cols) > 1 else config.ylabel or y_cols[0], fontsize=12)
        
        if config.grid:
            ax.grid(True, linestyle='--', alpha=0.7)
        if config.legend and len(y_cols) > 1:
            ax.legend()
        
        plt.tight_layout()
        
        # 保存或返回 base64
        result = {}
        
        if config.save_path:
            save_path = Path(config.save_path)
            save_path.parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(save_path, dpi=150, bbox_inches='tight')
            result["save_path"] = str(save_path)
            print(f"✅ 图表已保存: {save_path}")
        
        # 转换为 base64
        buffer = BytesIO()
        fig.savefig(buffer, format='png', dpi=150, bbox_inches='tight')
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        result["image_base64"] = f"data:image/png;base64,{img_base64}"
        
        self.figures.append(fig)
        plt.close(fig)
        
        return result
    
    def generate_regression(self, x_col: str, y_col: str, degree: int = 1) -> Dict:
        """自动拟合回归线"""
        from numpy.polynomial import polynomial as P
        
        x = self.data[x_col].values
        y = self.data[y_col].values
        
        # 拟合
        coeffs = np.polyfit(x, y, degree)
        y_fit = np.polyval(coeffs, x)
        
        # 计算 R²
        ss_res = np.sum((y - y_fit) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r_squared = 1 - (ss_res / ss_tot)
        
        # 绘图
        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(x, y, color='blue', label='原始数据', alpha=0.7)
        ax.plot(x, y_fit, color='red', linewidth=2, label=f'拟合曲线 (R²={r_squared:.4f})')
        
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.7)
        
        buffer = BytesIO()
        fig.savefig(buffer, format='png', dpi=150)
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        
        plt.close(fig)
        
        return {
            "coefficients": coeffs.tolist(),
            "r_squared": r_squared,
            "equation": f"y = {' + '.join([f'{c:.4f}x^{i}' for i, c in enumerate(coeffs[::-1])])}",
            "image_base64": f"data:image/png;base64,{img_base64}"
        }
    
    def generate_error_analysis(self, x_col: str, y_col: str) -> Dict:
        """自动误差分析"""
        x = self.data[x_col].values
        y = self.data[y_col].values
        
        # 计算统计量
        mean_y = np.mean(y)
        std_y = np.std(y)
        mean_x = np.mean(x)
        
        # 相对误差
        relative_error = std_y / mean_y * 100
        
        # 异常值检测 (2σ 准则)
        outliers = np.abs(y - mean_y) > 2 * std_y
        outlier_indices = np.where(outliers)[0]
        
        return {
            "mean": float(mean_y),
            "std": float(std_y),
            "relative_error_percent": float(relative_error),
            "outlier_count": int(np.sum(outliers)),
            "outlier_indices": outlier_indices.tolist(),
            "has_outliers": bool(np.sum(outliers) > 0)
        }


# 便捷函数
def quick_plot(data_path: str, x_col: str, y_col: str, output_path: str = "") -> Dict:
    """快速绑定数据生成图表"""
    ext = Path(data_path).suffix.lower()
    if ext == '.csv':
        data = pd.read_csv(data_path)
    elif ext == '.xlsx':
        data = pd.read_excel(data_path)
    else:
        raise ValueError(f"不支持格式: {ext}")
    
    generator = ChartGenerator(data)
    return generator.generate(x_col, [y_col], ChartConfig(save_path=output_path))


if __name__ == "__main__":
    # 测试
    import sys
    data_path = sys.argv[1] if len(sys.argv) > 1 else "data/examples/欧姆定律数据.csv"
    output = quick_plot(data_path, "电压(V)", "电流(A)", "output/test_chart.png")
    print(f"图表生成成功: {output['save_path']}")
