import pytest
from unittest.mock import MagicMock
from application.usecase.recommend_article_usecase import (
    RecommendArticleUsecase,
    RecommendOutput,
)
from application.domain.item import Item


@pytest.fixture
def mock_repository():
    repo = MagicMock()
    repo.TARGET_PAGE_COUNT = 2
    sample = Item(title="Test", url="https://example.com", likes_count=5)
    repo.fetch_items.side_effect = [
        [sample, sample, sample],
        [sample, sample, sample, sample],
    ]
    return repo


def test_should_return_top_five_items_when_handle_is_called(mock_repository):
    # 1. setup
    usecase = RecommendArticleUsecase(mock_repository)

    # 2. execute
    output: RecommendOutput = usecase.handle()

    # 3. verify
    assert isinstance(output, RecommendOutput)
    assert len(output.items) == 5
    print(output.items[0])
    assert all(isinstance(item, Item) for item in output.items)
