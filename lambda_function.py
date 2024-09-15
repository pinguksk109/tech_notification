import json
import requests
import os
from typing import List
from domain.item import Item
from application.usecase.tech_recommend_usecase import TechRecommendUsecase
from infrastructure.repository.qiita_api_repository import QiitaApiRepository

def lambda_handler(event, context):

    to = os.environ['LINE_USER_ID']
    bearer_token = os.environ['LINE_BEARER_TOKEN']

    qiita_api_repository = QiitaApiRepository()
    tech_recommend_usecase = TechRecommendUsecase(qiita_api_repository)
    top5_items = tech_recommend_usecase.handle()

    print(create_message(top5_items))
    message = [
        {'type':'text','text': create_message(top5_items)}
    ]
    payload = {'to': to, 'messages': message}
    headers = {'content-type': 'application/json', 'Authorization': bearer_token}
    print(headers)
    r = requests.post("https://api.line.me/v2/bot/message/push", headers=headers, data=json.dumps(payload))
    print("LINEレスポンス:" + r.text)
    return "送信完了"

def create_message(items: List[Item]) -> str:
    formatted_items = []
    for i, item in enumerate(items):
        formatted_items.append(f"{i+1}. {item.title} {item.url}")
    return "今日のQiitaおすすめ記事を送ります。\n\n" + "\n".join(formatted_items)

if __name__ == "__main__":
    event = {}
    context = {} 
    lambda_handler(event, context)