from pydantic import BaseModel, Field
from typing import List
from infrastructure.repository.line_notification_repository import (
    LineNotificationRepository,
)
from application.base import IInput, IUsecase
from application.domain.item import Item
from application.domain.weather import CityWeather
from datetime import datetime
import logging
from zoneinfo import ZoneInfo

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class LineSendInput(IInput, BaseModel):
    qiita_items: List[Item]
    zenn_items: List[Item]
    abnormal_train: List[str] = Field(default_factory=list)
    weather_forecasts: List[CityWeather]


class LineUsecase(IUsecase[None]):
    JST = ZoneInfo("Asia/Tokyo")

    def __init__(self, line_repository: LineNotificationRepository):
        self.line_repository = line_repository
        self.today_date = datetime.now(self.JST).strftime("%Y-%m-%d")

    def handle(self, input: LineSendInput) -> None:
        messages = [
            self._weather_message(input.weather_forecasts),
            # 大阪メトロ情報は通知停止。
            # self._train_message(input.abnormal_train),
            self._media_message(input.qiita_items, "Qiita"),
            self._media_message(input.zenn_items, "Zenn"),
        ]
        for m in messages:
            try:
                self.line_repository.send(m)
            except Exception as e:
                logger.error(f"メッセージ送信失敗: {e}")

    def _media_message(self, items: List[Item], media: str) -> str:
        lines = [f"{i+1}. {it.title} {it.url}" for i, it in enumerate(items)]
        header = f"{self.today_date} の{media}今日の記事を送ります✍\n"
        return header + "\n".join(lines)

    def _train_message(self, abnormal: List[str]) -> str:
        if not abnormal:
            return f"{self.today_date}: 大阪メトロの遅延なし🚆"
        joined = ", ".join(abnormal)
        return (
            f"{self.today_date}: 以下で遅延発生中🚨\n"
            f"{joined}\n"
            "詳細⇒https://subway.osakametro.co.jp/guide/subway_information.php"
        )

    def _weather_message(self, forecasts: List[CityWeather]) -> str:
        lines = [f"{self.today_date} の天気", ""]
        for forecast in forecasts:
            lines.extend(
                [
                    f"■ {forecast.city_name}",
                    forecast.forecast,
                    f"🌡 最低気温: {forecast.min_temp}℃ / 最高気温: {forecast.max_temp}℃",
                    "",
                ]
            )
        lines.append("詳細⇒https://www.jma.go.jp/bosai/forecast/")
        return "\n".join(lines)

    def _weather_message(self, forecasts: List[CityWeather]) -> str:
        header = [f"{self.today_date} の天気", ""]

        body = [
            line
            for fc in forecasts
            for line in [
                f"■ {fc.city_name}",
                fc.forecast,
                f"🌡 最低気温: {fc.min_temp}℃ / 最高気温: {fc.max_temp}℃",
                "",
            ]
        ]

        footer = ["大阪市詳細⇒https://www.jma.go.jp/bosai/forecast/"]

        return "\n".join(header + body + footer)