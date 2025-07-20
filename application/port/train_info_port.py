from abc import ABC, abstractmethod
from typing import List


class ITrainInfoPort(ABC):
    @abstractmethod
    def fetch_status(self) -> List[str]:
        pass
