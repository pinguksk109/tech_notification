from pydantic import BaseModel
from application.port.weather_port import IWeatherRepository
from application.port.llm_summary_port import LlmSummaryPort
from application.base import IOutput, IUsecase


class WeatherSummaryResponse(BaseModel):
    summary: str


class CityWeatherOutput(BaseModel):
    city_name: str
    forecast: str
    min_temp: int
    max_temp: int


class WeatherOutput(IOutput, BaseModel):
    forecasts: list[CityWeatherOutput]


class WeatherUsecase(IUsecase[WeatherOutput]):
    HANOI_LATITUDE = 21.03
    HANOI_LONGITUDE = 105.85
    HANOI_TIMEZONE = "Asia/Bangkok"

    def __init__(
        self,
        jma_weather_repository: IWeatherRepository,
        open_meteo_weather_repository: IWeatherRepository,
        llm_repository: LlmSummaryPort,
    ):
        self._jma_weather_repository = jma_weather_repository
        self._open_meteo_weather_repository = open_meteo_weather_repository
        self._llm_repository = llm_repository

    async def handle(self) -> WeatherOutput:
        osaka_data = self._jma_weather_repository.fetch()
        osaka_resp = await self._llm_repository.request(
            osaka_data.forecast, WeatherSummaryResponse
        )
        hanoi_data = self._open_meteo_weather_repository.fetch(
            latitude=self.HANOI_LATITUDE,
            longitude=self.HANOI_LONGITUDE,
            timezone=self.HANOI_TIMEZONE,
        )

        return WeatherOutput(
            forecasts=[
                CityWeatherOutput(
                    city_name="大阪市",
                    forecast=osaka_resp.summary,
                    min_temp=osaka_data.min_temp,
                    max_temp=osaka_data.max_temp,
                ),
                CityWeatherOutput(
                    city_name="ハノイ市",
                    forecast=hanoi_data.forecast,
                    min_temp=hanoi_data.min_temp,
                    max_temp=hanoi_data.max_temp,
                ),
            ]
        )
