import pytest
from unittest.mock import patch, Mock
from infrastructure.repository.qiita_article_repository import (
    QiitaArticleRepository,
)
from http import HTTPStatus
from application.domain.item import Item
from typing import List, Dict, Any


@pytest.fixture
def mock_qiita_response() -> List[Dict[str, Any]]:
    return [
        {
            "rendered_body": "This is a blurred rendered body example.",
            "body": "This is a blurred body content example, providing an overview of LLM evaluations and introducing key concepts. More detailed information is available in the survey paper [A Survey on Evaluation of Large Language Models (arXiv: 2307.03109)](https://example.com).",
            "coediting": False,
            "comments_count": 10,
            "created_at": "2023-07-01T12:34:56+09:00",
            "group": None,
            "id": "1234567890abcdef",
            "likes_count": 20,
            "private": False,
            "reactions_count": 5,
            "tags": [
                {"name": "LLM", "versions": ["v1.0", "v1.1"]},
                {"name": "evaluation", "versions": []},
            ],
            "title": "Introduction to LLM Evaluation Methods",
            "updated_at": "2023-07-02T12:00:00+09:00",
            "url": "https://example.com/articles/123456",
            "user": {
                "description": "This is a user description example.",
                "facebook_id": "exampleuser",
                "followees_count": 100,
                "followers_count": 50,
                "github_login_name": "example_github",
                "id": "example_user_id",
                "items_count": 25,
                "linkedin_id": "example_linkedin",
                "location": "Tokyo, Japan",
                "name": "Example User",
                "organization": "Example Organization",
                "permanent_id": 123456,
                "profile_image_url": "https://example.com/profile_image.jpg",
                "team_only": False,
                "twitter_screen_name": "example_twitter",
                "website_url": "https://example.com",
            },
            "page_views_count": 500,
            "team_membership": None,
            "organization_url_name": None,
        }
    ]


@pytest.mark.skip
def test_should_return_items_when_fetch_items_is_called_with_real_api():
    # 1. setup
    repo = QiitaArticleRepository()

    # 2. execute
    try:
        items = repo.fetch_items(page=1)
    except Exception as e:
        print(e)
        raise e

    # 3. verify
    print(items)


@patch("infrastructure.repository.qiita_article_repository.requests.get")
def test_should_return_items_when_qiita_api_returns_ok_response(
    mock_get, mock_qiita_response
):
    # 1. setup
    mock_response = Mock()
    mock_response.status_code = HTTPStatus.OK
    mock_response.json.return_value = mock_qiita_response
    mock_get.return_value = mock_response
    repo = QiitaArticleRepository()

    # 2. execute
    result = repo.fetch_items(page=1)

    # 3. verify
    assert isinstance(result, list)
    assert all(isinstance(item, Item) for item in result)
    assert len(result) == 1
    src = mock_qiita_response[0]
    item = result[0]
    assert item.title == src["title"]
    assert item.url == src["url"]
    assert item.likes_count == src["likes_count"]


@patch("infrastructure.repository.qiita_article_repository.requests.get")
def test_should_raise_exception_when_qiita_api_is_rate_limited(mock_get):
    # 1. setup
    mock_response = Mock()
    mock_response.status_code = HTTPStatus.FORBIDDEN
    mock_response.text = "rate limit"
    mock_get.return_value = mock_response
    repo = QiitaArticleRepository()

    # 2. execute
    with pytest.raises(Exception) as excinfo:
        repo.fetch_items(page=1)

    # 3. verify
    assert "rate limited" in str(excinfo.value)


@patch("infrastructure.repository.qiita_article_repository.requests.get")
def test_should_raise_exception_when_qiita_api_returns_non_ok_status(mock_get):
    # 1. setup
    mock_response = Mock()
    mock_response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    mock_response.text = "internal server error"
    mock_get.return_value = mock_response
    repo = QiitaArticleRepository()

    # 2. execute
    with pytest.raises(Exception) as excinfo:
        repo.fetch_items(page=1)

    # 3. verify
    assert "Qiita API error" in str(excinfo.value)


@patch("infrastructure.repository.qiita_article_repository.requests.get")
def test_should_raise_exception_when_qiita_request_fails(mock_get):
    # 1. setup
    mock_get.side_effect = Exception("network error")
    repo = QiitaArticleRepository()

    # 2. execute
    with pytest.raises(Exception) as excinfo:
        repo.fetch_items(page=1)

    # 3. verify
    assert "network error" in str(excinfo.value)
