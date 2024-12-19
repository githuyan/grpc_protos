import os
from pathlib import Path

import pytest

from scripts.gen_proto import ProtoGenerator


@pytest.fixture
def proto_generator():
    """创建 ProtoGenerator 实例的测试夹具"""
    return ProtoGenerator()


def test_proto_file_discovery(proto_generator):
    """测试是否正确发现所有的 proto 文件"""
    # 确保找到了 common.proto
    assert any("common.proto" in str(p) for p in proto_generator.common_protos)
    # 确保找到了 user.proto
    assert any("user.proto" in str(p) for p in proto_generator.service_packages)


def test_clean_target_dir(proto_generator, tmp_path):
    """测试目标目录清理功能"""
    # 使用临时目录作为测试目标目录
    proto_generator.target_dir = tmp_path
    
    # 创建一些测试文件
    test_file = tmp_path / "test.py"
    test_file.write_text("test content")
    
    # 执行清理
    proto_generator.clean_target_dir()
    
    # 验证目录被清理并重新创建
    assert tmp_path.exists()
    assert (tmp_path / "__init__.py").exists()
    assert not test_file.exists()


def test_generate_proto_files(proto_generator, tmp_path):
    """测试 Proto 文件生成功能"""
    # 使用临时目录作为测试目标目录
    proto_generator.target_dir = tmp_path
    
    # 生成代码
    proto_generator.generate()
    
    # 验证生成的文件
    generated_files = list(tmp_path.rglob("*.py"))
    
    # 检查是否生成了预期的文件
    assert any("user_pb2.py" in str(f) for f in generated_files)
    assert any("user_pb2_grpc.py" in str(f) for f in generated_files)
    assert any("__init__.py" in str(f) for f in generated_files)


def test_generated_code_imports():
    """测试生成的代码是否可以正确导入"""
    try:
        import sys
        sys.path.append('services')  # 确保路径正确
        from services.user_service.user_pb2 import User, CreateUserRequest
        from services.user_service.user_pb2_grpc import UserServiceStub
        
        # 创建测试对象以验证基本功能
        user = User(
            user_id="1",
            username="test_user",
            email="test@example.com",
            created_at=1234567890
        )
        
        assert user.user_id == "1"
        assert user.username == "test_user"
        assert user.email == "test@example.com"
        assert user.created_at == 1234567890
        
    except ImportError as e:
        pytest.fail(f"无法导入生成的代码: {e}") 