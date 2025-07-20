from pydantic import BaseModel


class Weather(BaseModel):
    forecast: str
    min_temp: int
    max_temp: int
