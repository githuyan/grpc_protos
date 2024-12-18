# Protocol Buffers CI/CD 工作流程

## 概述
本文档描述了 Python 项目中 Protocol Buffers (.proto 文件) 的 CI/CD 自动化管理流程，确保客户端和服务端始终使用统一的接口定义。

## 工作流程

### 1. Proto 文件管理
- 项目结构：
项目根目录/
├── protos/                    # 存放所有 .proto 文件
│   ├── common/
│   │   └── base.proto
│   └── user_service/
│       └── user.proto
├── services/                  # 存放生成的 Python 代码
│   ├── common/
│   │   ├── __init__.py
│   │   ├── base_pb2.py
│   │   └── base_pb2.pyi
│   ├── user_service/
│   │   ├── __init__.py
│   │   ├── user_pb2.py
│   │   ├── user_pb2_grpc.py
│   │   └── user_pb2.pyi
│   └── utils/
│       ├── __init__.py
│       └── grpc_helpers.py
├── tests/
│   ├── __init__.py
│   ├── test_user_service.py
│   └── conftest.py
├── docs/
│   ├── proto_guidelines.md
│   └── development.md
├── .gitignore
├── requirements.txt
└── pyproject.toml

### 2. CI/CD 自动化流程

#### 2.1 环境依赖
txt:requirements.txt
grpcio-tools>=1.59.0
mypy-protobuf>=3.5.0 # 用于生成类型提示

#### 2.2 提交阶段
1. 开发人员提交 .proto 文件变更
2. 触发 CI 流水线
3. 自动执行以下检查：
   - Proto 语法检查
   - 向后兼容性验证
   - API 破坏性变更检测

#### 2.3 构建阶段
1. 自动生成 Python 代码：
   - 生成 gRPC 服务代码 (_pb2_grpc.py)
   - 生成消息类代码 (_pb2.py)
   - 生成类型提示文件 (_pb2.pyi)
     - 需要安装 mypy-protobuf 包
     - 使用 --mypy_out 参数指定输出目录
     - 可以通过 mypy.proto 文件配置类型生成选项
     - 支持为字段添加类型注解
     - 生成的 .pyi 文件包含完整类型信息
2. 运行单元测试
3. 类型检查 (mypy)

#### 2.4 发布阶段
1. 自动更新生成的代码
2. 更新版本号
3. 发布到 PyPI（如需要）

### 3. 代码生成命令
生成 Python gRPC 代码
python -m grpc_tools.protoc \
--proto_path=proto \
--python_out=generated/proto \
--grpc_python_out=generated/proto \
--mypy_out=generated/proto \
proto//.proto

### 4. 示例 CI/CD 配置
```yaml
name: Proto CI/CD

on:
  push:
    paths:
      - 'proto/**'

jobs:
  proto-ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      
      - name: Lint proto files
        run: |
          pip install buf
          buf lint proto
      
      - name: Generate Python code
        run: |
          python -m grpc_tools.protoc \
            --proto_path=proto \
            --python_out=generated/proto \
            --grpc_python_out=generated/proto \
            --mypy_out=generated/proto \
            proto/**/*.proto
      
      - name: Run tests
        run: python -m pytest tests/
      
      - name: Type check
        run: mypy generated/proto
```

## 最佳实践
1. Proto 文件命名规范
   - 使用 snake_case
   - 文件名应与服务名对应
   - 例如：user_service.proto

2. Python 包导入处理
generated/
proto/
init.py
user_pb2.py
user_pb2_grpc.py

3. 版本控制
   - 使用语义化版本号
   - 在 proto 文件中使用 API 版本号
   ```protobuf
   syntax = "proto3";
   
   package myservice.v1;
   ```

4. 类型提示
   - 始终生成 .pyi 类型提示文件
   - 在代码中使用类型注解

## 故障排除

### 常见问题
1. 导入错误
解决方案：添加 init.py 并设置 PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:${PWD}/generated"

2. 生成代码冲突
解决方案：生成前清理目录
rm -rf generated/proto/*

### 有用的工具
- buf: 现代 Protocol Buffers 工具链
- mypy-protobuf: 类型提示生成
- grpcio-tools: Python gRPC 工具