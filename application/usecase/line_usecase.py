from pydantic import BaseModel
from typing import List
from infrastructure.repository.line_repository import LineRepository
from application.base import IInput
from domain.item import Item

class LineSendInput(IInput, BaseModel):
    items: List[Item]

class LineUsecase:
    def __init__(self, line_repository: LineRepository):
        self.line_repository = line_repository
        pass

    def handle(self, input_data: LineSendInput):
        message = _create_message(input_data.items)
        self.line_repository.send_message(message)

def _create_message(items: List[Item]) -> str:
    formatted_items = []
    for i, item in enumerate(items):
        formatted_items.append(f"{i+1}. {item.title} {item.url}")
    return "今日のQiitaおすすめ記事を送ります。\n\n" + "\n".join(formatted_items)