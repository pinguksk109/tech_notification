import pytest
from unittest.mock import patch, MagicMock
from lambda_function import lambda_handler
from application.usecase.line_usecase import LineUsecase
from application.usecase.train_info_usecase import TrainInfoOutput
from application.usecase.weather_usecase import WeatherOutput
from application.usecase.recommend_article_usecase import RecommendOutput
from application.domain.item import Item


@patch("lambda_function.LineUsecase")
@patch("lambda_function.RecommendArticleUsecase")
@patch("lambda_function.TrainInfoUsecase")
@patch("lambda_function.WeatherUsecase")
def test_should_return_200_when_all_usecases_succeed(
    mock_weather_uc_cls,
    mock_train_uc_cls,
    mock_recommend_uc_cls,
    mock_line_uc_cls,
):
    mock_weather_uc = MagicMock()
    mock_weather_uc.handle.return_value = WeatherOutput(forecast="はれ")
    mock_weather_uc_cls.return_value = mock_weather_uc

    mock_train_uc = MagicMock()
    mock_train_uc.handle.return_value = TrainInfoOutput(abnormal_train=[])
    mock_train_uc_cls.return_value = mock_train_uc

    mock_qiita_uc = MagicMock()
    mock_qiita_uc.handle.return_value = RecommendOutput(
        items=[
            Item(
                title="Qiita Article",
                url="https://qiita.com/article1",
                likes_count=10,
            )
        ]
    )
    mock_zenn_uc = MagicMock()
    mock_zenn_uc.handle.return_value = RecommendOutput(
        items=[
            Item(
                title="Zenn Article",
                url="https://zenn.dev/article1",
                likes_count=5,
            )
        ]
    )
    mock_recommend_uc_cls.side_effect = [mock_qiita_uc, mock_zenn_uc]

    mock_line_uc = MagicMock()
    mock_line_uc_cls.return_value = mock_line_uc

    actual = lambda_handler({}, {})

    assert actual == {"status_code": 200, "body": "Success"}


@pytest.mark.parametrize(
    "exception_cls, usecase_patch, side_effect_index",
    [
        (
            Exception("Qiita error"),
            "lambda_function.RecommendArticleUsecase",
            0,
        ),
        (
            Exception("Zenn error"),
            "lambda_function.RecommendArticleUsecase",
            1,
        ),
        (Exception("Line error"), "lambda_function.LineUsecase", None),
    ],
)
def test_should_return_500_when_exception_occurs(
    exception_cls, usecase_patch, side_effect_index
):
    with patch("lambda_function.WeatherUsecase") as mock_weather_uc_cls, patch(
        "lambda_function.TrainInfoUsecase"
    ) as mock_train_uc_cls, patch(usecase_patch) as mock_uc_cls:
        mock_weather_uc = MagicMock()
        mock_weather_uc.handle.return_value = WeatherOutput(forecast="はれ")
        mock_weather_uc_cls.return_value = mock_weather_uc
        mock_train_uc = MagicMock()
        mock_train_uc.handle.return_value = TrainInfoOutput(abnormal_train=[])
        mock_train_uc_cls.return_value = mock_train_uc

        if usecase_patch.endswith("RecommendArticleUsecase"):
            mock_qiita_uc = MagicMock()
            mock_qiita_uc.handle.side_effect = (
                exception_cls if side_effect_index == 0 else None
            )
            mock_zenn_uc = MagicMock()
            mock_zenn_uc.handle.side_effect = (
                exception_cls if side_effect_index == 1 else None
            )
            mock_uc_cls.side_effect = [mock_qiita_uc, mock_zenn_uc]
            with patch("lambda_function.LineUsecase") as mock_line_uc_cls:
                mock_line_uc = MagicMock()
                mock_line_uc.handle.return_value = None
                mock_line_uc_cls.return_value = mock_line_uc
                # 2. execute
                result = lambda_handler({}, {})
        else:
            mock_qiita_uc = MagicMock()
            mock_qiita_uc.handle.return_value = RecommendOutput(
                items=[
                    Item(
                        title="Qiita Article",
                        url="https://qiita.com/article1",
                        likes_count=10,
                    )
                ]
            )
            mock_zenn_uc = MagicMock()
            mock_zenn_uc.handle.return_value = RecommendOutput(
                items=[
                    Item(
                        title="Zenn Article",
                        url="https://zenn.dev/article1",
                        likes_count=5,
                    )
                ]
            )
            with patch(
                "lambda_function.RecommendArticleUsecase"
            ) as mock_recommend_uc_cls:
                mock_recommend_uc_cls.side_effect = [
                    mock_qiita_uc,
                    mock_zenn_uc,
                ]
                with patch("lambda_function.LineUsecase") as mock_line_uc_cls:
                    mock_line_uc = MagicMock()
                    mock_line_uc.handle.side_effect = exception_cls
                    mock_line_uc_cls.return_value = mock_line_uc
                    # 2. execute
                    result = lambda_handler({}, {})

    # 3. verify
    assert result["status_code"] == 500
