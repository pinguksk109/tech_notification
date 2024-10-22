import pytest
from unittest.mock import patch, Mock
from infrastructure.repository.zenn_repository import ZennApiRepository
from http import HTTPStatus


@pytest.fixture
def mock_zenn_response():
    return {
        "articles": [
            {
                "id": 123456,
                "post_type": "Article",
                "title": "Sample Title: How to Create a Project with Angular CLI without Git",
                "slug": "sample-angular-cli-tips",
                "comments_count": 0,
                "liked_count": 0,
                "body_letters_count": 350,
                "article_type": "tech",
                "emoji": "🤔",
                "is_suspending_private": False,
                "published_at": "2024-09-19T01:11:11.945+09:00",
                "body_updated_at": "2024-09-19T01:11:11.945+09:00",
                "source_repo_updated_at": "2024-09-19T01:11:11.944+09:00",
                "pinned": False,
                "path": "/sample_user/articles/angular-cli-tips",
                "user": {
                    "id": 123456,
                    "username": "sampleuser",
                    "name": "Sample User",
                    "avatar_small_url": "https://example.com/sample-avatar.jpg"},
                "publication": None
            }
        ]
    }

@patch('infrastructure.repository.zenn_repository.requests.get')
def test_処理が成功した場合_レスポンスを返すこと(mock_get, mock_zenn_response):
    mock_response = Mock()
    mock_response.status_code = HTTPStatus.OK
    mock_response.json_return = mock_zenn_response
    mock_get.return_value = mock_response

    repository = ZennApiRepository()
    actual = repository.get_items(page=1)

    assert actual == mock_zenn_response

@patch('infrastructure.repository.zenn_repository.requests.get')
def test_500の場合_Exceptionをスローすること(mock_get):
    mock_response = Mock()
    mock_response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    mock_response.text = "internal server error"
    mock_get.return_value = mock_response

    repository = ZennApiRepository()

    with pytest.raises(Exception):
        repository.get_items(page=1)

@patch('infrastructure.repository.zenn_repository.requests.get')
def test_リクエストに失敗した場合_Exceptionをスローすること(mock_get):
    mock_get.side_effect = Exception()

    repository = ZennApiRepository()

    with pytest.raises(Exception):
        repository.get_items(page=1)