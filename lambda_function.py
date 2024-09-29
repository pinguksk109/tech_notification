import json
from typing import List
from application.usecase.tech_recommend_usecase import TechRecommendUsecase
from application.usecase.line_usecase import LineUsecase, LineSendInput
from application.usecase.train_info_usecase import TrainInfoUsecase, TrainInfoOutput
from infrastructure.repository.qiita_api_repository import QiitaApiRepository
from infrastructure.repository.zenn_repository import ZennApiRepository
from infrastructure.repository.line_repository import LineRepository
from infrastructure.repository.scraper_repository import ScraperRepository


def lambda_handler(event, context):

    try:
        
        scraper_repository = ScraperRepository()
        train_info_usecase = TrainInfoUsecase(scraper_repository)
        # 大阪メトロの情報を取得
        abnormal_train_output = train_info_usecase.handle()           

        qiita_api_repository = QiitaApiRepository()
        zenn_api_repository = ZennApiRepository()
        tech_recommend_usecase = TechRecommendUsecase(
            qiita_api_repository, zenn_api_repository)
        recommend_qiita_output = tech_recommend_usecase.qiita_handle()
        recommend_zenn_output = tech_recommend_usecase.zenn_handle()

        line_repository = LineRepository()
        line_usecase = LineUsecase(line_repository)
        line_usecase.handle(
            LineSendInput(
                qiita_items=recommend_qiita_output.items,
                zenn_items=recommend_zenn_output.items,
                abnormal_train=abnormal_train_output.abnormal_train))

        return {
            "status_code": 200,
            "body": "Success"
        }

    except Exception as e:
        return {
            "status_code": 500,
            "body": json.dumps({
                "message": "Failed",
                "error": str(e)
            })
        }
