import pytest
import grpc
from services.utils.grpc_helpers import create_channel

@pytest.fixture
def grpc_channel():
    """创建测试用的 gRPC 通道"""
    channel = create_channel("localhost:50051")
    yield channel
    channel.close()

@pytest.fixture
def grpc_server():
    """创建测试用的 gRPC 服务器"""
    server = grpc.server(grpc.ThreadPoolExecutor(max_workers=10))
    yield server
    server.stop(0) 