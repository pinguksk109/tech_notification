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

class LineUsecase:
    JST = pytz.timezone('Asia/Tokyo')

    def __init__(self, line_repository: LineRepository):
        self.line_repository = line_repository
        self.today_date = datetime.now(self.JST).strftime("%Y-%m-%d")

    def handle(self, input_data: LineSendInput) -> None:
        message = _create_message(self, input_data.qiita_items, "Qiita")
        self.line_repository.send_message(message)
        message = _create_message(self, input_data.zenn_items, "Zenn")
        self.line_repository.send_message(message)

def _create_message(self, items: List[Item], media: str) -> str:
    formatted_items = []
    for i, item in enumerate(items):
        formatted_items.append(f"{i+1}. {item.title} {item.url}")
    return f"{self.today_date}の{media}おすすめ記事を送ります✍\n\n" + "\n".join(formatted_items)