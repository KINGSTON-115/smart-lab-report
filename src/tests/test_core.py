# 🧪 测试用例
# Test Cases

import unittest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.generators.chart_generator import ChartGenerator, ChartConfig
from src.generators.report_generator import ReportGenerator

class TestChartGenerator(unittest.TestCase):
    """图表生成器测试"""
    
    def setUp(self):
        """创建测试数据"""
        self.data = pd.DataFrame({
            'x': [1, 2, 3, 4, 5, 6],
            'y': [2, 4, 5, 4, 5, 6]
        })
        self.generator = ChartGenerator(self.data)
    
    def test_generate_line_chart(self):
        """测试折线图生成"""
        config = ChartConfig(
            title="测试折线图",
            chart_type="line",
            save_path="output/test_line.png"
        )
        result = self.generator.generate('x', ['y'], config)
        self.assertIn('image_base64', result)
        self.assertIn('save_path', result)
    
    def test_generate_scatter(self):
        """测试散点图生成"""
        config = ChartConfig(chart_type="scatter")
        result = self.generator.generate('x', ['y'], config)
        self.assertIn('image_base64', result)
    
    def test_generate_regression(self):
        """测试回归分析"""
        result = self.generator.generate_regression('x', 'y', degree=1)
        self.assertIn('r_squared', result)
        self.assertIn('coefficients', result)
        self.assertIn('equation', result)
        self.assertGreater(result['r_squared'], 0)
    
    def test_error_analysis(self):
        """测试误差分析"""
        result = self.generator.generate_error_analysis('x', 'y')
        self.assertIn('mean', result)
        self.assertIn('std', result)
        self.assertIn('relative_error_percent', result)


class TestReportGenerator(unittest.TestCase):
    """报告生成器测试"""
    
    def setUp(self):
        self.generator = ReportGenerator("physics_basic")
    
    def test_load_csv(self):
        """测试 CSV 数据加载"""
        data = self.generator.load_data("data/examples/欧姆定律数据.csv")
        self.assertEqual(len(data), 6)
        self.assertIn('电压(V)', data.columns)
    
    def test_summarize_data(self):
        """测试数据摘要"""
        data = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': [2, 4, 6, 8, 10]
        })
        summary = self.generator.summarize_data(data)
        self.assertIn('statistics', summary)
        self.assertIn('A', summary['statistics'])
        self.assertIn('B', summary['statistics'])
    
    def test_generate_report(self):
        """测试报告生成"""
        data = pd.DataFrame({'x': [1, 2, 3], 'y': [2, 4, 6]})
        self.generator.summarize_data(data)
        
        report = self.generator.generate_report(
            title="测试实验",
            author="测试用户",
            group="测试组",
            data=data
        )
        
        self.assertIn("测试实验", report)
        self.assertIn("测试用户", report)
        self.assertIn("物理实验基础模板", report)


class TestTemplates(unittest.TestCase):
    """模板测试"""
    
    def test_physics_template(self):
        """物理模板"""
        gen = ReportGenerator("physics_basic")
        self.assertEqual(gen.template.name, "physics_basic")
        self.assertTrue(len(gen.template.sections) > 0)
    
    def test_chemistry_template(self):
        """化学模板"""
        gen = ReportGenerator("chemistry_basic")
        self.assertEqual(gen.template.name, "chemistry_basic")
    
    def test_cs_template(self):
        """计算机模板"""
        gen = ReportGenerator("cs_algorithm")
        self.assertEqual(gen.template.name, "cs_algorithm")


if __name__ == "__main__":
    unittest.main()
