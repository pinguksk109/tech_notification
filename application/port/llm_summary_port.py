from abc import ABC, abstractmethod
from typing import Type, TypeVar
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class LlmSummaryPort(ABC):
    @abstractmethod
    async def request(self, input: str, response_type: Type[T]) -> Type[T]: ...
