import unittest
from unittest.mock import patch, MagicMock
from lambda_function import lambda_handler
from application.usecase.tech_recommend_usecase import QiitaRecommendOutput, ZennRecommendOutput
from domain.item import Item


class TestLambdaHandler(unittest.TestCase):

    @patch('lambda_function.LineUsecase')
    @patch('lambda_function.TechRecommendUsecase')
    @patch('lambda_function.QiitaApiRepository')
    @patch('lambda_function.ZennApiRepository')
    def test_処理が成功した場合_200を返すこと(
            self,
            mock_zenn_repository,
            mock_qiita_repository,
            mock_tech_recommend_usecase,
            mock_line_usecase):

        mock_tech_recommend_usecase = mock_tech_recommend_usecase.return_value

        mock_tech_recommend_usecase.qiita_handle.return_value = QiitaRecommendOutput(
            items=[Item(title="Qiita Article", url="https://qiita.com/article1", likes_count=10)]
        )

        mock_tech_recommend_usecase.zenn_handle.return_value = ZennRecommendOutput(
            items=[Item(title="Zenn Article", url="https://zenn.dev/article1", likes_count=5)]
        )

        mock_line_usecase_instance = mock_line_usecase.return_value
        mock_line_usecase_instance.handle = MagicMock()

        event = {}
        context = {}

        actual = lambda_handler(event, context)
        self.assertEqual(actual, {
            "status_code": 200,
            "body": "Success"
        })

    @patch('lambda_function.LineUsecase')
    @patch('lambda_function.TechRecommendUsecase')
    @patch('lambda_function.QiitaApiRepository')
    @patch('lambda_function.ZennApiRepository')
    def test_qiitaの処理を行うusecaseでExceptionがスローされた場合_500を返すこと(
            self,
            mock_zenn_repository,
            mock_qiita_repository,
            mock_tech_recommend_usecase,
            mock_line_usecase):

        mock_tech_recommend_usecase = mock_tech_recommend_usecase.return_value
        mock_tech_recommend_usecase.qiita_handle.side_effect = Exception()

        mock_tech_recommend_usecase.zenn_handle.return_value = ZennRecommendOutput(
            items=[Item(title="Zenn Article", url="https://zenn.dev/article1", likes_count=5)]
        )

        mock_line_usecase_instance = mock_line_usecase.return_value
        mock_line_usecase_instance.handle = MagicMock()

        event = {}
        context = {}

        actual = lambda_handler(event, context)

        self.assertEqual(actual["status_code"], 500)

    @patch('lambda_function.LineUsecase')
    @patch('lambda_function.TechRecommendUsecase')
    @patch('lambda_function.QiitaApiRepository')
    @patch('lambda_function.ZennApiRepository')
    def test_zennの処理を行うusecaseでExceptionがスローされた場合_500を返すこと(
            self,
            mock_zenn_repository,
            mock_qiita_repository,
            mock_tech_recommend_usecase,
            mock_line_usecase):

        mock_tech_recommend_usecase = mock_tech_recommend_usecase.return_value
        mock_tech_recommend_usecase.qiita_handle.return_value = QiitaRecommendOutput(
            items=[Item(title="Qiita Article", url="https://qiita.com/article1", likes_count=10)]
        )

        mock_tech_recommend_usecase.zenn_handle.side_effect = Exception()

        mock_line_usecase_instance = mock_line_usecase.return_value
        mock_line_usecase_instance.handle = MagicMock()

        event = {}
        context = {}

        actual = lambda_handler(event, context)

        self.assertEqual(actual["status_code"], 500)

    @patch('lambda_function.LineUsecase')
    @patch('lambda_function.TechRecommendUsecase')
    @patch('lambda_function.QiitaApiRepository')
    @patch('lambda_function.ZennApiRepository')
    def test_メッセージを送るusecaseでExceptionがスローされた場合_500を返すこと(
            self,
            mock_zenn_repository,
            mock_qiita_repository,
            mock_tech_recommend_usecase,
            mock_line_usecase):

        mock_tech_recommend_usecase = mock_tech_recommend_usecase.return_value
        mock_tech_recommend_usecase.qiita_handle.return_value = QiitaRecommendOutput(
            items=[Item(title="Qiita Article", url="https://qiita.com/article1", likes_count=10)]
        )

        mock_tech_recommend_usecase.zenn_handle.return_value = ZennRecommendOutput(
            items=[Item(title="Zenn Article", url="https://zenn.dev/article1", likes_count=5)]
        )
        mock_line_usecase_instance = mock_line_usecase.return_value
        mock_line_usecase_instance.handle.side_effect = Exception()

        event = {}
        context = {}

        actual = lambda_handler(event, context)

        self.assertEqual(actual["status_code"], 500)
