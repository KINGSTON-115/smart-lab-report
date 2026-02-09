# Windows GUI Entry Point
import sys
import os

# 确保编码正确
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 切换到程序目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from gui import main

if __name__ == "__main__":
    main()
