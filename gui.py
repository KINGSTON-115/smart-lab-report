# 🧪 Smart Lab Report - Windows GUI 主程序
# Smart Lab Report - Windows GUI Main Application

import sys
import os
from pathlib import Path
from datetime import datetime
import threading

# 添加项目路径
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    import PySimpleGUI as sg
except ImportError:
    print("请安装 GUI 依赖: pip install PySimpleGUI")
    sys.exit(1)

from src.generators.report_generator import ReportGenerator
from src.generators.chart_generator import ChartGenerator, ChartConfig
from src.generators.word_generator import WordReportGenerator


class LabReportApp:
    """实验报告生成器 GUI 应用"""
    
    def __init__(self):
        self.data_file = None
        self.template = "physics_basic"
        self.data_preview = None
        
        # 模板列表
        self.templates = {
            "physics_basic": "物理实验基础模板",
            "chemistry_basic": "化学实验基础模板",
            "biology_basic": "生物实验基础模板",
            "cs_algorithm": "计算机算法模板",
            "engineering_basic": "工程实验基础模板",
        }
        
        # 图表类型
        self.chart_types = ["line", "scatter", "bar", "histogram"]
        
        self._setup_theme()
    
    def _setup_theme(self):
        """设置主题"""
        sg.theme('LightBlue3')
    
    def create_window(self):
        """创建主窗口"""
        
        # 标题
        title = [[sg.Text("🧪 智能实验报告生成器", font=('Microsoft YaHei', 20, 'bold'), 
                         justification='center', expand_x=True)],
                 [sg.Text("自动生成实验报告 - 支持 Word/HTML/PDF", font=('Microsoft YaHei', 10),
                         justification='center', text_color='gray')]]
        
        # ===== 第一行：数据文件 =====
        file_section = [
            [sg.Text("📁 实验数据文件:", font=('Microsoft YaHei', 11, 'bold'))],
            [
                sg.Input(key='-FILE-', size=(50, 1), enable_events=True,
                        placeholder='选择 CSV/Excel/JSON 文件...'),
                sg.FileBrowse("浏览", file_types=(("数据文件", "*.csv *.xlsx *.json"), ("所有文件", "*.*")),
                             initial_folder=str(PROJECT_ROOT / "data")),
                sg.Button("示例数据", key='-SAMPLE-')
            ],
            [sg.Text(key='-FILE_INFO-', size=(60, 1), text_color='blue')]
        ]
        
        # ===== 第二行：报告信息 =====
        info_section = [
            [sg.Text("📝 报告信息:", font=('Microsoft YaHei', 11, 'bold'))],
            [
                sg.Text("标题:"), sg.Input(key='-TITLE-', size=(25, 1), 
                                         placeholder='例如: 欧姆定律验证实验'),
                sg.Text("作者:"), sg.Input(key='-AUTHOR-', size=(15, 1), placeholder='你的名字'),
            ],
            [
                sg.Text("组别:"), sg.Input(key='-GROUP-', size=(25, 1), placeholder='例如: 物理1班第3组'),
                sg.Text("模板:"), sg.Combo(list(self.templates.values()), 
                                         key='-TEMPLATE-', size=(20, 1),
                                         default_value=list(self.templates.values())[0])
            ]
        ]
        
        # ===== 第三行：图表设置 =====
        chart_section = [
            [sg.Text("📊 图表设置:", font=('Microsoft YaHei', 11, 'bold'))],
            [
                sg.Text("X轴:"), sg.Combo(key='-X_COL-', values=[], size=(15, 1)),
                sg.Text("Y轴:"), sg.Combo(key='-Y_COL-', values=[], size=(15, 1)),
                sg.Text("类型:"), sg.Combo(self.chart_types, key='-CHART_TYPE-', 
                                          default_value='scatter', size=(10, 1)),
            ],
            [
                sg.Text("图表标题:"), sg.Input(key='-CHART_TITLE-', size=(30, 1)),
                sg.Checkbox('生成图表', key='-GENERATE_CHART-', default=True)
            ]
        ]
        
        # ===== 第四行：输出设置 =====
        output_section = [
            [sg.Text("📤 输出设置:", font=('Microsoft YaHei', 11, 'bold'))],
            [
                sg.Checkbox('Word (.docx)', key='-OUTPUT_DOCX-', default=True),
                sg.Checkbox('HTML', key='-OUTPUT_HTML-', default=True),
                sg.Checkbox('Markdown', key='-OUTPUT_MD-', default=False),
                sg.FolderBrowse("输出文件夹", key='-OUTPUT_DIR-', 
                               initial_folder=str(PROJECT_ROOT / "output")),
            ]
        ]
        
        # ===== 数据预览 =====
        preview_section = [
            [sg.Text("📋 数据预览:", font=('Microsoft YaHei', 11, 'bold'))],
            [sg.Table(key='-PREVIEW-', values=[], headings=['数据预览将在这里显示'],
                     size=(80, 6), num_rows=6, max_col_width=20,
                     display_row_numbers=False, enable_events=False)]
        ]
        
        # ===== 日志输出 =====
        log_section = [
            [sg.Text("📜 生成日志:", font=('Microsoft YaHei', 11, 'bold'))],
            [sg.Multiline(key='-LOG-', size=(80, 8), font=('Consolas', 9),
                         autoscroll=True, disabled=True)]
        ]
        
        # ===== 按钮 =====
        button_section = [
            [
                sg.Button("🚀 生成报告", key='-GENERATE-', 
                        button_color=('white', '#27ae60'), font=('Microsoft YaHei', 12, 'bold'),
                        size=(15, 1)),
                sg.Button("🗑️ 清空", key='-CLEAR-', size=(10, 1)),
                sg.Button("❌ 退出", key='-EXIT-', size=(10, 1))
            ]
        ]
        
        # 组装布局
        layout = [
            [sg.Column(title, justification='center', expand_x=True)],
            [sg.HorizontalSeparator()],
            [sg.Frame("数据文件", file_section, expand_x=True)],
            [sg.Frame("报告信息", info_section, expand_x=True)],
            [sg.Frame("图表设置", chart_section, expand_x=True)],
            [sg.Frame("输出格式", output_section, expand_x=True)],
            [sg.Frame("预览", preview_section, expand_x=True)],
            [sg.Frame("日志", log_section, expand_x=True)],
            [sg.Column(button_section, justification='center', expand_x=True)],
        ]
        
        # 创建窗口
        window = sg.Window(
            "智能实验报告生成器 - Smart Lab Report",
            layout,
            size=(700, 850),
            resizable=True,
            finalize=True,
            icon=None  # 可以添加图标
        )
        
        return window
    
    def load_data(self, filepath: str):
        """加载数据文件"""
        ext = Path(filepath).suffix.lower()
        
        try:
            if ext == '.csv':
                import pandas as pd
                df = pd.read_csv(filepath)
            elif ext == '.xlsx':
                import pandas as pd
                df = pd.read_excel(filepath)
            elif ext == '.json':
                import pandas as pd
                df = pd.read_json(filepath)
            else:
                return None, "不支持的文件格式"
            
            self.data_file = filepath
            return df, None
            
        except Exception as e:
            return None, str(e)
    
    def generate_report(self, window, values):
        """生成报告"""
        # 获取输入
        filepath = values['-FILE-']
        if not filepath:
            window['-LOG-'].print("❌ 请先选择数据文件！")
            return
        
        title = values['-TITLE-'] or "实验报告"
        author = values['-AUTHOR-']
        group = values['-GROUP-']
        template_name = values['-TEMPLATE-']
        
        # 获取模板 key
        template_key = [k for k, v in self.templates.items() if v == template_name][0]
        
        # 输出目录
        output_dir = values['-OUTPUT_DIR-'] or str(PROJECT_ROOT / "output")
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # 日志
        window['-LOG-'].print(f"📂 加载数据: {filepath}")
        
        # 加载数据
        df, error = self.load_data(filepath)
        if error:
            window['-LOG-'].print(f"❌ 加载失败: {error}")
            return
        
        window['-LOG-'].print(f"✅ 数据加载成功: {df.shape[0]} 行 × {df.shape[1]} 列")
        
        # 生成图表
        charts = []
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
                charts.append(result)
                window['-LOG-'].print(f"   图表: {x_col} → {y_col}")
        
        # 生成 Word 报告
        if values['-OUTPUT_DOCX-']:
            window['-LOG-'].print("📝 生成 Word 报告...")
            
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
        
        window['-LOG-'].print("🎉 报告生成完成！")
        window['-LOG-'].print("-" * 50)
    
    def run(self):
        """运行应用"""
        window = self.create_window()
        
        while True:
            event, values = window.read()
            
            if event in (sg.WIN_CLOSED, '-EXIT-'):
                break
            
            elif event == '-FILE-':
                # 加载数据并更新选项
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
            
            elif event == '-SAMPLE-':
                # 使用示例数据
                sample_file = PROJECT_ROOT / "data" / "examples" / "欧姆定律数据.csv"
                if sample_file.exists():
                    window['-FILE-'].update(str(sample_file))
                    window['-TITLE-'].update("欧姆定律验证实验")
                    window['-AUTHOR-'].update("张三")
                    window['-GROUP-'].update("物理1班第3组")
            
            elif event == '-GENERATE-':
                self.generate_report(window, values)
            
            elif event == '-CLEAR-':
                window['-FILE-'].update('')
                window['-TITLE-'].update('')
                window['-AUTHOR-'].update('')
                window['-GROUP-'].update('')
                window['-X_COL-'].update(values=[])
                window['-Y_COL-'].update(values=[])
                window['-PREVIEW-'].update(values=[])
                window['-LOG-'].update('')
                self.data_file = None
        
        window.close()


def main():
    """主入口"""
    app = LabReportApp()
    app.run()


if __name__ == "__main__":
    main()
