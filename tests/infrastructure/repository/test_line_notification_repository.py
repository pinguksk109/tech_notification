import os
import pytest
from unittest.mock import patch, Mock
from infrastructure.repository.line_notification_repository import (
    LineNotificationRepository,
)
from http import HTTPStatus


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    # Arrange
    monkeypatch.setenv("LINE_USER_ID", "dummy_id")
    monkeypatch.setenv("LINE_BEARER_TOKEN", "Bearer dummy_token")


@patch("infrastructure.repository.line_notification_repository.requests.post")
def test_処理が成功した場合_sendが例外を投げない(mock_post):
    # Arrange
    mock_response = Mock()
    mock_response.status_code = HTTPStatus.OK
    mock_post.return_value = mock_response
    repo = LineNotificationRepository()

    # Act & Assert
    repo.send("hello")


@patch("infrastructure.repository.line_notification_repository.requests.post")
def test_500の場合_Exceptionをスローすること(mock_post):
    # Arrange
    mock_response = Mock()
    mock_response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    mock_response.text = "internal server error"
    mock_post.return_value = mock_response
    repo = LineNotificationRepository()

    # Act & Assert
    with pytest.raises(Exception) as excinfo:
        repo.send("Hello")
    assert "Line APIから200以外" in str(excinfo.value)


@patch("infrastructure.repository.line_notification_repository.requests.post")
def test_リクエストに失敗した場合_Exceptionをスローすること(mock_post):
    # Arrange
    mock_post.side_effect = Exception("network error")
    repo = LineNotificationRepository()

    # Act & Assert
    with pytest.raises(Exception) as excinfo:
        repo.send("Hello")
    assert "メッセージ送信リクエストに失敗しました" in str(excinfo.value)
