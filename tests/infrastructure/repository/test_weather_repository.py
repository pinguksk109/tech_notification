import pytest
from infrastructure.repository.weather_repository import WeatherRepository


@pytest.mark.skip
def test_should_return_weather_when_fetch_is_called_with_real_api():
    # 1. setup
    repo = WeatherRepository()

    # 2. execute
    try:
        data = repo.fetch()
    except Exception as e:
        print(e)
        raise e

    # 3. verify
    print(data)
