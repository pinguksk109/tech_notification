import pytest
from unittest.mock import patch, MagicMock
from lambda_function import lambda_handler
from application.usecase.tech_recommend_usecase import TechRecommendUsecase, QiitaRecommendOutput, ZennRecommendOutput
from application.usecase.line_usecase import LineUsecase
from application.usecase.train_info_usecase import TrainInfoOutput
from application.usecase.weather_usecase import WeatherOutput
from domain.item import Item

@pytest.fixture
def mock_usecases():
    with patch('lambda_function.LineUsecase') as mock_line_usecase, \
        patch('lambda_function.TechRecommendUsecase') as mock_tech_recommend_usecase, \
        patch('lambda_function.QiitaApiRepository') as mock_qiita_repository, \
        patch('lambda_function.ZennApiRepository') as mock_zenn_repository, \
        patch('lambda_function.TrainInfoUsecase') as mock_train_info_usecase, \
        patch('lambda_function.WeatherUsecase') as mock_weather_usecase, \
        patch('lambda_function.WeatherRepository') as mock_weather_repository, \
        patch('lambda_function.ScraperRepository') as mock_scraper_repository:

        yield {
            'mock_line_usecase': mock_line_usecase,
            'mock_tech_recommend_usecase': mock_tech_recommend_usecase,
            'mock_qiita_repository': mock_qiita_repository,
            'mock_zenn_repository': mock_zenn_repository,
            'mock_train_info_usecase': mock_train_info_usecase,
            'mock_weather_usecase': mock_weather_usecase,
            'mock_weather_repository': mock_weather_repository,
            'mock_scraper_repository': mock_scraper_repository,
        }

def test_処理が成功した場合_200を返すこと(mock_usecases):
    mock_tech_recommend_usecase = mock_usecases['mock_tech_recommend_usecase'].return_value
    mock_tech_recommend_usecase.qiita_handle.return_value = QiitaRecommendOutput(
        items=[Item(title="Qiita Article", url="https://qiita.com/article1", likes_count=10)]
    )
    mock_tech_recommend_usecase.zenn_handle.return_value = ZennRecommendOutput(
        items=[Item(title="Zenn Article", url="https://zenn.dev/article1", likes_count=5)]
    )
    mock_train_info_usecase = mock_usecases['mock_train_info_usecase'].return_value
    mock_train_info_usecase.handle.return_value = TrainInfoOutput(
        abnormal_train=[]
    )
    mock_weather_usecase = mock_usecases['mock_weather_usecase'].return_value
    mock_weather_usecase.handle.return_value = WeatherOutput(
        forecast="はれ"
    )

    mock_line_usecase_instance = mock_usecases['mock_line_usecase'].return_value
    mock_line_usecase_instance.handle = MagicMock()

    event = {}
    context = {}

    actual = lambda_handler(event, context)

    assert actual == {
        "status_code": 200,
        "body": "Success"
    }

def test_qiitaの処理でExceptionが発生した場合_500を返すこと(mock_usecases):

    mock_tech_recommend_usecase = mock_usecases['mock_tech_recommend_usecase'].return_value
    mock_tech_recommend_usecase.qiita_handle.side_effect = Exception("Qiita API error")

    mock_train_info_usecase = mock_usecases['mock_train_info_usecase'].return_value
    mock_train_info_usecase.handle.return_value = TrainInfoOutput(
        abnormal_train=[]
    )

    mock_weather_usecase = mock_usecases['mock_weather_usecase'].return_value
    mock_weather_usecase.handle.return_value = WeatherOutput(
        forecast="はれ"
    )

    event = {}
    context = {}

    actual = lambda_handler(event, context)

    assert actual["status_code"] == 500

def test_zennの処理でExceptionが発生した場合_500を返すこと(mock_usecases):

    mock_tech_recommend_usecase = mock_usecases['mock_tech_recommend_usecase'].return_value
    mock_tech_recommend_usecase.qiita_handle.return_value = QiitaRecommendOutput(
        items=[Item(title="Qiita Article", url="https://qiita.com/article1", likes_count=10)]
    )
    mock_tech_recommend_usecase.zenn_handle.side_effect = Exception("Zenn API error")

    mock_train_info_usecase = mock_usecases['mock_train_info_usecase'].return_value
    mock_train_info_usecase.handle.return_value = TrainInfoOutput(
        abnormal_train=[]
    )

    mock_weather_usecase = mock_usecases['mock_weather_usecase'].return_value
    mock_weather_usecase.handle.return_value = WeatherOutput(
        forecast="はれ"
    )

    event = {}
    context = {}

    actual = lambda_handler(event, context)

    assert actual["status_code"] == 500

def test_メッセージ送信の処理でExceptionが発生した場合_500を返すこと(mock_usecases):
    mock_tech_recommend_usecase = mock_usecases['mock_tech_recommend_usecase'].return_value
    mock_tech_recommend_usecase.qiita_handle.return_value = QiitaRecommendOutput(
        items=[Item(title="Qiita Article", url="https://qiita.com/article1", likes_count=10)]
    )
    mock_tech_recommend_usecase.zenn_handle.return_value = ZennRecommendOutput(
        items=[Item(title="Zenn Article", url="https://zenn.dev/article1", likes_count=5)]
    )

    mock_train_info_usecase = mock_usecases['mock_train_info_usecase'].return_value
    mock_train_info_usecase.handle.return_value = TrainInfoOutput(
        abnormal_train=[]
    )

    mock_weather_usecase = mock_usecases['mock_weather_usecase'].return_value
    mock_weather_usecase.handle.return_value = WeatherOutput(
        forecast="はれ"
    )

    mock_line_usecase_instance = mock_usecases['mock_line_usecase'].return_value
    mock_line_usecase_instance.handle.side_effect = Exception("Line API error")

    event = {}
    context = {}

    actual = lambda_handler(event, context)

    assert actual["status_code"] == 500