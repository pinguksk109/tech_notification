from typing import List
from pydantic import BaseModel


class Item(BaseModel):
    title: str
    url: str
    likes_count: int

    @classmethod
    def get_5ranking_items(cls, items: List['Item']) -> List['Item']:
        sorted_items = sorted(items, key=lambda x: x.likes_count, reverse=True)
        return sorted_items[:5]
