# -*- coding: utf-8 -*-
"""
Smart Lab Report - Windows GUI Simplified Test
简化版打包测试
"""

import sys
import os

# 确保路径正确
if getattr(sys, 'frozen', False):
    # 打包后的路径
    BASE_DIR = sys._MEIPASS
    os.chdir(os.path.dirname(sys.executable))
else:
    # 开发模式路径
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, BASE_DIR)

# 导入 PySimpleGUI
try:
    import PySimpleGUI as sg
except ImportError:
    print("错误: PySimpleGUI 未安装")
    print("请运行: pip install PySimpleGUI")
    sys.exit(1)

def main():
    """主函数"""
    
    # 设置主题
    sg.theme('LightBlue3')
    
    # 布局
    layout = [
        [sg.Text("🧪 Smart Lab Report - 智能实验报告生成器", 
                font=('Microsoft YaHei', 20, 'bold'), justification='center')],
        [sg.Text("Windows exe 打包测试版本", font=('Microsoft YaHei', 10), 
                text_color='gray', justification='center')],
        
        [sg.HorizontalSeparator()],
        
        [sg.Frame("数据文件", [
            [sg.FileBrowse("选择数据", file_types=(("CSV", "*.csv"), ("Excel", "*.xlsx")))],
            [sg.Input(key='-FILE-', size=(50, 1), disabled=True)],
            [sg.Text(key='-STATUS-', size=(50, 1), text_color='blue')]
        ], expand_x=True)],
        
        [sg.Frame("报告信息", [
            [sg.Text("标题:"), sg.Input(key='-TITLE-', size=(30, 1), default_text="实验报告")],
            [sg.Text("作者:"), sg.Input(key='-AUTHOR-', size=(20, 1))],
            [sg.Text("组别:"), sg.Input(key='-GROUP-', size=(20, 1))]
        ], expand_x=True)],
        
        [sg.Frame("模板", [
            [sg.Combo([
                "物理实验基础模板",
                "化学实验基础模板", 
                "生物实验基础模板",
                "计算机算法模板",
                "工程实验基础模板"
            ], key='-TEMPLATE-', size=(25, 1), default_value="物理实验基础模板")]
        ], expand_x=True)],
        
        [sg.Frame("输出", [
            [sg.Checkbox('Word (.docx)', key='-DOCX-', default=True)],
            [sg.Checkbox('HTML', key='-HTML-', default=True)],
            [sg.Checkbox('PDF', key='-PDF-', default=True)],
        ], expand_x=True)],
        
        [sg.HorizontalSeparator()],
        
        [sg.Button("🚀 生成报告", key='-GENERATE-', 
                  button_color=('white', '#27ae60'), font=('Microsoft YaHei', 12, 'bold'),
                  size=(15, 1)),
         sg.Button("❌ 退出", key='-EXIT-', size=(10, 1))],
        
        [sg.Multiline(key='-LOG-', size=(60, 10), font=('Consolas', 9),
                     autoscroll=True, disabled=True)]
    ]
    
    # 创建窗口
    window = sg.Window(
        "Smart Lab Report - 智能实验报告生成器",
        layout,
        size=(500, 550),
        resizable=True,
        finalize=True
    )
    
    # 事件循环
    while True:
        event, values = window.read()
        
        if event in (sg.WIN_CLOSED, '-EXIT-'):
            break
        
        elif event == '-GENERATE-':
            file_path = values['-FILE-']
            if not file_path:
                window['-LOG-'].print("⚠️ 请先选择数据文件！")
                continue
            
            window['-LOG-'].print("✅ 开始生成报告...")
            window['-LOG-'].print(f"文件: {file_path}")
            window['-LOG-'].print(f"标题: {values['-TITLE-']}")
            window['-LOG-'].print(f"作者: {values['-AUTHOR-']}")
            window['-LOG-'].print("🎉 报告生成完成！")
            
            sg.popup("✅ 报告生成完成！", "输出目录: output/")
    
    window.close()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
        input("按 Enter 退出...")
