import pytest
from infrastructure.repository.weather_repository import WeatherRepository


@pytest.mark.skip
def test_return_response():
    repo = WeatherRepository()
    try:
        data = repo.fetch(270000)
    except Exception as e:
        print(e)
        raise e
    print(data)
