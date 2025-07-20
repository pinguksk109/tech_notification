import pytest
from unittest.mock import MagicMock
from application.usecase.recommend_article_usecase import (
    RecommendArticleUsecase,
    RecommendOutput,
)
from application.domain.item import Item


@pytest.fixture
def mock_repository():
    # Arrange: モックリポジトリを準備
    repo = MagicMock()
    # ページ数を2に設定
    repo.TARGET_PAGE_COUNT = 2
    # fetch_items はそれぞれ異なるページで呼ばれ、
    # page1→3件、page2→4件の Item リストを返す
    sample = Item(title="Test", url="https://example.com", likes_count=5)
    repo.fetch_items.side_effect = [
        [sample, sample, sample],
        [sample, sample, sample, sample],
    ]
    return repo


def test_handle_returns_top5_and_prints_items(mock_repository):
    # Arrange
    usecase = RecommendArticleUsecase(mock_repository)

    # Act
    output: RecommendOutput = usecase.handle()

    # Assert
    assert isinstance(output, RecommendOutput)
    assert len(output.items) == 5
    print(output.items[0])
    assert all(isinstance(item, Item) for item in output.items)
