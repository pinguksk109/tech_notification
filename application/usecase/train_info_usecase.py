from typing import List
from pydantic import BaseModel
from infrastructure.repository.osaka_metro_repository import (
    OsakaMetroRepository,
)
from application.base import IOutput
from application.port.train_info_port import ITrainInfoPort


class TrainInfoOutput(IOutput, BaseModel):
    abnormal_train: List[str]


class TrainInfoUsecase:
    def __init__(self, train_info_repository: ITrainInfoPort):
        self.train_info_repository = train_info_repository

    def handle(self) -> TrainInfoOutput:
        abnormal = self.train_info_repository.fetch_status()
        return TrainInfoOutput(abnormal_train=abnormal)
