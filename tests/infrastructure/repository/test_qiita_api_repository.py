import unittest
from unittest.mock import patch, Mock
from infrastructure.repository.qiita_api_repository import QiitaApiRepository
from http import HTTPStatus
from typing import List, Dict, Any

class TestQiitaApiRepository(unittest.TestCase):
    
    @patch('infrastructure.repository.qiita_api_repository.requests.get')
    def test_処理が成功した場合_レスポンスを返すこと(self, mock_get):
        
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK
        mock_response.json.return_value = self.mock_qiita_response()
        mock_get.return_value = mock_response

        repository = QiitaApiRepository()

        actual = repository.get_items(page=1)

        self.assertEqual(actual, self.mock_qiita_response())

    @patch('infrastructure.repository.qiita_api_repository.requests.get')
    def test_レートリミットの場合_Exceptionをスローすること(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.FORBIDDEN
        mock_response.text = "rate limit"
        mock_get.return_value = mock_response

        repository = QiitaApiRepository()

        with self.assertRaises(Exception) as context:
            repository.get_items(page=1)

    @patch('infrastructure.repository.qiita_api_repository.requests.get')
    def test_500の場合_Exceptionをスローすること(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        mock_response.text = "internal server error"
        mock_get.return_value = mock_response

        repository = QiitaApiRepository()

        with self.assertRaises(Exception):
            repository.get_items(page=1)

    @patch('infrastructure.repository.qiita_api_repository.requests.get')
    def test_クエストに失敗した場合_Exceptionをスローすること(self, mock_get):
        mock_get.side_effect = Exception()

        repository = QiitaApiRepository()

        with self.assertRaises(Exception) as context:
            repository.get_items(page=1)

    @staticmethod
    def mock_qiita_response() -> List[Dict[str, Any]]:
        message = [
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
                    {
                        "name": "LLM",
                        "versions": ["v1.0", "v1.1"]
                    },
                    {
                        "name": "evaluation",
                        "versions": []
                    }
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
                    "website_url": "https://example.com"
                },
                "page_views_count": 500,
                "team_membership": None,
                "organization_url_name": None
            }
        ]
        return message

if __name__ == '__main__':
    unittest.main()