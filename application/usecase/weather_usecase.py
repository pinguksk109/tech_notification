from pydantic import BaseModel
from application.port.weather_port import IWeatherRepository
from application.port.llm_summary_port import LlmSummaryPort
from application.base import IOutput, IUsecase


class WeatherSummaryResponse(BaseModel):
    summary: str


class WeatherOutput(IOutput, BaseModel):
    forecast: str
    min_temp: int
    max_temp: int


class WeatherUsecase(IUsecase[WeatherOutput]):

    def __init__(
        self,
        weather_repository: IWeatherRepository,
        llm_repository: LlmSummaryPort,
    ):
        self._weather_repository = weather_repository
        self._llm_repository = llm_repository

    async def handle(self) -> WeatherOutput:
        data = self._weather_repository.fetch()
        resp = await self._llm_repository.request(
            data.forecast, WeatherSummaryResponse
        )
        return WeatherOutput(
            forecast=resp.summary,
            min_temp=data.min_temp,
            max_temp=data.max_temp,
        )
