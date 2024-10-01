from pydantic import BaseModel
from infrastructure.repository.weather_repository import WeatherRepository
from application.base import IOutput


class WeatherOutput(IOutput, BaseModel):
    forecast: str


class WeatherUsecase():

    def __init__(self, weather_repository: WeatherRepository):
        self.weather_repository = weather_repository
    
    def handle(self) -> WeatherOutput:
        # 大阪のエリアコードを代入
        # エリアを知りたい場合はこちら: https://www.jma.go.jp/bosai/common/const/area.json 
        osaka_code = 270000
        response = self.weather_repository.fetch(osaka_code)
        return WeatherOutput(forecast=response[0]["timeSeries"][0]["areas"][0]["weathers"][0])