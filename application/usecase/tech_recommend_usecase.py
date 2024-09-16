import logging
from pydantic import BaseModel
from typing import List
from infrastructure.repository.qiita_api_repository import QiitaApiRepository
from domain.item import Item
from application.base import IOutput

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class QiitaRecommendOutput(IOutput, BaseModel):
    items: List[Item]

class TechRecommendUsecase:
    QIITA_TARGET_PAGE_COUNT = 10

    def __init__(self, qiita_api_repository: QiitaApiRepository):
        self.qiita_api_repository = qiita_api_repository

    def qiita_handle(self) -> QiitaRecommendOutput:

        page_numbers = range(1, self.QIITA_TARGET_PAGE_COUNT+1)
        responses = [self._get_qiita_items(page) for page in page_numbers]

        items: List[Item] = []
        for response_list in responses:
            for item in response_list:
                if item['likes_count'] >= 3:
                    items.append(Item(**item))

        ranking_5items = Item.get_5ranking_items(items)

        return QiitaRecommendOutput(items=ranking_5items)
    
    def _get_qiita_items(self, page_number):
        response = self.qiita_api_repository.get_items(page_number)
        logger.info(f'{page_number}ページ目取得完了')
        return response