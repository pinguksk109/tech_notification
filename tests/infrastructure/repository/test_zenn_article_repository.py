import pytest
from unittest.mock import patch, Mock
from infrastructure.repository.zenn_article_repository import (
    ZennArticleRepository,
)
from http import HTTPStatus
from domain.item import Item
from typing import Dict, Any, List


@pytest.fixture
def mock_zenn_response() -> Dict[str, List[Dict[str, Any]]]:
    return {
        "articles": [
            {
                "id": 123456,
                "post_type": "Article",
                "title": "Sample Zenn Article",
                "slug": "sample-zenn-article",
                "comments_count": 0,
                "liked_count": 5,
                "body_letters_count": 350,
                "article_type": "tech",
                "emoji": "🤔",
                "is_suspending_private": False,
                "published_at": "2024-09-19T01:11:11.945+09:00",
                "body_updated_at": "2024-09-19T01:11:11.945+09:00",
                "source_repo_updated_at": "2024-09-19T01:11:11.944+09:00",
                "pinned": False,
                "path": "/sample_user/articles/sample-zenn-article",
                "user": {
                    "id": 123456,
                    "username": "sampleuser",
                    "name": "Sample User",
                    "avatar_small_url": "https://example.com/sample-avatar.jpg",
                },
                "publication": None,
            }
        ]
    }


@pytest.mark.skip
def test_return_response():
    repo = ZennArticleRepository()
    try:
        items = repo.fetch_items(page=1)
    except Exception as e:
        print(e)
        raise e
    print(items)


@patch("infrastructure.repository.zenn_article_repository.requests.get")
def test_処理が成功した場合_fetch_itemsがItemリストを返す(
    mock_get, mock_zenn_response
):
    # Arrange
    mock_response = Mock()
    mock_response.status_code = HTTPStatus.OK
    mock_response.json.return_value = mock_zenn_response
    mock_get.return_value = mock_response
    repo = ZennArticleRepository()

    # Act
    items = repo.fetch_items(page=1)

    # Assert
    assert isinstance(items, list)
    assert all(isinstance(item, Item) for item in items)
    assert len(items) == 1
    src = mock_zenn_response["articles"][0]
    item = items[0]
    assert item.title == src["title"]
    assert item.url == "https://zenn.dev" + src["path"]
    assert item.likes_count == src["liked_count"]


@patch("infrastructure.repository.zenn_article_repository.requests.get")
def test_status_not_ok_の場合_Exceptionをスローすること(mock_get):
    # Arrange
    mock_response = Mock()
    mock_response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    mock_response.text = "internal server error"
    mock_get.return_value = mock_response
    repo = ZennArticleRepository()

    # Act & Assert
    with pytest.raises(Exception) as excinfo:
        repo.fetch_items(page=1)
    assert "Zenn API error" in str(excinfo.value)


@patch("infrastructure.repository.zenn_article_repository.requests.get")
def test_requests_exception_の場合_Exceptionをスローすること(mock_get):
    # Arrange
    mock_get.side_effect = Exception("network error")
    repo = ZennArticleRepository()

    # Act & Assert
    with pytest.raises(Exception) as excinfo:
        repo.fetch_items(page=1)
    assert "network error" in str(excinfo.value)
