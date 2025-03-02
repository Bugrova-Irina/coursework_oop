from abc import ABC, abstractmethod
from typing import Any, Optional

import requests

from src.vacancy import Vacancy


class API(ABC):
    """Абстрактный класс для работы с API"""

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_vacancies(self) -> list[Vacancy]:
        pass


class HeadHunter(API):
    """Класс для получения данных с сайта по API"""
    # url: str = "https://api.hh.ru/vacancies",
    # headers: Optional[dict[str, str]] = None,
    # params: Optional[dict[str, Any]] = None,
    # city: str = "Moscow",
    # number_of_city: int = 1,
    # page: int = 1,
    # keyword: str = "Python",

    def __init__(self):
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"text": "", "page": 0, "per_page": 100}
        self.__vacancies = []
        # self.page = page
        # self.city = city
        # self.number_of_city = number_of_city
        # self.keyword = keyword
        super().__init__()

    @property
    def url(self) -> str:
        return self.__url

    @property
    def headers(self) -> dict[str, str]:
        return self.__headers

    @property
    def params(self) -> dict[str, Any]:
        return self.__params

    @property
    def vacancies(self) -> list:
        return self.__vacancies


        # super().__init__(
        #     url=url,
        #     headers=headers or {"User-Agent": "HH-User-Agent"},
        #     params=params or {"text": "", "page": 0, "per_page": 100},
        #     city=city,
        #     number_of_city=number_of_city,
        #     page=page,
        #     keyword=keyword,
        # )

    def get_row_vacancies(self) -> dict[str, Any]:
        """Получение списка вакансий с сайта"""
        response = requests.get(self.url, headers=self.headers, params=self.params)
        try:
            response.raise_for_status()
        except Exception as exc:
            print("Error get vacancies from HH", exc)
            raise
        return response.json()

    def get_vacancies(self) -> list[Vacancy]:
        """преобразование данных о вакансиях в нужный формат"""
        data = self.get_row_vacancies()
        return [
            Vacancy(
                id=item["id"],
                name=item["name"],
                link=item["alternate_url"],
                salary=item.get("salary"),
                area=item.get("area", {}).get("name", ""),
                description=item.get("snippet", "").get("responsibility", ""),
            )
            for item in data["items"]
        ]


# hh_vacancies = HeadHunter()
# print(hh_vacancies.get_row_vacancies())
# data_set_vacancy = hh_vacancies.get_vacancies()
# print(data_set_vacancy)
