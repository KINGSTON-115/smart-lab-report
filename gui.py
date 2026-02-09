# 🧪 Smart Lab Report - Windows GUI 主程序（稳定版）
# Smart Lab Report - Stable Windows GUI Application

import sys
import os
from pathlib import Path

# 路径设置
if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
    os.chdir(os.path.dirname(sys.executable))
else:
    BASE_DIR = Path(__file__).parent.absolute()
    sys.path.insert(0, str(BASE_DIR))

# GUI 库导入（失败时给出清晰提示）
try:
    import PySimpleGUI as sg
except ImportError:
    print("=" * 60)
    print("❌ PySimpleGUI 未安装")
    print("=" * 60)
    print("\n请运行以下命令安装依赖：")
    print("  pip install PySimpleGUI")
    print("\n完整安装（推荐）：")
    print("  pip install -r requirements.txt")
    print("=" * 60)
    sys.exit(1)

# 数据处理
PANDAS_AVAILABLE = True
try:
    import pandas as pd
except ImportError:
    PANDAS_AVAILABLE = False


def check_dependencies():
    """检查依赖是否安装"""
    issues = []
    
    if not PANDAS_AVAILABLE:
        issues.append("pandas - 数据处理")
    
    return issues


class LabReportApp:
    """实验报告生成器 GUI 应用"""
    
    def __init__(self):
        self.data_file = None
        self.template = "physics_basic"
        
        # 模板映射
        self.templates = {
            "physics_basic": "物理实验基础模板",
            "chemistry_basic": "化学实验基础模板",
            "biology_basic": "生物实验基础模板",
            "cs_algorithm": "计算机算法模板",
            "engineering_basic": "工程实验基础模板",
        }
        
        # 图表类型
        self.chart_types = ["line", "scatter", "bar", "histogram"]
        
        # 输出格式
        self.output_formats = {
            "Word (.docx)": "docx",
            "HTML": "html",
            "Markdown": "md",
            "PDF": "pdf"
        }
        
        self._setup_theme()
    
    def _setup_theme(self):
        """设置主题"""
        sg.theme('LightBlue3')
    
    def create_window(self):
        """创建主窗口"""
        
        # 顶部标题
        title_layout = [
            [sg.Text("🧪 Smart Lab Report", font=('Microsoft YaHei', 24, 'bold'), 
                     justification='center', expand_x=True)],
            [sg.Text("智能实验报告生成器 - 一键生成 Word/HTML/PDF", font=('Microsoft YaHei', 11),
                     text_color='#666666', justification='center', expand_x=True)]
        ]
        
        # ===== 第一行：数据文件 =====
        file_section = [
            [sg.Text("📁 实验数据", font=('Microsoft YaHei', 12, 'bold'))],
            [
                sg.Input(key='-FILE-', size=(50, 1), enable_events=True,
                        placeholder='选择 CSV 或 Excel 文件...',
                        text_color='#333333'),
                sg.FileBrowse("浏览", file_types=(("数据文件", "*.csv *.xlsx"), ("所有文件", "*.*")),
                             initial_folder=str(BASE_DIR / "data"))
            ],
            [sg.Text(key='-FILE_INFO-', size=(60, 1), text_color='#0066CC',
                    text='选择数据文件开始')]
        ]
        
        # ===== 第二行：报告信息 =====
        info_section = [
            [sg.Text("📝 报告信息", font=('Microsoft YaHei', 12, 'bold'))],
            [
                sg.Text("标题:", size=(6, 1)),
                sg.Input(key='-TITLE-', size=(28, 1), 
                        default_text="实验报告",
                        text_color='#333333'),
                sg.Text("作者:", size=(6, 1)),
                sg.Input(key='-AUTHOR-', size=(15, 1), text_color='#333333'),
            ],
            [
                sg.Text("组别:", size=(6, 1)),
                sg.Input(key='-GROUP-', size=(28, 1), text_color='#333333'),
                sg.Text("模板:", size=(6, 1)),
                sg.Combo(list(self.templates.values()), 
                        key='-TEMPLATE-', size=(18, 1),
                        default_value=list(self.templates.values())[0],
                        readonly=True)
            ]
        ]
        
        # ===== 第三行：数据预览 =====
        preview_section = [
            [sg.Text("📊 数据预览", font=('Microsoft YaHei', 12, 'bold'))],
            [sg.Table(key='-PREVIEW-', 
                     headings=['数据预览'],
                     values=[['选择数据文件后显示预览']],
                     size=(65, 4),
                     num_rows=4,
                     display_row_numbers=False,
                     enable_events=False)]
        ]
        
        # ===== 第四行：输出设置 =====
        output_section = [
            [sg.Text("📤 输出格式", font=('Microsoft YaHei', 12, 'bold'))],
            [
                sg.Checkbox('Word (.docx) ⭐', key='-OUTPUT_DOCX-', default=True,
                           tooltip='生成 Word 文档'),
                sg.Checkbox('HTML', key='-OUTPUT_HTML-', default=True,
                           tooltip='生成网页版报告'),
                sg.Checkbox('Markdown', key='-OUTPUT_MD-', default=False,
                           tooltip='生成 Markdown 格式'),
                sg.Checkbox('PDF', key='-OUTPUT_PDF-', default=False,
                           tooltip='生成 PDF 文档'),
            ],
            [
                sg.FolderBrowse("📂 输出目录", key='-OUTPUT_DIR-', 
                               initial_folder=str(BASE_DIR / "output"))
            ]
        ]
        
        # ===== 第五行：状态与日志 =====
        status_section = [
            [sg.Text("ℹ️ 状态", font=('Microsoft YaHei', 10, 'bold'))],
            [sg.Text(key='-STATUS-', size=(70, 1), text_color='#0066CC',
                    text='准备就绪，请选择数据文件')]
        ]
        
        log_section = [
            [sg.Text("📜 日志", font=('Microsoft YaHei', 10, 'bold'))],
            [sg.Multiline(key='-LOG-', size=(70, 8), font=('Consolas', 9),
                         autoscroll=True, disabled=True, text_color='#333333')]
        ]
        
        # ===== 按钮行 =====
        button_section = [
            [
                sg.Button("🚀 生成报告", key='-GENERATE-', 
                        button_color=('white', '#27AE60'), 
                        font=('Microsoft YaHei', 12, 'bold'),
                        size=(15, 1),
                        pad=(10, 5)),
                sg.Button("🧪 AI 分析", key='-AI_ANALYZE-', 
                        button_color=('white', '#3498DB'), 
                        font=('Microsoft YaHei', 11),
                        size=(12, 1),
                        pad=(10, 5),
                        tooltip='使用 AI 分析实验数据（需要 API Key）'),
                sg.Button("🗑️ 清空", key='-CLEAR-', 
                        font=('Microsoft YaHei', 11),
                        size=(10, 1),
                        pad=(10, 5)),
                sg.Button("❌ 退出", key='-EXIT-', 
                        font=('Microsoft YaHei', 11),
                        size=(10, 1),
                        pad=(10, 5)),
            ]
        ]
        
        # 组装完整布局
        layout = [
            [sg.Column(title_layout, justification='center', expand_x=True)],
            [sg.HorizontalSeparator(color='#CCCCCC')],
            [sg.Frame("数据选择", file_section, expand_x=True, 
                     relief=sg.RELIEF_GROOVE, border_width=1)],
            [sg.Frame("报告设置", info_section, expand_x=True,
                     relief=sg.RELIEF_GROOVE, border_width=1)],
            [sg.Frame("数据预览", preview_section, expand_x=True,
                     relief=sg.RELIEF_GROOVE, border_width=1)],
            [sg.Frame("输出设置", output_section, expand_x=True,
                     relief=sg.RELIEF_GROOVE, border_width=1)],
            [sg.Frame("处理状态", status_section, expand_x=True,
                     relief=sg.RELIEF_GROOVE, border_width=1)],
            [sg.Frame("处理日志", log_section, expand_x=True,
                     relief=sg.RELIEF_GROOVE, border_width=1)],
            [sg.Column(button_section, justification='center', expand_x=True)],
        ]
        
        # 创建窗口
        window = sg.Window(
            "🧪 Smart Lab Report - 智能实验报告生成器",
            layout,
            size=(550, 750),
            resizable=True,
            finalize=True,
            grab_anywhere=False
        )
        
        return window
    
    def load_data(self, filepath: str):
        """加载数据文件"""
        if not PANDAS_AVAILABLE:
            return None, "pandas 未安装"
        
        ext = Path(filepath).suffix.lower()
        
        try:
            if ext == '.csv':
                df = pd.read_csv(filepath)
            elif ext == '.xlsx':
                df = pd.read_excel(filepath)
            else:
                return None, f"不支持的文件格式: {ext}"
            
            self.data_file = filepath
            return df, None
            
        except Exception as e:
            return None, str(e)
    
    def log(self, window, message, level='info'):
        """日志输出"""
        colors = {
            'info': '#333333',
            'success': '#27AE60',
            'warning': '#F39C12',
            'error': '#E74C3C'
        }
        
        prefix = {
            'info': 'ℹ️',
            'success': '✅',
            'warning': '⚠️',
            'error': '❌'
        }
        
        window['-LOG-'].print(f"{prefix.get(level, 'ℹ️')} {message}",
                             text_color=colors.get(level, '#333333'))
    
    def generate_report(self, window, values):
        """生成报告"""
        if not self.data_file:
            self.log(window, "请先选择数据文件！", 'warning')
            return
        
        # 获取输入
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
        
        # 输出目录
        output_dir = values['-OUTPUT_DIR-'] or str(BASE_DIR / "output")
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        self.log(window, f"开始生成报告: {title}")
        self.log(window, f"模板: {template_name}")
        self.log(window, f"输出目录: {output_dir}")
        
        # 加载数据
        df, error = self.load_data(self.data_file)
        if error:
            self.log(window, f"数据加载失败: {error}", 'error')
            return
        
        self.log(window, f"数据加载成功: {df.shape[0]} 行 × {df.shape[1]} 列", 'success')
        
        # 获取数值列
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        
        if not numeric_cols:
            self.log(window, "未找到数值列，无法生成图表", 'warning')
        
        # 生成 Word 报告
        if values['-OUTPUT_DOCX-']:
            self.log(window, "生成 Word 报告...")
            try:
                from src.generators.word_generator import WordReportGenerator
                
                word_gen = WordReportGenerator(template_key)
                doc = word_gen.generate_report(
                    title=title,
                    author=author,
                    group=group,
                    conclusion="请根据实验结果填写结论...",
                    data_summary={}
                )
                
                output_path = Path(output_dir) / f"{title}.docx"
                word_gen.save(str(output_path))
                self.log(window, f"✅ Word 报告已保存: {output_path.name}", 'success')
                
            except Exception as e:
                self.log(window, f"Word 生成失败: {e}", 'error')
        
        # 生成 HTML 报告
        if values['-OUTPUT_HTML-']:
            self.log(window, "生成 HTML 报告...")
            try:
                from src.generators.report_generator import ReportGenerator
                
                gen = ReportGenerator(template_key)
                gen.summarize_data(df)
                report = gen.generate_report(title, author, group, df)
                
                output_path = Path(output_dir) / f"{title}.html"
                gen.save_report(report, str(output_path))
                self.log(window, f"✅ HTML 报告已保存: {output_path.name}", 'success')
                
            except Exception as e:
                self.log(window, f"HTML 生成失败: {e}", 'error')
        
        # 完成
        self.log(window, "=" * 40, 'info')
        self.log(window, "🎉 报告生成完成！", 'success')
        self.log(window, f"📂 输出目录: {output_dir}", 'info')
        self.log(window, "=" * 40, 'info')
    
    def run(self):
        """运行应用"""
        window = self.create_window()
        
        while True:
            event, values = window.read()
            
            if event in (sg.WIN_CLOSED, '-EXIT-'):
                break
            
            elif event == '-FILE-':
                filepath = values['-FILE-']
                if filepath:
                    df, error = self.load_data(filepath)
                    
                    if error:
                        window['-FILE_INFO-'].update(f"❌ {error}", text_color='#E74C3C')
                    else:
                        window['-FILE_INFO-'].update(
                            f"✅ 已加载: {df.shape[0]} 行, {df.shape[1]} 列",
                            text_color='#27AE60'
                        )
                        
                        # 更新预览
                        preview_data = df.head(10).values.tolist()
                        preview_headers = df.columns.tolist()
                        window['-PREVIEW-'].update(
                            values=preview_data,
                            headings=preview_headers
                        )
                        self.log(window, f"数据预览已更新 ({df.shape[0]} 行)")
            
            elif event == '-GENERATE-':
                self.generate_report(window, values)
            
            elif event == '-CLEAR-':
                window['-FILE-'].update('')
                window['-TITLE-'].update('实验报告')
                window['-AUTHOR-'].update('')
                window['-GROUP-'].update('')
                window['-PREVIEW-'].update(values=[['选择数据文件后显示预览']])
                window['-LOG-'].update('')
                window['-FILE_INFO-'].update('选择数据文件开始', text_color='#0066CC')
                self.data_file = None
                self.log(window, "已清空所有输入")
            
            elif event == '-AI_ANALYZE-':
                self.log(window, "AI 分析功能需要 API Key，请在代码中配置", 'warning')
        
        window.close()


def main():
    """主入口"""
    print("=" * 60)
    print("🧪 Smart Lab Report - 智能实验报告生成器")
    print("=" * 60)
    
    # 检查依赖
    issues = check_dependencies()
    if issues:
        print("⚠️ 缺少依赖:")
        for issue in issues:
            print(f"   - {issue}")
        print("\n请运行: pip install -r requirements.txt")
        print("=" * 60)
    
    # 启动 GUI
    try:
        app = LabReportApp()
        app.run()
    except Exception as e:
        print(f"\n❌ 启动失败: {e}")
        import traceback
        traceback.print_exc()
        input("\n按 Enter 退出...")


if __name__ == "__main__":
    main()
