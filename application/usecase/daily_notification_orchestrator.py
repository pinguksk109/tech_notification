from application.usecase.daily_notification_input import DailyNotificationInput
from application.usecase.daily_notification_message_builder import (
    DailyNotificationMessageBuilder,
)
from application.usecase.line_usecase import LineUsecase
from application.usecase.recommend_article_usecase import (
    RecommendArticleUsecase,
)
from application.usecase.train_info_usecase import TrainInfoUsecase
from application.usecase.weather_usecase import WeatherUsecase


class DailyNotificationOrchestrator:
    def __init__(
        self,
        weather_usecase: WeatherUsecase,
        qiita_usecase: RecommendArticleUsecase,
        zenn_usecase: RecommendArticleUsecase,
        line_usecase: LineUsecase,
        message_builder: DailyNotificationMessageBuilder,
        train_usecase: TrainInfoUsecase | None = None,
    ):
        self._weather_usecase = weather_usecase
        self._qiita_usecase = qiita_usecase
        self._zenn_usecase = zenn_usecase
        self._line_usecase = line_usecase
        self._message_builder = message_builder
        self._train_usecase = train_usecase

    async def handle(self) -> None:
        weather_out = await self._weather_usecase.handle()
        qiita_out = self._qiita_usecase.handle()
        zenn_out = self._zenn_usecase.handle()

        abnormal_train: list[str] = []
        if self._train_usecase is not None:
            train_out = self._train_usecase.handle()
            abnormal_train = train_out.abnormal_train

        notification_input = DailyNotificationInput(
            weather_forecasts=weather_out.forecasts,
            qiita_items=qiita_out.items,
            zenn_items=zenn_out.items,
            abnormal_train=abnormal_train,
        )
        messages = self._message_builder.build(notification_input)
        self._line_usecase.handle(messages)
