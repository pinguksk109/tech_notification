import asyncio
import json
import logging
from application.usecase.daily_notification_message_builder import (
    DailyNotificationMessageBuilder,
)
from application.usecase.daily_notification_orchestrator import (
    DailyNotificationOrchestrator,
)
from application.usecase.line_usecase import LineUsecase
from application.usecase.recommend_article_usecase import (
    RecommendArticleUsecase,
)
from application.usecase.weather_usecase import WeatherUsecase
from infrastructure.repository.line_notification_repository import (
    LineNotificationRepository,
)
from infrastructure.repository.gemini_summary_repository import (
    GeminiSummaryRepository,
)
from infrastructure.repository.weather_repository import WeatherRepository
from infrastructure.repository.open_meteo_weather_repository import (
    OpenMeteoWeatherRepository,
)
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


def _build_daily_notification_orchestrator() -> DailyNotificationOrchestrator:
    return DailyNotificationOrchestrator(
        weather_usecase=WeatherUsecase(
            jma_weather_repository=WeatherRepository(),
            open_meteo_weather_repository=OpenMeteoWeatherRepository(),
            llm_repository=GeminiSummaryRepository(),
        ),
        qiita_usecase=RecommendArticleUsecase(QiitaArticleRepository()),
        zenn_usecase=RecommendArticleUsecase(ZennArticleRepository()),
        line_usecase=LineUsecase(LineNotificationRepository()),
        message_builder=DailyNotificationMessageBuilder(),
    )


def lambda_handler(event, context):
    try:
        daily_notification_orchestrator = (
            _build_daily_notification_orchestrator()
        )
        asyncio.run(daily_notification_orchestrator.handle())
        return {"status_code": 200, "body": "Success"}
    except Exception as e:
        logger.exception(str(e))
        return {
            "status_code": 500,
            "body": json.dumps({"message": "Failed"}),
        }
