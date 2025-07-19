import logging
from typing import List
import requests
from http import HTTPStatus
from application.port.article_port import IArticleRepository
from domain.item import Item


logger = logging.getLogger(__name__)


class QiitaArticleRepository(IArticleRepository):
    def fetch_items(self, page: int) -> List[Item]:
        url = f"https://qiita.com/api/v2/items?page={page}&per_page=100"
        resp = requests.get(url)
        if resp.status_code == HTTPStatus.FORBIDDEN:
            raise Exception("Qiita API: rate limited")
        if resp.status_code != HTTPStatus.OK:
            raise Exception(f"Qiita API error {resp.status_code}")
        raw = resp.json()
        items = [Item(**i) for i in raw if i.get("likes_count", 0) >= 3]
        logger.info(f"Qiita page {page} fetched, {len(items)} items filtered")
        return items
