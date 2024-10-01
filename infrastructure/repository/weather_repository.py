import requests
from http import HTTPStatus


class WeatherRepository:
    def __init__(self):
        pass

    def fetch(self, area_code: int):
        url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{area_code}.json"
        try:
            response = requests.get(url)
        except Exception as e:
            raise Exception(f"気象庁APIから天気取得のリクエストに失敗しました エラー内容: {e}") 
        if (response.status_code == HTTPStatus):
            raise Exception(
                f"気象庁APIから200以外が返却されました。ステータスコード: {
                    response.status_code} レスポンス内容: {
                    response.text}")
        return response.json()