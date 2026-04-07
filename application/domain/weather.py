from pydantic import BaseModel


class Weather(BaseModel):
    forecast: str
    min_temp: int
    max_temp: int


class CityWeather(BaseModel):
    city_name: str
    forecast: str
    min_temp: int
    max_temp: int
