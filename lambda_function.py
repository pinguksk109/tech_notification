import json
import requests
import os
from typing import List
from domain.item import Item
from application.usecase.tech_recommend_usecase import TechRecommendUsecase
from application.usecase.line_usecase import LineUsecase, LineSendInput
from infrastructure.repository.qiita_api_repository import QiitaApiRepository
from infrastructure.repository.line_repository import LineRepository

def lambda_handler(event, context):

    qiita_api_repository = QiitaApiRepository()
    tech_recommend_usecase = TechRecommendUsecase(qiita_api_repository)
    tech_recommend_output = tech_recommend_usecase.qiita_handle()

    line_repository = LineRepository()
    line_usecase = LineUsecase(line_repository)
    line_usecase.handle(LineSendInput(items=tech_recommend_output.items))