from pydantic import BaseModel
from typing import List
from infrastructure.repository.line_repository import LineRepository
from application.base import IInput
from domain.item import Item
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


class LineUsecase:
    JST = pytz.timezone('Asia/Tokyo')

    def __init__(self, line_repository: LineRepository):
        self.line_repository = line_repository
        self.today_date = datetime.now(self.JST).strftime("%Y-%m-%d")

    def handle(self, input_data: LineSendInput) -> None:
        weather_message = _create_weather_forecast_message(self, input_data.weather_forecast)
        self.line_repository.send_message(weather_message)
        train_info_message = _create_train_info_message(self, input_data.abnormal_train)
        self.line_repository.send_message(train_info_message)
        qiita_message = _create_message(self, input_data.qiita_items, "Qiita")
        self.line_repository.send_message(qiita_message)
        zenn_message = _create_message(self, input_data.zenn_items, "Zenn")
        self.line_repository.send_message(zenn_message)


def _create_message(self, items: List[Item], media: str) -> str:
    formatted_items = []
    for i, item in enumerate(items):
        formatted_items.append(f"{i + 1}. {item.title} {item.url}")
    return f"{self.today_date}の{media}おすすめ記事を送ります✍\n\n" + \
        "\n".join(formatted_items)

def _create_train_info_message(self, abnormal_train: List[str]) -> str:
    if(len(abnormal_train) == 0):
        return f"{self.today_date}: 大阪メトロの電車遅延はありませんでした"
    else:
        delayed_trains = ", ".join(abnormal_train)
        return f"{self.today_date}: 以下の電車で遅延が発生しています: {delayed_trains}。詳細はこちら: https://subway.osakametro.co.jp/guide/subway_information.php"
    
def _create_weather_forecast_message(self, weather_forecast: str) -> str:
    return f"{self.today_date}の天気予報です: {weather_forecast}\n 詳しくはこちら: https://www.jma.go.jp/bosai/forecast/#area_type=offices&area_code=270000"