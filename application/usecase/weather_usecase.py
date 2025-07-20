from pydantic import BaseModel
from application.port.weather_port import IWeatherRepository
from application.base import IOutput, IUsecase


class WeatherOutput(IOutput, BaseModel):
    forecast: str


class WeatherUsecase(IUsecase[WeatherOutput]):

    def __init__(self, weather_repository: IWeatherRepository):
        self.weather_repository = weather_repository

    def handle(self) -> WeatherOutput:
        # 大阪のエリアコードを代入
        # エリアを知りたい場合はこちら: https://www.jma.go.jp/bosai/common/const/area.json
        osaka_code = 270000
        response = self.weather_repository.fetch(osaka_code)
        return WeatherOutput(
            forecast=response[0]["timeSeries"][0]["areas"][0]["weathers"][0]
        )
