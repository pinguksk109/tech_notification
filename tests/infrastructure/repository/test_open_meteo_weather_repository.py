from http import HTTPStatus
from unittest.mock import Mock, patch

import pytest

from infrastructure.repository.open_meteo_weather_repository import (
    OpenMeteoWeatherRepository,
)


@patch("infrastructure.repository.open_meteo_weather_repository.requests.get")
def test_should_return_today_temperature_when_open_meteo_response_is_valid(
    mock_get,
):
    # 1. setup
    mock_response = Mock()
    mock_response.status_code = HTTPStatus.OK
    mock_response.json.return_value = {
        "daily": {
            "temperature_2m_max": [35.6, 35.7],
            "temperature_2m_min": [24.7, 25.4],
        }
    }
    mock_get.return_value = mock_response

    repo = OpenMeteoWeatherRepository()

    # 2. execute
    actual = repo.fetch(
        latitude=21.03,
        longitude=105.85,
        timezone="Asia/Bangkok",
    )

    # 3. verify
    assert actual.forecast == "気温予報"
    assert actual.min_temp == 25
    assert actual.max_temp == 36


@patch("infrastructure.repository.open_meteo_weather_repository.requests.get")
def test_should_raise_exception_when_open_meteo_returns_non_ok_status(
    mock_get,
):
    # 1. setup
    mock_response = Mock()
    mock_response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
    mock_response.text = "internal server error"
    mock_get.return_value = mock_response

    repo = OpenMeteoWeatherRepository()

    # 2. execute
    with pytest.raises(Exception) as excinfo:
        repo.fetch(
            latitude=21.03,
            longitude=105.85,
            timezone="Asia/Bangkok",
        )

    # 3. verify
    assert "Open-Meteo APIから200以外" in str(excinfo.value)


def test_should_raise_value_error_when_required_parameters_are_missing():
    # 1. setup
    repo = OpenMeteoWeatherRepository()

    # 2. execute
    with pytest.raises(ValueError) as excinfo:
        repo.fetch()

    # 3. verify
    assert "latitude, longitude, timezone が必要" in str(excinfo.value)


@patch("infrastructure.repository.open_meteo_weather_repository.requests.get")
def test_should_raise_exception_when_daily_temperatures_are_missing(
    mock_get,
):
    # 1. setup
    mock_response = Mock()
    mock_response.status_code = HTTPStatus.OK
    mock_response.json.return_value = {"daily": {}}
    mock_get.return_value = mock_response

    repo = OpenMeteoWeatherRepository()

    # 2. execute
    with pytest.raises(Exception) as excinfo:
        repo.fetch(
            latitude=21.03,
            longitude=105.85,
            timezone="Asia/Bangkok",
        )

    # 3. verify
    assert "temperature_2m_min または temperature_2m_max" in str(excinfo.value)
