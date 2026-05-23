from unittest.mock import MagicMock

from application.usecase.line_usecase import LineUsecase


def test_should_send_all_messages_when_handle_is_called():
    # 1. setup
    mock_line_repository = MagicMock()
    usecase = LineUsecase(line_repository=mock_line_repository)
    messages = ["message-1", "message-2", "message-3"]

    # 2. execute
    usecase.handle(messages)

    # 3. verify
    mock_line_repository.send.assert_any_call("message-1")
    mock_line_repository.send.assert_any_call("message-2")
    mock_line_repository.send.assert_any_call("message-3")
    assert mock_line_repository.send.call_count == 3


def test_should_continue_sending_when_a_message_send_fails():
    # 1. setup
    mock_line_repository = MagicMock()
    mock_line_repository.send.side_effect = [
        Exception("send failed"),
        None,
        None,
    ]
    usecase = LineUsecase(line_repository=mock_line_repository)

    # 2. execute
    usecase.handle(["message-1", "message-2", "message-3"])

    # 3. verify
    assert mock_line_repository.send.call_count == 3
