import os
import pytest
from unittest.mock import patch, Mock
from infrastructure.repository.line_notification_repository import (
    LineNotificationRepository,
)
from http import HTTPStatus


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("LINE_USER_ID", "dummy_id")
    monkeypatch.setenv("LINE_BEARER_TOKEN", "Bearer dummy_token")


@patch("infrastructure.repository.line_notification_repository.requests.post")
def test_should_return_without_exception_when_line_api_returns_ok(mock_post):
    # 1. setup
    mock_response = Mock()
    mock_response.status_code = HTTPStatus.OK
    mock_post.return_value = mock_response
    repo = LineNotificationRepository()

    # 2. execute
    repo.send("hello")

    # 3. verify
    mock_post.assert_called_once()


@patch("infrastructure.repository.line_notification_repository.requests.post")
def test_should_raise_exception_when_line_api_returns_non_ok_status(
    mock_post,
):
    # 1. setup
    mock_response = Mock()
    mock_response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    mock_response.text = "internal server error"
    mock_post.return_value = mock_response
    repo = LineNotificationRepository()

    # 2. execute
    with pytest.raises(Exception) as excinfo:
        repo.send("Hello")

    # 3. verify
    assert "Line APIから200以外" in str(excinfo.value)


@patch("infrastructure.repository.line_notification_repository.requests.post")
def test_should_raise_exception_when_line_request_fails(mock_post):
    # 1. setup
    mock_post.side_effect = Exception("network error")
    repo = LineNotificationRepository()

    # 2. execute
    with pytest.raises(Exception) as excinfo:
        repo.send("Hello")

    # 3. verify
    assert "メッセージ送信リクエストに失敗しました" in str(excinfo.value)
