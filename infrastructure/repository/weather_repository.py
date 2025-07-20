from typing import Any, Dict
import requests
import os
import json
from http import HTTPStatus
from application.port.weather_port import IWeatherRepository


class WeatherRepository(IWeatherRepository):
    def __init__(self):
        self.base_url = os.getenv(
            "JMA_BASE_URL",
            "https://www.jma.go.jp/bosai/forecast/data/forecast",
        )

    def fetch(self, area_code: int):
        url = f"{self.base_url}/{area_code}.json"
        try:
            resp = requests.get(url)
        except Exception as e:
            raise Exception(
                f"気象庁APIから天気取得のリクエストに失敗しました エラー内容: {e}"
            )
        if resp.status_code != HTTPStatus.OK:
            raise Exception(
                f"気象庁APIから200以外が返却されました。ステータスコード: {
                    resp.status_code} レスポンス内容: {
                    resp.text}"
            )
        return resp.json()
