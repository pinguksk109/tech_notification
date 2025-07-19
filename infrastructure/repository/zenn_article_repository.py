import logging
from typing import List
import requests
from http import HTTPStatus
from application.port.article_port import IArticleRepository
from domain.item import Item

logger = logging.getLogger(__name__)


class ZennArticleRepository(IArticleRepository):
    def fetch_items(self, page: int) -> List[Item]:
        url = f"https://zenn.dev/api/articles?order=latest&page={page}"
        resp = requests.get(url)
        if resp.status_code != HTTPStatus.OK:
            raise Exception(f"Zenn API error {resp.status_code}")
        raw = resp.json().get("articles", [])
        items = [
            Item(
                title=art["title"],
                url="https://zenn.dev" + art["path"],
                likes_count=art["liked_count"],
            )
            for art in raw
            if art.get("liked_count", 0) >= 3
        ]
        logger.info(f"Zenn page {page} fetched, {len(items)} items filtered")
        return items
