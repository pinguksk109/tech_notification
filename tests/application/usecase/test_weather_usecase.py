import asyncio
from unittest.mock import AsyncMock, MagicMock

from application.domain.weather import Weather
from application.usecase.weather_usecase import (
    WeatherSummaryResponse,
    WeatherUsecase,
)


def test_should_return_weather_forecasts_for_osaka_and_hanoi_when_handle_is_called():
    # 1. setup
    mock_jma_repository = MagicMock()
    mock_jma_repository.fetch.return_value = Weather(
        forecast="大阪の元予報",
        min_temp=10,
        max_temp=25,
    )
    mock_open_meteo_repository = MagicMock()
    mock_open_meteo_repository.fetch.return_value = Weather(
        forecast="気温予報",
        min_temp=25,
        max_temp=36,
    )
    mock_llm_repository = MagicMock()
    mock_llm_repository.request = AsyncMock(
        return_value=WeatherSummaryResponse(summary="大阪の要約予報")
    )

    usecase = WeatherUsecase(
        jma_weather_repository=mock_jma_repository,
        open_meteo_weather_repository=mock_open_meteo_repository,
        llm_repository=mock_llm_repository,
    )

    # 2. execute
    actual = asyncio.run(usecase.handle())

    # 3. verify
    assert len(actual.forecasts) == 2
    assert actual.forecasts[0].city_name == "大阪市"
    assert actual.forecasts[0].forecast == "大阪の要約予報"
    assert actual.forecasts[0].min_temp == 10
    assert actual.forecasts[0].max_temp == 25
    assert actual.forecasts[1].city_name == "ハノイ市"
    assert actual.forecasts[1].forecast == "気温予報"
    assert actual.forecasts[1].min_temp == 25
    assert actual.forecasts[1].max_temp == 36

    mock_jma_repository.fetch.assert_called_once_with()
    mock_llm_repository.request.assert_awaited_once_with(
        "大阪の元予報", WeatherSummaryResponse
    )
    mock_open_meteo_repository.fetch.assert_called_once_with(
        latitude=21.03,
        longitude=105.85,
        timezone="Asia/Bangkok",
    )
