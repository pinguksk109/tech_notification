import unittest
from unittest.mock import patch, Mock
from infrastructure.repository.line_repository import LineRepository
from http import HTTPStatus

class TestLieApiRepository(unittest.TestCase):

    @patch('infrastructure.repository.line_repository.requests.post')
    def test_処理が成功した場合_処理が終了すること(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.OK
        mock_post.return_value = mock_response

        repository = LineRepository()

        try:
            repository.send_message("Hello")
        except Exception as e:
            print(e)

    @patch('infrastructure.repository.line_repository.requests.post')
    def test_500の場合_Excecptionをスローすること(self, mock_post):
        mock_response = Mock()
        mock_response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        mock_post.return_value = mock_response

        repository = LineRepository()

        with self.assertRaises(Exception):
            repository.send_message('Hello')

    @patch('infrastructure.repository.line_repository.requests.post')
    def test_リクエストに失敗した場合_Excecptionをスローすること(self, mock_post):
        mock_post.side_effect = Exception()

        repository = LineRepository()

        with self.assertRaises(Exception):
            repository.send_message('Hello')