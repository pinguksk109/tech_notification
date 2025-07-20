from abc import ABC, abstractmethod
from typing import TypeVar, Generic

TOutput = TypeVar("TOutput")


class IInput(ABC):
    pass


class IOutput(ABC):
    pass


class IUsecase(ABC, Generic[TOutput]):
    @abstractmethod
    def handle(self) -> TOutput:
        pass
