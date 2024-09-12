import json
import requests
import os

def lambda_handler(event, context):

    to = os.environ['LINE_USER_ID']
    bearer_token = os.environ['LINE_BEARER_TOKEN']

    message = [
        {'type':'text','text': 'Hello World'}
    ]
    payload = {'to': to, 'messages': message}
    headers = {'content-type': 'application/json', 'Authorization': bearer_token}
    r = requests.post("https://api.line.me/v2/bot/message/push", headers=headers, data=json.dumps(payload))
    print("LINEレスポンス:" + r.text)
    return "送信完了"

# def main():
#     event = {"key1": "こんにちは、世界！"}
#     context = {} 
#     result = handler(event, context)

# if __name__ == "__main__":
#     main()