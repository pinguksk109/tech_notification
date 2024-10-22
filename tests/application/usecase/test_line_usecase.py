import pytest
from unittest.mock import MagicMock
from application.usecase.line_usecase import LineUsecase, LineSendInput
from domain.item import Item

@pytest.fixture
def line_usecase():
    mock_line_repository = MagicMock()
    line_usecase_instance = LineUsecase(line_repository=mock_line_repository)
    line_usecase_instance.today_date = "2024-01-01"
    return line_usecase_instance, mock_line_repository

def test_処理が終了すること(line_usecase):
    line_usecase_instance, mock_line_repository = line_usecase

    qiita_items = [
        Item(title="Qiita記事1", url="https://qiita.com/article1", likes_count=2),
        Item(title="Qiita記事2", url="https://qiita.com/article2", likes_count=4),
    ]
    zenn_items = [
        Item(title="Zenn記事1", url="https://zenn.dev/article1", likes_count=6),
    ]
    abnormal_train = []
    weather_forecast = "はれ"

    input_data = LineSendInput(qiita_items=qiita_items, zenn_items=zenn_items, abnormal_train=abnormal_train, weather_forecast=weather_forecast)

    try:
        line_usecase_instance.handle(input_data)
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

    mock_line_repository.send_message.assert_any_call(expected_qiita_message)
    mock_line_repository.send_message.assert_any_call(expected_zenn_message)
    assert mock_line_repository.send_message.call_count == 4