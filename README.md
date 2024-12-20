# gRPC Protos

gRPC service with Protocol Buffers

## 安装

您可以通过以下命令安装本项目：

```bash
pip install -e ../grpc_protos
```

## 使用方法

在您的 Python 代码中，您可以通过以下方式导入服务模块：

```python
from grpc_protos.services.user_service import user_pb2_grpc
```

### 启动 gRPC 服务

首先，您需要启动 gRPC 服务。以下是一个简单的示例，展示如何启动服务：

```python
import grpc
from concurrent import futures
from grpc_protos.services.user_service import user_pb2_grpc

class UserService(user_pb2_grpc.UserServiceServicer):
    def CreateUser(self, request, context):
        return common_pb2.BaseResponse(code=0, message="User created successfully")

    def GetUser(self, request, context):
        return user_pb2.User(
            user_id=request.user_id,
            username="test_user",
            email="test@example.com",
            created_at=1234567890,
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(UserService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server is running on port 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
```

### 创建 gRPC 客户端

接下来，您可以创建一个简单的客户端来测试与服务的通信：

```python
import grpc
from grpc_protos.services.user_service import user_pb2_grpc, user_pb2

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = user_pb2_grpc.UserServiceStub(channel)

    request = user_pb2.CreateUserRequest(
        username="test_user",
        email="test@example.com",
        password="secure_password"
    )

    response = stub.CreateUser(request)
    print(response.message)

if __name__ == "__main__":
    run()
```

### 测试 gRPC 服务

项目中包含了测试用例，您可以使用 `pytest` 来运行测试，验证服务的基本通信功能是否正常：

```bash
pytest tests/test_grpc_connection.py
```

### 示例代码

以下是一个使用 gRPC 服务的完整示例：

```python
import grpc
from grpc_protos.services.user_service import user_pb2_grpc, user_pb2

def create_user():
    channel = grpc.insecure_channel('localhost:50051')
    stub = user_pb2_grpc.UserServiceStub(channel)

    request = user_pb2.CreateUserRequest(
        username="test_user",
        email="test@example.com",
        password="secure_password"
    )

    response = stub.CreateUser(request)
    print(response.message)

if __name__ == "__main__":
    create_user()
```

## 目录结构

```
.
├── grpc_protos/      # gRPC Protos 项目目录
│   ├── __init__.py   # 初始化文件
│   ├── protos/       # Proto 文件目录
│   │   ├── common/   # 公共 Proto 文件
│   │   └── services/ # 服务相关 Proto 文件
│   └── services/     # 生成的 Python 代码
├── scripts/          # 开发工具脚本
│   ├── dev.py        # 开发脚本
│   └── gen_proto.py  # Proto 生成脚本
├── tests/            # 测试文件
└── README.md         # 项目说明文档
```

## 开发工具使用

项目提供了多个开发工具命令，都集成在 `scripts/dev.py` 中：

### Proto 代码生成

使用以下命令生成 Proto 对应的 Python 代码：

```bash
python -m scripts.gen_proto [--source-dir PROTO目录] [--target-dir 输出目录]
```

参数说明：
- `--source-dir`: Proto 文件所在目录（默认: protos）
- `--target-dir`: 生成代码的目标目录（默认: services）

### 代码格式化

```bash
python -m scripts.dev format
```

这个命令会：
- 使用 black 格式化 Python 代码
- 使用 isort 对导入语句进行排序

### 代码检查

```bash
python -m scripts.dev lint
```

这个命令会：
- 使用 ruff 进行代码风格检查
- 使用 mypy 进行类型检查

### 运行测试

```bash
python -m scripts.dev test
```

### 清理生成的文件

```bash
python -m scripts.dev clean
```

这个命令会清理：
- `__pycache__` 目录
- `.pyc`、`.pyo`、`.pyi` 文件
- 生成的 Proto 代码（`*_pb2.py` 和 `*_pb2_grpc.py`）

## CI/CD

项目配置了两个 GitHub Actions 工作流：

1. `CI/CD` 工作流：
   - 在 main 分支的推送和 PR 时触发
   - 在多个 Python 版本上运行测试
   - 执行代码格式检查和类型检查
   - 在 main 分支更新时构建包

2. `Proto CI` 工作流：
   - 在 Proto 相关文件变更时触发
   - 检查 Proto 代码生成是否正常
   - 对生成的代码进行类型检查
   - 运行相关测试

## 开发流程建议

1. 在 `protos/` 目录下编写或修改 Proto 文件
2. 使用 `gen_proto.py` 生成代码
3. 编写测试代码
4. 运行格式化和代码检查
5. 提交代码前运行完整测试套件

## 注意事项

- 每次修改 Proto 文件后需要重新生成代码
- 提交代码前建议运行完整的代码检查和测试
- 生成的代码不建议手动修改，应该修改 Proto 文件
```

这个文档：
1. 介绍了项目的基本结构
2. 详细说明了各个开发工具的使用方法
3. 解释了 CI/CD 配置
4. 提供了开发流程建议
5. 包含了重要的注意事项

你可以根据实际需求继续补充或修改这个文档。