import requests
from http import HTTPStatus

class ZennApiRepository:
    def __init__(self):
        pass

    def get_items(self, page):
        """
        Zenn APIから最新の記事を取得します
        """
        url = f"https://zenn.dev/api/articles?order=latest&page={page}"

        try:
            response = requests.get(url)
        except Exception as e:
            raise Exception(f"Zenn APIのリクエストに失敗しました エラー内容: {e}")
        if(response.status_code != HTTPStatus.OK):
            raise Exception(f"Qiita APIから200以外が返却されました。ステータスコード: {response.status_code} レスポンス内容: {response.text}")
        return response.json()