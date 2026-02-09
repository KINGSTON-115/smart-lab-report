# 📚 实验模板库
# Experiment Template Library

from pathlib import Path

TEMPLATE_DIR = Path(__file__).parent

def list_templates(category: str = None):
    """列出所有模板"""
    templates = {}
    
    if category:
        category_dir = TEMPLATE_DIR / category
        if category_dir.exists():
            for f in category_dir.glob("*.md"):
                templates[f.stem] = f.read_text(encoding='utf-8')
    else:
        # 遍历所有分类
        for cat_dir in TEMPLATE_DIR.iterdir():
            if cat_dir.is_dir():
                for f in cat_dir.glob("*.md"):
                    templates[f"{cat_dir.name}/{f.stem}"] = f.read_text(encoding='utf-8')
    
    return templates

def get_template(template_path: str) -> str:
    """获取模板内容"""
    # 支持 "physics/ohms_law" 或 "physics_ohms_law" 格式
    template_path = template_path.replace("/", "_")
    
    # 先检查子目录
    for cat_dir in TEMPLATE_DIR.iterdir():
        if cat_dir.is_dir():
            template_file = cat_dir / f"{template_path}.md"
            if template_file.exists():
                return template_file.read_text(encoding='utf-8')
    
    # 检查主模板
    main_template = TEMPLATE_DIR / f"{template_path}.md"
    if main_template.exists():
        return main_template.read_text(encoding='utf-8')
    
    return None

__all__ = ["list_templates", "get_template"]
