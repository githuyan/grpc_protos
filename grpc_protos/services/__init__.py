import sys
import os

# 由于 protoc 生成的代码中，引用的路径是相对路径，所以需要将当前目录添加到 sys.path 中
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
