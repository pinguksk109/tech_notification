
import unittest
from unittest.mock import MagicMock
from application.usecase.line_usecase import LineUsecase, LineSendInput
from domain.item import Item


class TestLineUsecase(unittest.TestCase):

    def setUp(self):
        self.mock_line_repository = MagicMock()

        self.line_usecase = LineUsecase(
            line_repository=self.mock_line_repository)

        self.day = "2024-01-01"
        self.line_usecase.today_date = self.day

    def test_処理が終了すること(self):
        qiita_items = [
            Item(
                title="Qiita記事1",
                url="https://qiita.com/article1",
                likes_count=2),
            Item(
                title="Qiita記事2",
                url="https://qiita.com/article2",
                likes_count=4),
        ]
        zenn_items = [
            Item(
                title="Zenn記事1",
                url="https://zenn.dev/article1",
                likes_count=6),
        ]

        input_data = LineSendInput(
            qiita_items=qiita_items,
            zenn_items=zenn_items)

        try:
            self.line_usecase.handle(input_data)
        except Exception as e:
            print(e)

        expected_qiita_message = (
            f"2024-01-01のQiitaおすすめ記事を送ります✍\n\n"
            "1. Qiita記事1 https://qiita.com/article1\n"
            "2. Qiita記事2 https://qiita.com/article2"
        )
        expected_zenn_message = (
            f"2024-01-01のZennおすすめ記事を送ります✍\n\n"
            "1. Zenn記事1 https://zenn.dev/article1"
        )

        self.mock_line_repository.send_message.assert_any_call(
            expected_qiita_message)
        self.mock_line_repository.send_message.assert_any_call(
            expected_zenn_message)
        self.assertEqual(self.mock_line_repository.send_message.call_count, 2)


if __name__ == '__main__':
    unittest.main()
