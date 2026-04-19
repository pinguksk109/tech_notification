import logging

from application.base import IUsecase
from application.port.notification_port import INotificationPort

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class LineUsecase(IUsecase[None]):
    def __init__(self, line_repository: INotificationPort):
        self.line_repository = line_repository

    def handle(self, messages: list[str]) -> None:
        for message in messages:
            try:
                self.line_repository.send(message)
            except Exception as e:
                logger.error(f"メッセージ送信失敗: {e}")
