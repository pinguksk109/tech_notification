import requests
from bs4 import BeautifulSoup
from typing import List
from application.port.train_info_port import ITrainInfoPort


class OsakaMetroRepository(ITrainInfoPort):
    TARGET_URL = "https://subway.osakametro.co.jp/guide/subway_information.php"

    def fetch_status(self) -> List[str]:
        resp = requests.get(self.TARGET_URL)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        abnormal = []
        for dd in soup.find_all("dd", class_="headerMenuOperationArea_subway"):
            name = dd.find("li", class_="subwayArea_LineName").img["alt"]
            icon = dd.find("li", class_="subwayArea_Status").img.get("src", "")
            if "icon_operation_normal.svg" not in icon:
                abnormal.append(name)
        return abnormal
