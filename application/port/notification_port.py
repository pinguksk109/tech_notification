from abc import ABC, abstractmethod


class INotificationPort(ABC):
    @abstractmethod
    def send(self, message: str) -> None:
        pass
