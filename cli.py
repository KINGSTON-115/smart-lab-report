# -*- coding: utf-8 -*-
"""
🧪 智能实验报告生成器 CLI
Smart Lab Report CLI
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from src.generators.report_generator import ReportGenerator
from src.generators.chart_generator import ChartGenerator, ChartConfig

def setup_chinese_font():
    """设置中文字体支持"""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    
    # 尝试设置中文字体
    fonts = [
        'SimHei', 'Microsoft YaHei', 'WenQuanYi Micro Hei',
        'Noto Sans CJK SC', 'DejaVu Sans'
    ]
    
    for font in fonts:
        try:
            plt.rcParams['font.sans-serif'] = [font]
            plt.rcParams['axes.unicode_minus'] = False
            break
        except:
            continue

def main():
    parser = argparse.ArgumentParser(
        description="🧪 智能实验报告生成器 - 从数据自动生成实验报告",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  # 生成物理实验报告
  python cli.py --data data/examples/欧姆定律数据.csv \\
                --template physics_basic \\
                --title "欧姆定律验证实验" \\
                --author "张三" \\
                --output output/report.html
                
  # 生成带图表的报告
  python cli.py --data data.csv \\
                --x "电压" --y "电流" \\
                --chart-type scatter \\
                --title "实验报告"
        """
    )
    
    # 必需参数
    parser.add_argument('--data', '-d', required=True, help='实验数据文件路径 (CSV/Excel/JSON)')
    parser.add_argument('--title', '-t', required=True, help='实验报告标题')
    
    # 模板参数
    parser.add_argument('--template', '-T', 
                       default='physics_basic',
                       choices=['physics_basic', 'chemistry_basic', 'biology_basic', 
                               'cs_algorithm', 'engineering_basic'],
                       help='报告模板类型')
    
    # 作者信息
    parser.add_argument('--author', '-a', default='', help='作者姓名')
    parser.add_argument('--group', '-g', default='', help='实验组别')
    
    # 图表参数
    parser.add_argument('--x', '-x', default='', help='X轴列名')
    parser.add_argument('--y', '-y', default='', help='Y轴列名')
    parser.add_argument('--chart-type', '-c', 
                       default='scatter',
                       choices=['line', 'scatter', 'bar', 'histogram'],
                       help='图表类型')
    parser.add_argument('--chart-title', default='', help='图表标题')
    parser.add_argument('--no-chart', action='store_true', help='不生成图表')
    
    # 输出参数
    parser.add_argument('--output', '-o', default='output/report.html', help='输出文件路径')
    parser.add_argument('--format', '-f', 
                       default='html',
                       choices=['html', 'markdown'],
                       help='输出格式')
    
    # 其他参数
    parser.add_argument('--conclusion', default='', help='实验结论')
    parser.add_argument('--error-analysis', default='', help='误差分析')
    parser.add_argument('--quiet', '-q', action='store_true', help='安静模式（减少输出）')
    
    args = parser.parse_args()
    
    # 设置中文字体
    setup_chinese_font()
    
    try:
        if not args.quiet:
            print("🧪 智能实验报告生成器")
            print("=" * 50)
        
        # 初始化报告生成器
        generator = ReportGenerator(args.template)
        
        # 加载数据
        if not args.quiet:
            print(f"📂 加载数据: {args.data}")
        data = generator.load_data(args.data)
        
        # 数据摘要
        if not args.quiet:
            print(f"📊 数据形状: {data.shape[0]} 行 × {data.shape[1]} 列")
        summary = generator.summarize_data(data)
        
        # 获取数值列
        numeric_cols = data.select_dtypes(include=['number']).columns.tolist()
        
        # 自动生成图表
        if not args.no_chart:
            if not args.quiet:
                print("📈 生成图表...")
            
            # 智能选择列
            x_col = args.x or (numeric_cols[0] if numeric_cols else None)
            y_col = args.y or (numeric_cols[1] if len(numeric_cols) > 1 else (numeric_cols[0] if numeric_cols else None))
            
            if x_col and y_col:
                chart_config = ChartConfig(
                    title=args.chart_title or f"{y_col} vs {x_col}",
                    chart_type=args.chart_type,
                    xlabel=x_col,
                    ylabel=y_col
                )
                generator.add_chart(data, x_col, y_col, chart_config)
                if not args.quiet:
                    print(f"   图表: {x_col} → {y_col}")
        
        # 生成报告
        if not args.quiet:
            print("📝 生成报告...")
        
        report = generator.generate_report(
            title=args.title,
            author=args.author,
            group=args.group,
            data=data,
            conclusion=args.conclusion or "请根据实验结果填写结论...",
            error_analysis=args.error_analysis or "请分析实验误差来源..."
        )
        
        # 保存报告
        output_path = args.output
        if not output_path.endswith(('.html', '.md')):
            output_path += f".{args.format}"
        
        generator.save_report(report, output_path)
        
        if not args.quiet:
            print(f"\n✅ 报告生成成功!")
            print(f"📄 输出文件: {output_path}")
            print(f"📊 统计摘要:")
            for col, stats in summary.get('statistics', {}).items():
                print(f"   {col}: 均值={stats['mean']:.4f}, 标准差={stats['std']:.4f}")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ 错误: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
