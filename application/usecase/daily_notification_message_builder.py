from datetime import datetime
from zoneinfo import ZoneInfo

from application.domain.item import Item
from application.domain.weather import CityWeather
from application.usecase.daily_notification_input import DailyNotificationInput


class DailyNotificationMessageBuilder:
    JST = ZoneInfo("Asia/Tokyo")

    def __init__(self, today_date: str | None = None):
        self.today_date = today_date or datetime.now(self.JST).strftime(
            "%Y-%m-%d"
        )

    def build(self, input_data: DailyNotificationInput) -> list[str]:
        return [
            self._weather_message(input_data.weather_forecasts),
            self._media_message(input_data.qiita_items, "Qiita"),
            self._media_message(input_data.zenn_items, "Zenn"),
        ]

    def _media_message(self, items: list[Item], media: str) -> str:
        lines = [f"{i + 1}. {item.title} {item.url}" for i, item in enumerate(items)]
        header = f"{self.today_date} の{media}今日の記事を送ります✍\n"
        return header + "\n".join(lines)

    def _weather_message(self, forecasts: list[CityWeather]) -> str:
        header = [f"{self.today_date} の天気", ""]
        body = [
            line
            for forecast in forecasts
            for line in [
                f"■ {forecast.city_name}",
                forecast.forecast,
                f"🌡 最低気温: {forecast.min_temp}℃ / 最高気温: {forecast.max_temp}℃",
                "",
            ]
        ]
        footer = ["大阪市詳細⇒https://www.jma.go.jp/bosai/forecast/"]
        return "\n".join(header + body + footer)
