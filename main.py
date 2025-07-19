from infrastructure.repository.zenn_repository import ZennApiRepository
from infrastructure.repository.qiita_api_repository import QiitaApiRepository
from infrastructure.repository.line_repository import LineRepository
from application.usecase.tech_recommend_usecase import TechRecommendUsecase
from infrastructure.repository.scraper_repository import ScraperRepository

def main():
    # zenn_api_repository = ZennApiRepository()
    # qiita_api_repository = QiitaApiRepository()
    # usecase = TechRecommendUsecase(qiita_api_repository, zenn_api_repository)

    # hoge = usecase.zenn_handle()
    # print(hoge)

    url = "https://subway.osakametro.co.jp/guide/subway_information.php"

    scraper = ScraperRepository()

    html_content = scraper.fetch_content(url)

    if html_content:
        hoge = scraper.parse_all_lines_status(html_content)

    print(hoge)

    # if html_content:
    #     # 長堀鶴見緑地線の運行状況を解析して出力
    #     status = scraper.parse_nagahori_status(html_content)
    #     print(status)
    #     if status:
    #         print('OK')
    #     else:
    #         print('NG')
    # else:
    #     print("HTMLコンテンツの取得に失敗しました。")

if __name__ == "__main__":
    main()
