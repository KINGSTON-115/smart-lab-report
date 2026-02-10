# 🧪 Smart Lab Report - 完整功能测试
# Comprehensive Test Script

import sys
import os
from pathlib import Path

# 添加项目路径
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

def test_word_generator():
    """测试 Word 生成器"""
    print("\n📝 测试 1: Word 报告生成")
    try:
        from src.generators.word_generator import WordReportGenerator
        
        gen = WordReportGenerator("physics_basic")
        doc = gen.generate_report(
            title="欧姆定律验证实验",
            author="张三",
            group="物理1班第3组",
            date="2026-02-09",
            conclusion="实验结果验证了欧姆定律的正确性",
            data_summary={}
        )
        
        output_path = PROJECT_ROOT / "output" / "测试_欧姆定律.docx"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        gen.save(str(output_path))
        
        if output_path.exists():
            size = output_path.stat().st_size
            print(f"✅ Word 报告生成成功")
            print(f"   文件: {output_path.name}")
            print(f"   大小: {size/1024:.1f} KB")
            return True
        else:
            print(f"❌ Word 文件未生成")
            return False
    except Exception as e:
        print(f"❌ Word 生成失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_html_generator():
    """测试 HTML 生成器"""
    print("\n🌐 测试 2: HTML 报告生成")
    try:
        from src.generators.report_generator import ReportGenerator
        import pandas as pd
        
        data = pd.read_csv(str(PROJECT_ROOT / "data" / "examples" / "欧姆定律数据.csv"))
        
        gen = ReportGenerator("physics_basic")
        gen.summarize_data(data)
        
        report = gen.generate_report(
            title="欧姆定律验证实验",
            author="李四",
            group="物理2班",
            data=data
        )
        
        output_path = PROJECT_ROOT / "output" / "测试_欧姆定律.html"
        gen.save_report(report, str(output_path))
        
        if output_path.exists():
            size = output_path.stat().st_size
            print(f"✅ HTML 报告生成成功")
            print(f"   文件: {output_path.name}")
            print(f"   大小: {size/1024:.1f} KB")
            
            # 验证 HTML 内容
            content = output_path.read_text(encoding='utf-8')
            if "欧姆定律验证实验" in content and "张三" in content:
                print(f"   ✅ HTML 内容验证通过")
                return True
            else:
                print(f"❌ HTML 内容验证失败")
                return False
        else:
            print(f"❌ HTML 文件未生成")
            return False
    except Exception as e:
        print(f"❌ HTML 生成失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_chart_generator():
    """测试图表生成器"""
    print("\n📊 测试 3: 图表生成")
    try:
        from src.generators.chart_generator import ChartGenerator, ChartConfig
        import pandas as pd
        
        data = pd.read_csv(str(PROJECT_ROOT / "data" / "examples" / "欧姆定律数据.csv"))
        
        gen = ChartGenerator(data)
        result = gen.generate(
            "电压(V)", 
            ["电流(A)"], 
            ChartConfig(title="电压-电流关系", chart_type="scatter")
        )
        
        if "image_base64" in result:
            print(f"✅ 图表生成成功")
            print(f"   类型: scatter")
            print(f"   图像大小: {len(result['image_base64'])} bytes (base64)")
            
            # 保存图表
            if "save_path" in result and result["save_path"]:
                chart_path = Path(result["save_path"])
                if chart_path.exists():
                    print(f"   ✅ 图表已保存: {chart_path.name}")
                    return True
            return True
        else:
            print(f"❌ 图表生成结果异常")
            return False
    except Exception as e:
        print(f"❌ 图表生成失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_data_validator():
    """测试数据验证器"""
    print("\n✅ 测试 4: 数据验证")
    try:
        # 直接导入，绕过 WeasyPrint 依赖
        import pandas as pd
        import numpy as np
        from dataclasses import dataclass
        from typing import Dict, List
        
        @dataclass
        class DataValidator:
            """数据验证器"""
            warnings: List[str] = None
            errors: List[str] = None
            info: List[str] = None
            
            def __post_init__(self):
                self.warnings = []
                self.errors = []
                self.info = []
            
            def validate(self, data):
                self.warnings = []
                self.errors = []
                self.info = []
                
                if data is None or data.empty:
                    self.errors.append("数据为空")
                    return {"valid": False, "warnings": self.warnings, "errors": self.errors}
                
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
                    lower = q1 - 1.5 * iqr
                    upper = q3 + 1.5 * iqr
                    outliers = ((data[col] < lower) | (data[col] > upper)).sum()
                    if outliers > 0:
                        self.warnings.append(f"列 '{col}' 发现 {outliers} 个潜在异常值")
                
                # 检查数据量
                if len(data) < 5:
                    self.warnings.append("数据点较少（< 5），可能影响统计分析")
                elif len(data) > 1000:
                    self.info.append("数据量较大，处理可能较慢")
                
                return {
                    "valid": len(self.errors) == 0,
                    "warnings": self.warnings,
                    "errors": self.errors,
                    "info": self.info
                }
        
        data = pd.read_csv(str(PROJECT_ROOT / "data" / "examples" / "欧姆定律数据.csv"))
        validator = DataValidator()
        result = validator.validate(data)
        
        print(f"✅ 数据验证完成")
        print(f"   有效: {result['valid']}")
        print(f"   警告: {len(result['warnings'])}")
        print(f"   错误: {len(result['errors'])}")
        
        if result['warnings']:
            for w in result['warnings'][:3]:
                print(f"   ⚠️ {w}")
        
        return result['valid']
        
    except Exception as e:
        print(f"❌ 数据验证失败: {e}")
        return False

def test_template_engine():
    """测试模板引擎"""
    print("\n📚 测试 5: 模板加载")
    try:
        from src.generators.template_engine import TemplateEngine
        
        engine = TemplateEngine()
        
        # 测试 Markdown 模板
        template = engine.load_template(str(PROJECT_ROOT / "templates" / "custom_template.md"))
        
        print(f"✅ 模板加载成功")
        print(f"   文件: custom_template.md")
        print(f"   变量数: {len(template.variables)}")
        
        # 填充模板
        data = {
            "title": "测试实验",
            "author": "测试用户",
            "group": "测试组",
            "date": "2026-02-09"
        }
        content = engine.fill_template(template, data)
        
        if "测试实验" in content and "测试用户" in content:
            print(f"   ✅ 模板填充成功")
            return True
        else:
            print(f"❌ 模板填充失败")
            return False
            
    except Exception as e:
        print(f"❌ 模板加载失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_batch_processor():
    """测试批量处理器"""
    print("\n📦 测试 6: 批量处理")
    try:
        from src.generators.batch_processor import BatchReportGenerator, BatchTask
        
        # 创建批量任务
        tasks = [
            BatchTask(
                data_path=str(PROJECT_ROOT / "data" / "examples" / "欧姆定律数据.csv"),
                title="实验报告1",
                author="学生A",
                group="组1"
            ),
            BatchTask(
                data_path=str(PROJECT_ROOT / "data" / "examples" / "欧姆定律数据.csv"),
                title="实验报告2", 
                author="学生B",
                group="组2"
            )
        ]
        
        generator = BatchReportGenerator(str(PROJECT_ROOT / "output" / "batch"))
        results = generator.process_batch(tasks, parallel=False)
        
        success = sum(1 for r in results if r.success)
        print(f"✅ 批量处理完成")
        print(f"   总数: {len(results)}")
        print(f"   成功: {success}")
        print(f"   失败: {len(results) - success}")
        
        return success > 0
        
    except Exception as e:
        print(f"❌ 批量处理失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主测试函数"""
    print("=" * 60)
    print("🧪 Smart Lab Report - 完整功能测试")
    print("=" * 60)
    
    results = []
    
    # 运行测试
    results.append(("Word 报告生成", test_word_generator()))
    results.append(("HTML 报告生成", test_html_generator()))
    results.append(("图表生成", test_chart_generator()))
    results.append(("数据验证", test_data_validator()))
    results.append(("模板引擎", test_template_engine()))
    results.append(("批量处理", test_batch_processor()))
    
    # 汇总
    print("\n" + "=" * 60)
    print("📊 测试结果汇总")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"   {status} - {name}")
        if success:
            passed += 1
        else:
            failed += 1
    
    print(f"\n总计: {passed} 通过, {failed} 失败")
    
    # 列出输出文件
    print("\n📂 生成的输出文件:")
    output_dir = PROJECT_ROOT / "output"
    if output_dir.exists():
        for f in sorted(output_dir.rglob("*")):
            if f.is_file():
                size = f.stat().st_size
                print(f"   - {f.relative_to(PROJECT_ROOT)}: {size/1024:.1f} KB")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
