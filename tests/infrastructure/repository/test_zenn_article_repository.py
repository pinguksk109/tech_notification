import pytest
from unittest.mock import patch, Mock
from infrastructure.repository.zenn_article_repository import (
    ZennArticleRepository,
)
from http import HTTPStatus
from application.domain.item import Item
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
def test_should_return_items_when_fetch_items_is_called_with_real_api():
    # 1. setup
    repo = ZennArticleRepository()

    # 2. execute
    try:
        items = repo.fetch_items(page=1)
    except Exception as e:
        print(e)
        raise e

    # 3. verify
    print(items)


@patch("infrastructure.repository.zenn_article_repository.requests.get")
def test_should_return_items_when_zenn_api_returns_ok_response(
    mock_get, mock_zenn_response
):
    # 1. setup
    mock_response = Mock()
    mock_response.status_code = HTTPStatus.OK
    mock_response.json.return_value = mock_zenn_response
    mock_get.return_value = mock_response
    repo = ZennArticleRepository()

    # 2. execute
    items = repo.fetch_items(page=1)

    # 3. verify
    assert isinstance(items, list)
    assert all(isinstance(item, Item) for item in items)
    assert len(items) == 1
    src = mock_zenn_response["articles"][0]
    item = items[0]
    assert item.title == src["title"]
    assert item.url == "https://zenn.dev" + src["path"]
    assert item.likes_count == src["liked_count"]


@patch("infrastructure.repository.zenn_article_repository.requests.get")
def test_should_raise_exception_when_zenn_api_returns_non_ok_status(mock_get):
    # 1. setup
    mock_response = Mock()
    mock_response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    mock_response.text = "internal server error"
    mock_get.return_value = mock_response
    repo = ZennArticleRepository()

    # 2. execute
    with pytest.raises(Exception) as excinfo:
        repo.fetch_items(page=1)

    # 3. verify
    assert "Zenn API error" in str(excinfo.value)


@patch("infrastructure.repository.zenn_article_repository.requests.get")
def test_should_raise_exception_when_zenn_request_fails(mock_get):
    # 1. setup
    mock_get.side_effect = Exception("network error")
    repo = ZennArticleRepository()

    # 2. execute
    with pytest.raises(Exception) as excinfo:
        repo.fetch_items(page=1)

    # 3. verify
    assert "network error" in str(excinfo.value)
