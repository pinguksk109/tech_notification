import pytest
from unittest.mock import patch, MagicMock
from lambda_function import lambda_handler
from application.domain.item import Item


@patch("lambda_function._gather_all_info")
@patch("infrastructure.repository.line_notification_repository.LineNotificationRepository")
@patch("lambda_function.LineUsecase")
def test_should_return_200_when_all_usecases_succeed(
    mock_line_uc_cls,
    mock_line_repository_cls,
    mock_gather_all_info,
):
    mock_gather_all_info.return_value = {
        "weather_forecast": "はれ",
        "min_temp": 15,
        "max_temp": 30,
        "qiita_items": [
            Item(
                title="Qiita Article",
                url="https://qiita.com/article1",
                likes_count=10,
            )
        ],
        "zenn_items": [
            Item(
                title="Zenn Article",
                url="https://zenn.dev/article1",
                likes_count=5,
            )
        ],
    }

    mock_line_repository_cls.return_value = MagicMock()
    mock_line_uc = MagicMock()
    mock_line_uc_cls.return_value = mock_line_uc

    actual = lambda_handler({}, {})

    assert actual == {"status_code": 200, "body": "Success"}


@pytest.mark.parametrize(
    "exception_cls, patch_target",
    [
        (Exception("Gather error"), "lambda_function._gather_all_info"),
        (Exception("Line error"), "lambda_function.LineUsecase"),
    ],
)
def test_should_return_500_when_exception_occurs(exception_cls, patch_target):
    # 1. setup
    with patch("lambda_function._gather_all_info") as mock_gather_all_info, patch(
        "infrastructure.repository.line_notification_repository.LineNotificationRepository"
    ) as mock_line_repository_cls, patch(
        patch_target
    ) as mock_target:
        mock_gather_all_info.return_value = {
            "weather_forecast": "はれ",
            "min_temp": 15,
            "max_temp": 30,
            "qiita_items": [
                Item(
                    title="Qiita Article",
                    url="https://qiita.com/article1",
                    likes_count=10,
                )
            ],
            "zenn_items": [
                Item(
                    title="Zenn Article",
                    url="https://zenn.dev/article1",
                    likes_count=5,
                )
            ],
        }
        mock_line_repository_cls.return_value = MagicMock()

        if patch_target.endswith("_gather_all_info"):
            mock_target.side_effect = exception_cls
        else:
            mock_line_uc = MagicMock()
            mock_line_uc.handle.side_effect = exception_cls
            mock_target.return_value = mock_line_uc

        # 2. execute
        result = lambda_handler({}, {})

    # 3. verify
    assert result["status_code"] == 500
