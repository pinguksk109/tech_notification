from abc import ABC, abstractmethod
from application.domain.weather import Weather


class IWeatherRepository(ABC):
    @abstractmethod
    def fetch(
        self,
        *,
        latitude: float | None = None,
        longitude: float | None = None,
        timezone: str | None = None,
    ) -> Weather:
        pass
