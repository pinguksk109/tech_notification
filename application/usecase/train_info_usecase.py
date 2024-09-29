from typing import List
from pydantic import BaseModel
from infrastructure.repository.scraper_repository import ScraperRepository
from application.base import IOutput

class TrainInfoOutput(IOutput, BaseModel):
    abnormal_train: List[str]

class TrainInfoUsecase():
    def __init__(self, scraper_repository: ScraperRepository):
        self.scraper_repository = scraper_repository

    def handle(self):
        '''
        大阪メトロしか対応していない
        '''
        target_url = "https://subway.osakametro.co.jp/guide/subway_information.php"
        html_content = self.scraper_repository.fetch_content(target_url)
        abnormal_train_list = self.scraper_repository.parse_all_lines_status(html_content)
        return TrainInfoOutput(abnormal_train=abnormal_train_list)