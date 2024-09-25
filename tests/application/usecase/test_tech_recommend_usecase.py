import unittest
from unittest.mock import MagicMock
from application.usecase.tech_recommend_usecase import TechRecommendUsecase, QiitaRecommendOutput, ZennRecommendOutput
from domain.item import Item


class TestTechRecommendUsecase(unittest.TestCase):

    def setUp(self):
        self.mock_qiita_api_repository = MagicMock()
        self.mock_zenn_api_repository = MagicMock()

        self.usecase = TechRecommendUsecase(
            qiita_api_repository=self.mock_qiita_api_repository,
            zenn_api_repository=self.mock_zenn_api_repository
        )

    def test_qiita_handle_処理が成功した場合_おすすめ記事を返すこと(self):
        self.mock_qiita_api_repository.get_items.return_value = [
            {
                "rendered_body": "This is a blurred rendered body example.",
                "body": "This is a blurred body content example.",
                "coediting": False,
                "comments_count": 10,
                "created_at": "2023-07-01T12:34:56+09:00",
                "group": None,
                "id": "1234567890abcdef",
                "likes_count": 20,  # likes_count >= 3
                "private": False,
                "reactions_count": 5,
                "tags": [
                    {"name": "LLM", "versions": ["v1.0", "v1.1"]},
                    {"name": "evaluation", "versions": []}
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

        actual = self.usecase.qiita_handle()

        self.assertEqual(len(actual.items), 5)
        self.assertEqual(
            actual.items[0].title,
            "Introduction to LLM Evaluation Methods")
        self.assertEqual(
            actual.items[0].url,
            "https://example.com/articles/123456")
        self.assertEqual(actual.items[0].likes_count, 20)

        self.assertEqual(
            actual.items[1].title,
            "Introduction to LLM Evaluation Methods")
        self.assertEqual(
            actual.items[1].url,
            "https://example.com/articles/123456")
        self.assertEqual(actual.items[1].likes_count, 20)

        self.assertEqual(
            actual.items[2].title,
            "Introduction to LLM Evaluation Methods")
        self.assertEqual(
            actual.items[2].url,
            "https://example.com/articles/123456")
        self.assertEqual(actual.items[2].likes_count, 20)

        self.assertEqual(
            actual.items[3].title,
            "Introduction to LLM Evaluation Methods")
        self.assertEqual(
            actual.items[3].url,
            "https://example.com/articles/123456")
        self.assertEqual(actual.items[3].likes_count, 20)

        self.assertEqual(
            actual.items[4].title,
            "Introduction to LLM Evaluation Methods")
        self.assertEqual(
            actual.items[4].url,
            "https://example.com/articles/123456")
        self.assertEqual(actual.items[4].likes_count, 20)

    def test_zenn_handle_処理が成功した場合_おすすめ記事を返すこと(self):
        self.mock_zenn_api_repository.get_items.return_value = {
            "articles": [
                {
                    "id": 123456,
                    "post_type": "Article",
                    "title": "Sample Title: How to Create a Project with Angular CLI without Git",
                    "slug": "sample-angular-cli-tips",
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
                    "path": "/sample_user/articles/angular-cli-tips",
                    "user": {
                        "id": 123456,
                        "username": "sampleuser",
                        "name": "Sample User",
                        "avatar_small_url": "https://example.com/sample-avatar.jpg"},
                    "publication": None}]}

        actual = self.usecase.zenn_handle()

        self.assertEqual(len(actual.items), 5)
        self.assertEqual(
            actual.items[0].title,
            "Sample Title: How to Create a Project with Angular CLI without Git")
        self.assertEqual(
            actual.items[0].url,
            "https://zenn.dev/sample_user/articles/angular-cli-tips")
        self.assertEqual(actual.items[0].likes_count, 5)

        self.assertEqual(
            actual.items[1].title,
            "Sample Title: How to Create a Project with Angular CLI without Git")
        self.assertEqual(
            actual.items[1].url,
            "https://zenn.dev/sample_user/articles/angular-cli-tips")
        self.assertEqual(actual.items[1].likes_count, 5)

        self.assertEqual(
            actual.items[2].title,
            "Sample Title: How to Create a Project with Angular CLI without Git")
        self.assertEqual(
            actual.items[2].url,
            "https://zenn.dev/sample_user/articles/angular-cli-tips")
        self.assertEqual(actual.items[2].likes_count, 5)

        self.assertEqual(
            actual.items[3].title,
            "Sample Title: How to Create a Project with Angular CLI without Git")
        self.assertEqual(
            actual.items[3].url,
            "https://zenn.dev/sample_user/articles/angular-cli-tips")
        self.assertEqual(actual.items[3].likes_count, 5)

        self.assertEqual(
            actual.items[4].title,
            "Sample Title: How to Create a Project with Angular CLI without Git")
        self.assertEqual(
            actual.items[4].url,
            "https://zenn.dev/sample_user/articles/angular-cli-tips")
        self.assertEqual(actual.items[4].likes_count, 5)
