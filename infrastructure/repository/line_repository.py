import requests
import os
import json
from http import HTTPStatus

class LineRepository:
    def __init__(self):
        self.to = os.environ['LINE_USER_ID']
        self.bearer_token = os.environ['LINE_BEARER_TOKEN']

    def send_message(self, message) -> None:
        message = [
            {"type": "text", "text": message}
        ]
        payload = {"to": self.to, "messages": message}
        headers = {'content-type': 'application/json', 'Authorization': self.bearer_token}
        try:
            response = requests.post("https://api.line.me/v2/bot/message/push", headers=headers, data=json.dumps(payload))
        except Exception as e:
            raise Exception(f"Lineへのメッセージ送信リクエストに失敗しました {e}")
        if(response.status_code != HTTPStatus.OK):
            raise Exception(f"Line APIから200以外が返却されました。ステータスコード: {response.status_code} レスポンス内容: {response.text}")