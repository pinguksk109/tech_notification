import requests
from http import HTTPStatus

class QiitaApiRepository:
    def __init__(self):
        pass

    def get_items(self, page):
        """
        Qiita APIから最新の記事を取得します
        """
        url = f"https://qiita.com/api/v2/items?page={page}&per_page=100"

        # テスト用
        # url = "http://localhost:3000/items"

        try:
            response = requests.get(url)
        except Exception as e:
            raise Exception(f"Qiita APIのリクエストに失敗しました エラー内容: {e}")
        if(response.status_code == HTTPStatus.FORBIDDEN):
            raise Exception(f"Qiita APIから403(レートリミット)が返却されました。レスポンス内容: {response.text}")
        if(response.status_code != HTTPStatus.OK):
            raise Exception(f"Qiita APIから200以外が返却されました。ステータスコード: {response.status_code} レスポンス内容: {response.text}")
        return response.json()