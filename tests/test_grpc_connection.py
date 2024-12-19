import grpc
import pytest
from concurrent import futures
from services.user_service import user_pb2_grpc, user_pb2
from services.common import common_pb2

# 创建一个 mock gRPC 服务器
class MockUserService(user_pb2_grpc.UserServiceServicer):
    def CreateUser(self, request, context):
        return common_pb2.BaseResponse(code=0, message="User created successfully")

    def GetUser(self, request, context):
        return user_pb2.User(user_id=request.user_id, username="test_user", email="test@example.com", created_at=1234567890)

@pytest.fixture
def grpc_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    user_pb2_grpc.add_UserServiceServicer_to_server(MockUserService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    yield server
    server.stop(0)

@pytest.fixture
def grpc_channel(grpc_server):
    channel = grpc.insecure_channel('localhost:50051')
    yield channel
    channel.close()

def test_create_user(grpc_channel):
    """测试创建用户的 gRPC 调用"""
    stub = user_pb2_grpc.UserServiceStub(grpc_channel)
    
    request = user_pb2.CreateUserRequest(
        username="test_user",
        email="test@example.com",
        password="secure_password"
    )
    
    response = stub.CreateUser(request)
    
    assert response is not None  # 确保响应不为空
    assert response.code == 0  # 假设成功时返回的 code 为 0
    assert response.message == "User created successfully"  # 假设成功时返回的消息 

def test_get_user(grpc_channel):
    """测试获取用户的 gRPC 调用"""
    stub = user_pb2_grpc.UserServiceStub(grpc_channel)
    
    request = user_pb2.GetUserRequest(user_id="12345")
    
    response = stub.GetUser(request)
    
    assert response is not None  # 确保响应不为空
    assert response.user_id == "12345"  # 确保返回的用户 ID 正确
    assert response.username == "test_user"  # 确保返回的用户名正确
    assert response.email == "test@example.com"  # 确保返回的邮箱正确