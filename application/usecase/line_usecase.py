from pydantic import BaseModel
from typing import List
from infrastructure.repository.line_notification_repository import (
    LineNotificationRepository,
)
from application.base import IInput, IUsecase
from application.domain.item import Item
from datetime import datetime
import pytz
import logging

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class LineSendInput(IInput, BaseModel):
    qiita_items: List[Item]
    zenn_items: List[Item]
    abnormal_train: List[str]
    weather_forecast: str


class LineUsecase(IUsecase[None]):
    JST = pytz.timezone("Asia/Tokyo")

    def __init__(self, line_repository: LineNotificationRepository):
        self.line_repository = line_repository
        self.today_date = datetime.now(self.JST).strftime("%Y-%m-%d")

    def handle(self, input_data: LineSendInput) -> None:
        messages = [
            self._weather_message(input_data.weather_forecast),
            self._train_message(input_data.abnormal_train),
            self._media_message(input_data.qiita_items, "Qiita"),
            self._media_message(input_data.zenn_items, "Zenn"),
        ]
        for m in messages:
            try:
                self.line_repository.send(m)
            except Exception as e:
                logger.error(f"メッセージ送信失敗: {e}")

    def _media_message(self, items: List[Item], media: str) -> str:
        lines = [f"{i+1}. {it.title} {it.url}" for i, it in enumerate(items)]
        header = f"{self.today_date} の{media}おすすめ記事を送ります✍\n"
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

    def _weather_message(self, forecast: str) -> str:
        return (
            f"{self.today_date} の天気\n"
            f"{forecast}\n"
            "詳細⇒https://www.jma.go.jp/bosai/forecast/"
        )
