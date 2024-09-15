import logging
from typing import List
from infrastructure.repository.qiita_api_repository import QiitaApiRepository
from domain.item import Item

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TechRecommendUsecase:
    def __init__(self, qiita_api_repository: QiitaApiRepository):
        self.qiita_api_repository = qiita_api_repository
        pass

    def handle(self):
        page_numbers = range(1, 11)

        responses = []
        for page in page_numbers:
            print(page)
            response = self._get_items(page)
            responses.append(response)

        items: List[Item] = []

        # HACK: Pythonでfor分のネストはパフォーマンス観点でやめた方がいいかも
        for response_list in responses:
            for item in response_list:
                if item['likes_count'] >= 3:
                    items.append(Item(**item))

        return Item.get_5ranking_items(items)
    
    def _get_items(self, page_number):
        response = self.qiita_api_repository.get_items(page_number)
        logger.info(f'{page_number}ページ目取得完了')
        return response