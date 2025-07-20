from abc import ABC, abstractmethod
from typing import List
from application.domain.item import Item


class IArticleRepository(ABC):
    TARGET_PAGE_COUNT: int = 10

    @abstractmethod
    def fetch_items(self, page: int) -> List[Item]:
        pass
