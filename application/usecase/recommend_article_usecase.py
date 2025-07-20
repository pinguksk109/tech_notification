from typing import List
from application.port.article_port import IArticleRepository
from application.base import IOutput, IUsecase
from application.domain.item import Item
from pydantic import BaseModel


class RecommendOutput(IOutput, BaseModel):
    items: List[Item]


class RecommendArticleUsecase(IUsecase[RecommendOutput]):
    def __init__(self, repository: IArticleRepository):
        self.repository = repository

    def handle(self) -> RecommendOutput:
        all_items: List[Item] = []
        for page in range(1, self.repository.TARGET_PAGE_COUNT + 1):
            all_items.extend(self.repository.fetch_items(page))

        top5 = Item.get_5ranking_items(all_items)
        return RecommendOutput(items=top5)
