import asyncio
from unittest.mock import AsyncMock, MagicMock

from application.domain.item import Item
from application.domain.weather import CityWeather
from application.usecase.daily_notification_input import DailyNotificationInput
from application.usecase.daily_notification_orchestrator import (
    DailyNotificationOrchestrator,
)
from application.usecase.recommend_article_usecase import RecommendOutput
from application.usecase.train_info_usecase import TrainInfoOutput
from application.usecase.weather_usecase import WeatherOutput


def test_should_collect_data_build_messages_and_send_notifications():
    # 1. setup
    weather_usecase = MagicMock()
    weather_usecase.handle = AsyncMock(
        return_value=WeatherOutput(
            forecasts=[
                CityWeather(
                    city_name="大阪市",
                    forecast="はれ",
                    min_temp=10,
                    max_temp=25,
                )
            ]
        )
    )
    qiita_usecase = MagicMock()
    qiita_usecase.handle.return_value = RecommendOutput(
        items=[
            Item(
                title="Qiita記事1",
                url="https://qiita.com/article1",
                likes_count=2,
            )
        ]
    )
    zenn_usecase = MagicMock()
    zenn_usecase.handle.return_value = RecommendOutput(
        items=[
            Item(
                title="Zenn記事1",
                url="https://zenn.dev/article1",
                likes_count=6,
            )
        ]
    )
    line_usecase = MagicMock()
    message_builder = MagicMock()
    message_builder.build.return_value = ["message-1", "message-2"]

    orchestrator = DailyNotificationOrchestrator(
        weather_usecase=weather_usecase,
        qiita_usecase=qiita_usecase,
        zenn_usecase=zenn_usecase,
        line_usecase=line_usecase,
        message_builder=message_builder,
    )

    # 2. execute
    asyncio.run(orchestrator.handle())

    # 3. verify
    weather_usecase.handle.assert_awaited_once_with()
    qiita_usecase.handle.assert_called_once_with()
    zenn_usecase.handle.assert_called_once_with()
    message_builder.build.assert_called_once_with(
        DailyNotificationInput(
            weather_forecasts=[
                CityWeather(
                    city_name="大阪市",
                    forecast="はれ",
                    min_temp=10,
                    max_temp=25,
                )
            ],
            qiita_items=[
                Item(
                    title="Qiita記事1",
                    url="https://qiita.com/article1",
                    likes_count=2,
                )
            ],
            zenn_items=[
                Item(
                    title="Zenn記事1",
                    url="https://zenn.dev/article1",
                    likes_count=6,
                )
            ],
            abnormal_train=[],
        )
    )
    line_usecase.handle.assert_called_once_with(["message-1", "message-2"])


def test_should_include_train_info_when_train_usecase_is_provided():
    # 1. setup
    weather_usecase = MagicMock()
    weather_usecase.handle = AsyncMock(
        return_value=WeatherOutput(
            forecasts=[
                CityWeather(
                    city_name="大阪市",
                    forecast="はれ",
                    min_temp=10,
                    max_temp=25,
                )
            ]
        )
    )
    qiita_usecase = MagicMock()
    qiita_usecase.handle.return_value = RecommendOutput(items=[])
    zenn_usecase = MagicMock()
    zenn_usecase.handle.return_value = RecommendOutput(items=[])
    line_usecase = MagicMock()
    message_builder = MagicMock()
    train_usecase = MagicMock()
    train_usecase.handle.return_value = TrainInfoOutput(
        abnormal_train=["御堂筋線"]
    )

    orchestrator = DailyNotificationOrchestrator(
        weather_usecase=weather_usecase,
        qiita_usecase=qiita_usecase,
        zenn_usecase=zenn_usecase,
        line_usecase=line_usecase,
        message_builder=message_builder,
        train_usecase=train_usecase,
    )

    # 2. execute
    asyncio.run(orchestrator.handle())

    # 3. verify
    message_builder.build.assert_called_once_with(
        DailyNotificationInput(
            weather_forecasts=[
                CityWeather(
                    city_name="大阪市",
                    forecast="はれ",
                    min_temp=10,
                    max_temp=25,
                )
            ],
            qiita_items=[],
            zenn_items=[],
            abnormal_train=["御堂筋線"],
        )
    )
    train_usecase.handle.assert_called_once_with()
