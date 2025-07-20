from abc import ABC, abstractmethod
from application.domain.weather import Weather


class IWeatherRepository(ABC):
    @abstractmethod
    def fetch(self) -> Weather:
        pass
