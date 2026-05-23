from pydantic import BaseModel, Field

from application.base import IInput
from application.domain.item import Item
from application.domain.weather import CityWeather


class DailyNotificationInput(IInput, BaseModel):
    qiita_items: list[Item]
    zenn_items: list[Item]
    abnormal_train: list[str] = Field(default_factory=list)
    weather_forecasts: list[CityWeather]
