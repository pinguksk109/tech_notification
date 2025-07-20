from abc import ABC, abstractmethod
from typing import Any, Dict


class IWeatherRepository(ABC):
    @abstractmethod
    def fetch(self, area_code: int):
        pass
