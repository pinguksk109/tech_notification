import pytest
from unittest.mock import MagicMock
from application.usecase.line_usecase import (
    LineSendInput,
    LineUsecase,
)
from application.domain.item import Item
from application.domain.weather import CityWeather


@pytest.fixture
def line_usecase():
    mock_line_repository = MagicMock()
    line_usecase_instance = LineUsecase(line_repository=mock_line_repository)
    line_usecase_instance.today_date = "2024-01-01"
    return line_usecase_instance, mock_line_repository


def test_should_return_three_messages_when_handle_is_called(line_usecase):
    # 1. setup
    line_usecase_instance, mock_line_repository = line_usecase

    qiita_items = [
        Item(
            title="Qiita記事1", url="https://qiita.com/article1", likes_count=2
        ),
        Item(
            title="Qiita記事2", url="https://qiita.com/article2", likes_count=4
        ),
    ]
    zenn_items = [
        Item(
            title="Zenn記事1", url="https://zenn.dev/article1", likes_count=6
        ),
    ]
    abnormal_train = []
    weather_forecasts = [
        CityWeather(
            city_name="大阪市",
            forecast="はれ",
            min_temp=10,
            max_temp=25,
        ),
        CityWeather(
            city_name="ハノイ市",
            forecast="気温予報",
            min_temp=25,
            max_temp=36,
        ),
    ]

    input_data = LineSendInput(
        qiita_items=qiita_items,
        zenn_items=zenn_items,
        abnormal_train=abnormal_train,
        weather_forecasts=weather_forecasts,
    )

    # 2. execute
    line_usecase_instance.handle(input_data)

    # 3. verify
    expected_weather_message = (
        "2024-01-01 の天気\n"
        "\n"
        "■ 大阪市\n"
        "はれ\n"
        "🌡 最低気温: 10℃ / 最高気温: 25℃\n"
        "\n"
        "■ ハノイ市\n"
        "気温予報\n"
        "🌡 最低気温: 25℃ / 最高気温: 36℃\n"
        "\n"
        "詳細⇒https://www.jma.go.jp/bosai/forecast/"
    )
    expected_qiita_message = (
        "2024-01-01 のQiita今日の記事を送ります✍\n"
        "1. Qiita記事1 https://qiita.com/article1\n"
        "2. Qiita記事2 https://qiita.com/article2"
    )
    expected_zenn_message = (
        "2024-01-01 のZenn今日の記事を送ります✍\n"
        "1. Zenn記事1 https://zenn.dev/article1"
    )

    mock_line_repository.send.assert_any_call(expected_weather_message)
    mock_line_repository.send.assert_any_call(expected_qiita_message)
    mock_line_repository.send.assert_any_call(expected_zenn_message)
    assert mock_line_repository.send.call_count == 3
