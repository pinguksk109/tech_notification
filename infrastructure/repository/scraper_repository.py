import requests
from bs4 import BeautifulSoup

class ScraperRepository:
    def __init__(self):
        pass

    def fetch_content(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            raise Exception(f"スクレイピング先の情報取得に失敗しました: {e}")
        
    def parse_all_lines_status(self, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')

        abnormal_lines = []

        subway_lines = soup.find_all('dd', class_='headerMenuOperationArea_subway')

        for line in subway_lines:
            line_name_img = line.find('li', class_='subwayArea_LineName').find('img')
            line_name = line_name_img['alt']

            status_icon_img = line.find('li', class_='subwayArea_Status').find('img')
            status_icon_src = status_icon_img['src'] if status_icon_img else ""

            if "icon_operation_normal.svg" not in status_icon_src:
                abnormal_lines.append(line_name)
        
        return abnormal_lines