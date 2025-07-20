import requests
from http import HTTPStatus
from application.port.weather_port import IWeatherRepository
from application.domain.weather import Weather


class WeatherRepository(IWeatherRepository):
    # エリアを知りたい場合はこちら: https://www.jma.go.jp/bosai/common/const/area.json
    OSAKA_AREA_CODE = 270000
    BASE_URL = "https://www.jma.go.jp/bosai/forecast/data/forecast"

    def fetch(self) -> Weather:
        url = f"{self.BASE_URL}/{self.OSAKA_AREA_CODE}.json"
        resp = requests.get(url)
        if resp.status_code != HTTPStatus.OK:
            raise Exception(
                f"気象庁APIから200以外が返却されました。ステータスコード: {
                    resp.status_code} レスポンス内容: {
                    resp.text}"
            )
        data = resp.json()
        frt = data[0]["timeSeries"][0]["areas"][0]["weathers"][0]
        temps = data[0]["timeSeries"][2]["areas"][0].get("temps", [])
        min = int(temps[0]) if len(temps) > 0 and temps[0] else 0
        max = int(temps[1]) if len(temps) > 1 and temps[1] else 0
        return Weather(forecast=frt, min_temp=min, max_temp=max)
