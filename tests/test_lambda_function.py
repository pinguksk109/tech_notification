import pytest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
from lambda_function import lambda_handler
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
    mock_weather_uc.handle = AsyncMock(
        return_value=WeatherOutput(forecast="はれ", min_temp=15, max_temp=30)
    )
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
    # 1. setup
    with patch("lambda_function.WeatherUsecase") as mock_weather_uc_cls, patch(
        "lambda_function.TrainInfoUsecase"
    ) as mock_train_uc_cls, patch(usecase_patch) as mock_uc_cls:

        mock_weather_uc = MagicMock()
        mock_weather_uc.handle = AsyncMock(
            return_value=WeatherOutput(
                forecast="はれ", min_temp=15, max_temp=30
            )
        )
        mock_weather_uc_cls.return_value = mock_weather_uc

        mock_train_uc = MagicMock()
        mock_train_uc.handle.return_value = TrainInfoOutput(abnormal_train=[])
        mock_train_uc_cls.return_value = mock_train_uc

        # 2. patch failures
        if usecase_patch.endswith("RecommendArticleUsecase"):
            mock_qiita_uc = MagicMock()
            if side_effect_index == 0:
                mock_qiita_uc.handle.side_effect = exception_cls
            else:
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
            if side_effect_index == 1:
                mock_zenn_uc.handle.side_effect = exception_cls
            else:
                mock_zenn_uc.handle.return_value = RecommendOutput(
                    items=[
                        Item(
                            title="Zenn Article",
                            url="https://zenn.dev/article1",
                            likes_count=5,
                        )
                    ]
                )

            mock_uc_cls.side_effect = [mock_qiita_uc, mock_zenn_uc]

            with patch("lambda_function.LineUsecase") as mock_line_uc_cls:
                mock_line_uc = MagicMock()
                mock_line_uc.handle.return_value = None
                mock_line_uc_cls.return_value = mock_line_uc

                # 3. execute
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
            ) as mock_rec_cls, patch(
                "lambda_function.LineUsecase"
            ) as mock_line_uc_cls:

                mock_rec_cls.side_effect = [mock_qiita_uc, mock_zenn_uc]

                mock_line_uc = MagicMock()
                mock_line_uc.handle.side_effect = exception_cls
                mock_line_uc_cls.return_value = mock_line_uc

                # 3. execute
                result = lambda_handler({}, {})

    # 4. verify
    assert result["status_code"] == 500
