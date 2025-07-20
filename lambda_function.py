import asyncio
import json
import logging
from application.usecase.line_usecase import LineUsecase, LineSendInput
from application.usecase.train_info_usecase import TrainInfoUsecase
from application.usecase.weather_usecase import WeatherUsecase
from application.usecase.recommend_article_usecase import (
    RecommendArticleUsecase,
)
from infrastructure.repository.gemini_summary_repository import (
    GeminiSummaryRepository,
)
from infrastructure.repository.line_notification_repository import (
    LineNotificationRepository,
)
from infrastructure.repository.osaka_metro_repository import (
    OsakaMetroRepository,
)
from infrastructure.repository.weather_repository import WeatherRepository
from infrastructure.repository.qiita_article_repository import (
    QiitaArticleRepository,
)
from infrastructure.repository.zenn_article_repository import (
    ZennArticleRepository,
)

# logger setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
)
logger.addHandler(handler)


async def _gather_all_info():
    weather_out = await WeatherUsecase(
        weather_repository=WeatherRepository(),
        llm_repository=GeminiSummaryRepository(),
    ).handle()
    train_out = TrainInfoUsecase(OsakaMetroRepository()).handle()
    qiita_out = RecommendArticleUsecase(QiitaArticleRepository()).handle()
    zenn_out = RecommendArticleUsecase(ZennArticleRepository()).handle()

    return {
        "weather_forecast": weather_out.forecast,
        "min_temp": weather_out.min_temp,
        "max_temp": weather_out.max_temp,
        "abnormal_train": train_out.abnormal_train,
        "qiita_items": qiita_out.items,
        "zenn_items": zenn_out.items,
    }


def lambda_handler(event, context):
    try:
        info = asyncio.run(_gather_all_info())
        line_uc = LineUsecase(LineNotificationRepository())
        line_uc.handle(LineSendInput(**info))
        return {"status_code": 200, "body": "Success"}
    except Exception as e:
        logger.exception(str(e))
        return {
            "status_code": 500,
            "body": json.dumps({"message": "Failed"}),
        }
