import importlib.util
import os


def test_proto_generation():
    """测试生成的Proto代码是否可以正确导入"""
    # 假设生成的代码在 services 目录下
    proto_file = "services/common_pb2.py"  # 根据实际生成的文件名调整
    assert os.path.exists(proto_file), "生成的Proto文件不存在"

    # 动态导入生成的模块
    spec = importlib.util.spec_from_file_location("common_pb2", proto_file)
    common_pb2 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(common_pb2)

    # 测试 BaseResponse 消息是否存在
    assert hasattr(common_pb2, "BaseResponse"), "BaseResponse 消息未生成"

    # 创建 BaseResponse 实例并测试
    response = common_pb2.BaseResponse(code=200, message="成功")
    assert response.code == 200
    assert response.message == "成功"
