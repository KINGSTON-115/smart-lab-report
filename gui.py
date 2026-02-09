# 🧪 Smart Lab Report - Windows GUI 主程序（增强版）
# Smart Lab Report - Windows GUI Main Application (Enhanced)

import sys
import os
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    import PySimpleGUI as sg
except ImportError:
    print("请安装 GUI 依赖: pip install PySimpleGUI")
    sys.exit(1)

import pandas as pd

from src.generators.report_generator import ReportGenerator
from src.generators.chart_generator import ChartGenerator, ChartConfig
from src.generators.word_generator import WordReportGenerator
from src.generators.template_engine import TemplateEngine
from src.generators.ai_engine import AILabAnalyzer, AIConfig


class LabReportApp:
    """实验报告生成器 GUI 应用（增强版）"""
    
    def __init__(self):
        self.data_file = None
        self.template_file = None
        self.template = "physics_basic"
        self.data_preview = None
        self.ai_available = False
        
        # 模板列表
        self.templates = {
            "physics_basic": "物理实验基础模板",
            "chemistry_basic": "化学实验基础模板",
            "biology_basic": "生物实验基础模板",
            "cs_algorithm": "计算机算法模板",
            "engineering_basic": "工程实验基础模板",
            "custom": "📁 自定义模板 (上传您的模板)"
        }
        
        # 图表类型
        self.chart_types = ["line", "scatter", "bar", "histogram"]
        
        # AI 提供商
        self.ai_providers = {
            "openai": "OpenAI (GPT-3.5/4)",
            "claude": "Claude (Anthropic)",
            "qwen": "通义千问 (阿里)",
            "zhipu": "智谱 AI (ChatGLM)",
            "local": "本地模型 (Ollama)",
            "none": "不使用 AI"
        }
        
        self._setup_theme()
        self._check_ai()
    
    def _setup_theme(self):
        """设置主题"""
        sg.theme('LightBlue3')
    
    def _check_ai(self):
        """检查 AI 是否可用"""
        config = AIConfig()
        analyzer = AILabAnalyzer(config)
        self.ai_available = analyzer._available
    
    def create_window(self):
        """创建主窗口"""
        
        # ===== 标题区域 =====
        title = [[sg.Text("🧪 智能实验报告生成器", font=('Microsoft YaHei', 20, 'bold'), 
                         justification='center', expand_x=True)],
                 [sg.Text("支持自定义模板 + AI 大模型分析", font=('Microsoft YaHei', 10),
                         justification='center', text_color='gray')]]
        
        # ===== 第一行：数据文件 =====
        file_section = [
            [sg.Text("📁 实验数据文件:", font=('Microsoft YaHei', 11, 'bold'))],
            [
                sg.Input(key='-FILE-', size=(45, 1), enable_events=True,
                        placeholder='选择 CSV/Excel/JSON 文件...'),
                sg.FileBrowse("浏览", file_types=(("数据文件", "*.csv *.xlsx *.json"), ("所有文件", "*.*")),
                             initial_folder=str(PROJECT_ROOT / "data")),
                sg.Button("示例数据", key='-SAMPLE-')
            ],
            [sg.Text(key='-FILE_INFO-', size=(60, 1), text_color='blue')]
        ]
        
        # ===== 第二行：自定义模板 =====
        template_section = [
            [sg.Text("📄 自定义模板 (可选):", font=('Microsoft YaHei', 11, 'bold'))],
            [
                sg.Input(key='-TEMPLATE_FILE-', size=(45, 1), enable_events=True,
                        placeholder='选择 Word/HTML/Markdown 模板...'),
                sg.FileBrowse("上传模板", file_types=(("模板文件", "*.docx *.md *.html"), ("所有文件", "*.*")),
                             initial_folder=str(PROJECT_ROOT)),
                sg.Button("解析模板", key='-PARSE_TEMPLATE-')
            ],
            [sg.Text(key='-TEMPLATE_INFO-', size=(60, 1), text_color='green')],
            [sg.Text("💡 提示: 使用 {{变量名}} 标记需要填充的位置", 
                    font=('Microsoft YaHei', 9), text_color='gray', size=(60, 1))]
        ]
        
        # ===== 第三行：报告信息 =====
        info_section = [
            [sg.Text("📝 报告信息:", font=('Microsoft YaHei', 11, 'bold'))],
            [
                sg.Text("标题:"), sg.Input(key='-TITLE-', size=(25, 1), 
                                         placeholder='例如: 欧姆定律验证实验'),
                sg.Text("作者:"), sg.Input(key='-AUTHOR-', size=(12, 1), placeholder='你的名字'),
            ],
            [
                sg.Text("组别:"), sg.Input(key='-GROUP-', size=(25, 1), placeholder='例如: 物理1班第3组'),
                sg.Text("模板:"), sg.Combo(list(self.templates.values()), 
                                         key='-TEMPLATE-', size=(18, 1),
                                         default_value=list(self.templates.values())[0],
                                         enable_events=True)
            ]
        ]
        
        # ===== 第四行：AI 设置 =====
        ai_section = [
            [sg.Text("🤖 AI 分析设置:", font=('Microsoft YaHei', 11, 'bold'))],
            [
                sg.Text("提供商:"), sg.Combo(list(self.ai_providers.values()), 
                                          key='-AI_PROVIDER-', size=(20, 1),
                                          default_value=list(self.ai_providers.values())[0] if self.ai_available else "不使用 AI"),
                sg.Text("API Key:"), 
                sg.Input(key='-API_KEY-', size=(25, 1), password_char='*', 
                        placeholder='输入 API Key 或留空使用环境变量'),
            ],
            [
                sg.Checkbox('启用 AI 自动分析', key='-ENABLE_AI-', default=self.ai_available),
                sg.Text("AI 状态:", text_color='green' if self.ai_available else 'red'),
                sg.Text("✅ 可用" if self.ai_available else "❌ 不可用", 
                       key='-AI_STATUS-', 
                       text_color='green' if self.ai_available else 'red')
            ],
            [
                sg.Text("AI 将自动生成: 实验现象、结论、分析、改进建议", 
                       font=('Microsoft YaHei', 9), text_color='gray', size=(60, 1))
            ]
        ]
        
        # ===== 第五行：图表设置 =====
        chart_section = [
            [sg.Text("📊 图表设置:", font=('Microsoft YaHei', 11, 'bold'))],
            [
                sg.Text("X轴:"), sg.Combo(key='-X_COL-', values=[], size=(12, 1)),
                sg.Text("Y轴:"), sg.Combo(key='-Y_COL-', values=[], size=(12, 1)),
                sg.Text("类型:"), sg.Combo(self.chart_types, key='-CHART_TYPE-', 
                                          default_value='scatter', size=(10, 1)),
            ],
            [
                sg.Text("图表标题:"), sg.Input(key='-CHART_TITLE-', size=(25, 1)),
                sg.Checkbox('生成图表', key='-GENERATE_CHART-', default=True),
                sg.Checkbox('图表插入模板', key='-CHART_IN_TEMPLATE-', default=True)
            ]
        ]
        
        # ===== 第六行：输出设置 =====
        output_section = [
            [sg.Text("📤 输出设置:", font=('Microsoft YaHei', 11, 'bold'))],
            [
                sg.Checkbox('Word (.docx)', key='-OUTPUT_DOCX-', default=True),
                sg.Checkbox('HTML', key='-OUTPUT_HTML-', default=True),
                sg.Checkbox('Markdown', key='-OUTPUT_MD-', default=False),
            ],
            [
                sg.FolderBrowse("输出文件夹", key='-OUTPUT_DIR-', 
                               initial_folder=str(PROJECT_ROOT / "output")),
            ]
        ]
        
        # ===== 数据预览 =====
        preview_section = [
            [sg.Text("📋 数据预览:", font=('Microsoft YaHei', 11, 'bold'))],
            [sg.Table(key='-PREVIEW-', values=[], headings=['数据预览将在这里显示'],
                     size=(80, 5), num_rows=5, max_col_width=20,
                     display_row_numbers=False, enable_events=False)]
        ]
        
        # ===== AI 分析结果 =====
        ai_result_section = [
            [sg.Text("🤖 AI 分析结果:", font=('Microsoft YaHei', 11, 'bold'))],
            [sg.Multiline(key='-AI_RESULT-', size=(80, 8), font=('Microsoft YaHei', 9),
                         autoscroll=True, disabled=True)]
        ]
        
        # ===== 日志输出 =====
        log_section = [
            [sg.Text("📜 生成日志:", font=('Microsoft YaHei', 11, 'bold'))],
            [sg.Multiline(key='-LOG-', size=(80, 6), font=('Consolas', 9),
                         autoscroll=True, disabled=True)]
        ]
        
        # ===== 按钮 =====
        button_section = [
            [
                sg.Button("🚀 生成报告", key='-GENERATE-', 
                        button_color=('white', '#27ae60'), font=('Microsoft YaHei', 12, 'bold'),
                        size=(15, 1)),
                sg.Button("🧪 AI 分析", key='-AI_ANALYZE-', 
                        button_color=('white', '#3498db'), font=('Microsoft YaHei', 11),
                        size=(12, 1)),
                sg.Button("🗑️ 清空", key='-CLEAR-', size=(10, 1)),
                sg.Button("❌ 退出", key='-EXIT-', size=(10, 1))
            ]
        ]
        
        # 组装布局
        layout = [
            [sg.Column(title, justification='center', expand_x=True)],
            [sg.HorizontalSeparator()],
            [sg.Frame("实验数据", file_section, expand_x=True)],
            [sg.Frame("自定义模板", template_section, expand_x=True)],
            [sg.Frame("报告信息", info_section, expand_x=True)],
            [sg.Frame("AI 分析", ai_section, expand_x=True)],
            [sg.Frame("图表设置", chart_section, expand_x=True)],
            [sg.Frame("输出格式", output_section, expand_x=True)],
            [sg.Frame("预览", preview_section, expand_x=True)],
            [sg.Frame("AI 结果", ai_result_section, expand_x=True)],
            [sg.Frame("日志", log_section, expand_x=True)],
            [sg.Column(button_section, justification='center', expand_x=True)],
        ]
        
        # 创建窗口
        window = sg.Window(
            "智能实验报告生成器 - Smart Lab Report",
            layout,
            size=(750, 950),
            resizable=True,
            finalize=True
        )
        
        return window
    
    def load_data(self, filepath: str):
        """加载数据文件"""
        ext = Path(filepath).suffix.lower()
        
        try:
            if ext == '.csv':
                df = pd.read_csv(filepath)
            elif ext == '.xlsx':
                df = pd.read_excel(filepath)
            elif ext == '.json':
                df = pd.read_json(filepath)
            else:
                return None, "不支持的文件格式"
            
            self.data_file = filepath
            return df, None
            
        except Exception as e:
            return None, str(e)
    
    def parse_template(self, filepath: str) -> Dict:
        """解析自定义模板"""
        from src.generators.template_engine import TemplateEngine
        
        engine = TemplateEngine()
        template = engine.load_template(filepath)
        
        # 获取字段
        fields = {f.name: f.description for f in template.fields}
        
        return {
            "template": template,
            "fields": fields,
            "variables": template.variables
        }
    
    def run_ai_analysis(self, window, values):
        """运行 AI 分析"""
        if not self.data_file:
            window['-AI_RESULT-'].print("❌ 请先选择数据文件！")
            return
        
        # 获取 AI 配置
        provider_map = {v: k for k, v in self.ai_providers.items()}
        provider = provider_map.get(values['-AI_PROVIDER'], "openai")
        api_key = values['-API_KEY-']
        
        config = AIConfig(
            provider=provider,
            api_key=api_key,
            model="gpt-3.5-turbo"
        )
        
        analyzer = AILabAnalyzer(config)
        
        if not analyzer._available:
            window['-AI_RESULT-'].print("❌ AI 不可用，请检查 API Key 或网络连接")
            return
        
        # 加载数据
        df, error = self.load_data(self.data_file)
        if error:
            window['-AI_RESULT-'].print(f"❌ 数据加载失败: {error}")
            return
        
        window['-AI_RESULT-'].print("🤖 AI 分析中，请稍候...")
        
        # 分析
        result = analyzer.analyze_phenomenon(
            df, 
            title=values['-TITLE-'] or "实验报告",
            description=""
        )
        
        # 显示结果
        window['-AI_RESULT-'].print("=" * 60)
        window['-AI_RESULT-'].print(f"📊 实验现象:\n{result.phenomenon}")
        window['-AI_RESULT-'].print(f"\n📝 实验结论:\n{result.conclusion}")
        window['-AI_RESULT-'].print(f"\n📈 数据趋势:\n{result.trend}")
        window['-AI_RESULT-'].print(f"\n⚠️ 异常检测:\n{result.anomaly}")
        window['-AI_RESULT-'].print(f"\n💡 改进建议:\n{result.suggestion}")
        window['-AI_RESULT-'].print(f"\n🎯 置信度: {result.confidence:.2%}")
        window['-AI_RESULT-'].print("=" * 60)
        
        # 保存到临时变量
        self.ai_result = result
    
    def generate_report(self, window, values):
        """生成报告"""
        filepath = values['-FILE-']
        if not filepath:
            window['-LOG-'].print("❌ 请先选择数据文件！")
            return
        
        title = values['-TITLE-'] or "实验报告"
        author = values['-AUTHOR-']
        group = values['-GROUP-']
        
        # 获取模板
        template_name = values['-TEMPLATE-']
        template_key = "physics_basic"
        for k, v in self.templates.items():
            if v == template_name:
                template_key = k
                break
        
        # 检查是否使用自定义模板
        template_file = values['-TEMPLATE_FILE-']
        use_custom = bool(template_file) and "自定义模板" in template_name
        
        # 输出目录
        output_dir = values['-OUTPUT_DIR-'] or str(PROJECT_ROOT / "output")
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        window['-LOG-'].print(f"📂 加载数据: {filepath}")
        
        # 加载数据
        df, error = self.load_data(filepath)
        if error:
            window['-LOG-'].print(f"❌ 加载失败: {error}")
            return
        
        window['-LOG-'].print(f"✅ 数据加载成功: {df.shape[0]} 行 × {df.shape[1]} 列")
        
        # AI 分析（如果启用）
        ai_content = {}
        if values['-ENABLE_AI-'] and hasattr(self, 'ai_result'):
            ai_result = self.ai_result
            ai_content = {
                "phenomenon": ai_result.phenomenon,
                "conclusion": ai_result.conclusion,
                "trend": ai_result.trend,
                "suggestion": ai_result.suggestion
            }
            window['-LOG-'].print("🤖 已使用 AI 分析结果")
        
        # 生成图表
        chart_images = []
        if values['-GENERATE_CHART-']:
            window['-LOG-'].print("📊 生成图表...")
            x_col = values['-X_COL-']
            y_col = values['-Y_COL-']
            chart_type = values['-CHART_TYPE-']
            chart_title = values['-CHART_TITLE-'] or f"{y_col} vs {x_col}"
            
            if x_col and y_col:
                chart_gen = ChartGenerator(df)
                result = chart_gen.generate(x_col, [y_col], ChartConfig(
                    title=chart_title,
                    chart_type=chart_type
                ))
                chart_images.append(result)
                window['-LOG-'].print(f"   图表: {x_col} → {y_col}")
        
        # 生成 Word 报告
        if values['-OUTPUT_DOCX-']:
            window['-LOG-'].print("📝 生成 Word 报告...")
            
            if use_custom and template_file.endswith('.docx'):
                # 使用自定义 Word 模板
                from src.generators.word_generator import WordReportGenerator
                word_gen = WordReportGenerator("physics_basic")
                doc = word_gen.generate_report(
                    title=title,
                    author=author,
                    group=group,
                    conclusion=ai_content.get("conclusion", "请根据实验结果填写结论..."),
                    data_summary={}
                )
            else:
                word_gen = WordReportGenerator(template_key)
                doc = word_gen.generate_report(
                    title=title,
                    author=author,
                    group=group,
                    conclusion=ai_content.get("conclusion", "请根据实验结果填写结论..."),
                    data_summary={}
                )
            
            output_path = Path(output_dir) / f"{title}.docx"
            word_gen.save(str(output_path))
            window['-LOG-'].print(f"✅ 已保存: {output_path}")
        
        # 生成 HTML 报告
        if values['-OUTPUT_HTML-']:
            window['-LOG-'].print("🌐 生成 HTML 报告...")
            
            gen = ReportGenerator(template_key)
            gen.summarize_data(df)
            
            report = gen.generate_report(title, author, group, df)
            
            output_path = Path(output_dir) / f"{title}.html"
            gen.save_report(report, str(output_path))
            window['-LOG-'].print(f"✅ 已保存: {output_path}")
        
        # 生成 Markdown
        if values['-OUTPUT_MD-']:
            output_path = Path(output_dir) / f"{title}.md"
            window['-LOG-'].print(f"📄 Markdown: {output_path}")
        
        window['-LOG-'].print("\n🎉 报告生成完成！")
        window['-LOG-'].print("-" * 50)
    
    def run(self):
        """运行应用"""
        window = self.create_window()
        self.ai_result = None
        
        while True:
            event, values = window.read()
            
            if event in (sg.WIN_CLOSED, '-EXIT-'):
                break
            
            elif event == '-FILE-':
                filepath = values['-FILE-']
                df, error = self.load_data(filepath)
                
                if error:
                    window['-FILE_INFO-'].update(f"❌ {error}")
                else:
                    window['-FILE_INFO-'].update(f"✅ 已加载: {df.shape[0]} 行, {df.shape[1]} 列")
                    
                    # 更新列选项
                    cols = df.columns.tolist()
                    window['-X_COL-'].update(values=cols)
                    window['-Y_COL-'].update(values=cols)
                    
                    if cols:
                        window['-X_COL-'].update(set_to_index=0)
                        window['-Y_COL-'].update(set_to_index=min(1, len(cols)-1))
                    
                    # 更新预览
                    preview_data = df.head(10).values.tolist()
                    preview_headers = df.columns.tolist()
                    window['-PREVIEW-'].update(values=preview_data, 
                                             headings=preview_headers)
            
            elif event == '-TEMPLATE_FILE-':
                filepath = values['-TEMPLATE_FILE-']
                if filepath and Path(filepath).exists():
                    window['-TEMPLATE_INFO-'].update(f"✅ 已加载: {Path(filepath).name}")
            
            elif event == '-PARSE_TEMPLATE-':
                filepath = values['-TEMPLATE_FILE-']
                if not filepath:
                    window['-TEMPLATE_INFO-'].update("❌ 请先选择模板文件")
                else:
                    try:
                        result = self.parse_template(filepath)
                        vars_count = len(result['variables'])
                        window['-TEMPLATE_INFO-'].update(f"✅ 解析成功: 发现 {vars_count} 个变量")
                        window['-TEMPLATE_INFO-'].update(f"变量: {', '.join(result['variables'].keys())}")
                    except Exception as e:
                        window['-TEMPLATE_INFO-'].update(f"❌ 解析失败: {e}")
            
            elif event == '-SAMPLE-':
                sample_file = PROJECT_ROOT / "data" / "examples" / "欧姆定律数据.csv"
                if sample_file.exists():
                    window['-FILE-'].update(str(sample_file))
                    window['-TITLE-'].update("欧姆定律验证实验")
                    window['-AUTHOR-'].update("张三")
                    window['-GROUP-'].update("物理1班第3组")
            
            elif event == '-AI_ANALYZE-':
                self.run_ai_analysis(window, values)
            
            elif event == '-GENERATE-':
                self.generate_report(window, values)
            
            elif event == '-CLEAR-':
                window['-FILE-'].update('')
                window['-TEMPLATE_FILE-'].update('')
                window['-TITLE-'].update('')
                window['-AUTHOR-'].update('')
                window['-GROUP-'].update('')
                window['-X_COL-'].update(values=[])
                window['-Y_COL-'].update(values=[])
                window['-PREVIEW-'].update(values=[])
                window['-AI_RESULT-'].update('')
                window['-LOG-'].update('')
                window['-FILE_INFO-'].update('')
                window['-TEMPLATE_INFO-'].update('')
                self.data_file = None
                self.template_file = None
                self.ai_result = None
        
        window.close()


def main():
    """主入口"""
    app = LabReportApp()
    app.run()


if __name__ == "__main__":
    main()
