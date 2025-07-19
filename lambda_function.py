import json
from application.usecase.line_usecase import LineUsecase, LineSendInput
from application.usecase.train_info_usecase import TrainInfoUsecase
from application.usecase.weather_usecase import WeatherUsecase
from application.usecase.recommend_article_usecase import (
    RecommendArticleUsecase,
)
from infrastructure.repository.line_repository import LineRepository
from infrastructure.repository.scraper_repository import ScraperRepository
from infrastructure.repository.weather_repository import WeatherRepository
from infrastructure.repository.qiita_article_repository import (
    QiitaArticleRepository,
)
from infrastructure.repository.zenn_article_repository import (
    ZennArticleRepository,
)


def lambda_handler(event, context):

    try:

        weather_repository = WeatherRepository()
        weather_usecase = WeatherUsecase(weather_repository)
        # 大阪市の天気情報を取得
        weather_output = weather_usecase.handle()

        scraper_repository = ScraperRepository()
        train_info_usecase = TrainInfoUsecase(scraper_repository)
        # 大阪メトロの情報を取得
        abnormal_train_output = train_info_usecase.handle()

        usecase_qiita = RecommendArticleUsecase(QiitaArticleRepository())
        output_qiita = usecase_qiita.handle()
        usecase_zenn = RecommendArticleUsecase(ZennArticleRepository())
        output_zenn = usecase_zenn.handle()

        line_repository = LineRepository()
        line_usecase = LineUsecase(line_repository)
        line_usecase.handle(
            LineSendInput(
                qiita_items=output_qiita.items,
                zenn_items=output_zenn.items,
                abnormal_train=abnormal_train_output.abnormal_train,
                weather_forecast=weather_output.forecast,
            )
        )

        return {"status_code": 200, "body": "Success"}

    except Exception as e:
        return {
            "status_code": 500,
            "body": json.dumps({"message": "Failed", "error": str(e)}),
        }
