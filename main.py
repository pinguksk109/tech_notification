from infrastructure.repository.qiita_api_repository import QiitaApiRepository
from application.usecase.tech_recommend_usecase import TechRecommendUsecase

def main():
    repository = QiitaApiRepository()

    usecase = TechRecommendUsecase(repository)

    response = usecase.handle()
    
    print(response)

if __name__ == "__main__":
    main()