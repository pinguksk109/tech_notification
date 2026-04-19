from application.domain.item import Item
from application.domain.weather import CityWeather
from application.usecase.daily_notification_input import DailyNotificationInput
from application.usecase.daily_notification_message_builder import (
    DailyNotificationMessageBuilder,
)


def test_should_build_weather_and_article_messages():
    # 1. setup
    builder = DailyNotificationMessageBuilder(today_date="2024-01-01")
    input_data = DailyNotificationInput(
        qiita_items=[
            Item(
                title="Qiita記事1",
                url="https://qiita.com/article1",
                likes_count=2,
            ),
            Item(
                title="Qiita記事2",
                url="https://qiita.com/article2",
                likes_count=4,
            ),
        ],
        zenn_items=[
            Item(
                title="Zenn記事1",
                url="https://zenn.dev/article1",
                likes_count=6,
            )
        ],
        weather_forecasts=[
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
        ],
    )

    # 2. execute
    actual = builder.build(input_data)

    # 3. verify
    assert actual == [
        (
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
            "大阪市詳細⇒https://www.jma.go.jp/bosai/forecast/"
        ),
        (
            "2024-01-01 のQiita今日の記事を送ります✍\n"
            "1. Qiita記事1 https://qiita.com/article1\n"
            "2. Qiita記事2 https://qiita.com/article2"
        ),
        (
            "2024-01-01 のZenn今日の記事を送ります✍\n"
            "1. Zenn記事1 https://zenn.dev/article1"
        ),
    ]
