import os
import json
import requests
from http import HTTPStatus
from application.port.notification_port import INotificationPort
from dotenv import load_dotenv

load_dotenv()


class LineNotificationRepository(INotificationPort):

    def __init__(self):
        self.to = os.getenv("LINE_USER_ID")
        self.bearer_token = os.getenv("LINE_BEARER_TOKEN")

        if not self.to or not self.bearer_token:
            raise ValueError(
                "LINE_USER_ID または LINE_BEARER_TOKEN が .env から読み込めませんでした"
            )

    def send(self, message: str) -> None:
        payload = {
            "to": self.to,
            "messages": [{"type": "text", "text": message}],
        }
        headers = {
            "content-type": "application/json",
            "Authorization": self.bearer_token,
        }
        try:
            resp = requests.post(
                "https://api.line.me/v2/bot/message/push",
                headers=headers,
                data=json.dumps(payload),
            )
        except Exception as e:
            raise Exception(
                f"Lineへのメッセージ送信リクエストに失敗しました {e}"
            )
        if resp.status_code != HTTPStatus.OK:
            raise Exception(
                f"Line APIから200以外が返却されました。ステータスコード: {
                    resp.status_code} レスポンス内容: {
                    resp.text} メッセージリクエスト内容: {message}"
            )
