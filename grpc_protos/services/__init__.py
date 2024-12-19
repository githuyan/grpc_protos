import importlib
import pkgutil
from pathlib import Path

# 当前模块路径
current_package = __name__
current_path = Path(__file__).parent

# 自动导入 services 目录下的所有子模块
for module_info in pkgutil.iter_modules([str(current_path)]):
    # 动态导入模块
    imported_module = importlib.import_module(
        f".{module_info.name}", package=current_package
    )
    globals()[module_info.name] = imported_module
