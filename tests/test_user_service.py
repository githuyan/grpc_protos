import pytest
from services.service.user_pb2 import CreateUserRequest, GetUserRequest
from services.common.base_pb2 import BaseResponse

def test_create_user_request():
    request = CreateUserRequest(
        username="test_user",
        email="test@example.com",
        password="password123"
    )
    assert request.username == "test_user"
    assert request.email == "test@example.com"
    assert request.password == "password123"

def test_get_user_request():
    request = GetUserRequest(user_id="123")
    assert request.user_id == "123" 