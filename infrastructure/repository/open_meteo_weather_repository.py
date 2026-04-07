from http import HTTPStatus

import requests

from application.domain.weather import Weather
from application.port.weather_port import IWeatherRepository


class OpenMeteoWeatherRepository(IWeatherRepository):
    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    def fetch(
        self,
        *,
        latitude: float | None = None,
        longitude: float | None = None,
        timezone: str | None = None,
    ) -> Weather:
        if latitude is None or longitude is None or timezone is None:
            raise ValueError(
                "Open-Meteoの天気取得には latitude, longitude, timezone が必要です。"
            )

        resp = requests.get(
            self.BASE_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "daily": "temperature_2m_max,temperature_2m_min",
                "timezone": timezone,
            },
        )
        if resp.status_code != HTTPStatus.OK:
            raise Exception(
                "Open-Meteo APIから200以外が返却されました。"
                f"ステータスコード: {resp.status_code} "
                f"レスポンス内容: {resp.text}"
            )

        data = resp.json()
        daily = data.get("daily")
        if daily is None:
            raise Exception("Open-Meteo APIレスポンスに daily が含まれていません。")

        min_temps = daily.get("temperature_2m_min", [])
        max_temps = daily.get("temperature_2m_max", [])
        if not min_temps or not max_temps:
            raise Exception(
                "Open-Meteo APIレスポンスに temperature_2m_min または "
                "temperature_2m_max が含まれていません。"
            )

        return Weather(
            forecast="気温予報",
            min_temp=round(min_temps[0]),
            max_temp=round(max_temps[0]),
        )
