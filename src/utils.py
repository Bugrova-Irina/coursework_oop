import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional

from src.vacancy import Vacancy


class Repository(ABC):
    """Абстрактный класс для работы с файлами"""

    @abstractmethod
    def add(self, data: list[Vacancy]):
        """Запись данных в файл"""
        pass

    @abstractmethod
    def get_by_filters(self, filters: dict[str, Any]):
        """Получение отфильтрованных вакансий"""
        pass

    @abstractmethod
    def delete_vacancies(self, data: Vacancy):
        """Удаление данных о вакансиях из файла"""
        pass


class FileRepository(Repository):
    """Класс для работы с файлами"""
    def __init__(
            self,
            filename: str = 'data.json'
    ):
        self.__filename = filename
        self.vacancies = []

    @property
    def filename(self) -> str:
        return self.__filename

    def _read_json(self) -> list[Vacancy]:
        """Чтение данных из json-файла"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as json_file:
                content = json_file.read()
                if not content:
                    return []  # Если файл пуст, возвращаем пустой список
                vacancies = json.loads(content)

            for vacancy in vacancies:
                self.vacancies.append(
                    Vacancy(
                        id=vacancy['id'],
                        name=vacancy['name'],
                        link=vacancy['link'],
                        salary=vacancy.get('salary'),
                        area=vacancy['area'],
                        description=vacancy['description']
                    )
                )
            return self.vacancies
        except FileNotFoundError:
            print(f"Файл {self.filename} не найден")
            return []

    def _save_to_file(self, vacancies: list[dict[str, Any]]) -> bool:
        """ Запись данных в файл"""
        # os.makedirs(os.path.dirname('../coursework_oop/data/data.json'), exist_ok=True)
        # Создаем директорию, если она не существует
        Path(self.filename).parent.mkdir(parents=True, exist_ok=True)

        with open(self.filename, 'w+', encoding='utf-8') as json_file:
            try:
                json.dump(vacancies, json_file, ensure_ascii=False, indent=4)
                return True
            except (IOError, json.JSONDecodeError) as e:
                print(f"Ошибка при работе с файлом: {e}")
                return False

    def _join_vacancies(self, data: list[Vacancy]) -> list[dict[str, Any]]:
        """
        Объединение существующих и новых вакансий в список словарей
        """
        exists_vacancies = self._read_json()
        exists_vacancies_ids = {
            v.id for v in exists_vacancies
        }
        for item in data:
            if item.id in exists_vacancies_ids:
                continue
            exists_vacancies.append(item)
        self.vacancies = exists_vacancies

        data_for_file = []
        for item in exists_vacancies:
            data_for_file.append(item.as_dict())
        return data_for_file

    def add(self, data: list[Vacancy]):
        """Добавление новых данных в файл"""
        data_for_save = self._join_vacancies(data)
        return self._save_to_file(data_for_save)

    def get_by_filters(
            self,
            top_n: Optional[int] = None,
            keyword: Optional[str] = None
    ) -> list[Vacancy]:
        """Получаем отфильтрованный по ключевому слову в названии вакансии список вакансий"""
        vacancies = self._read_json()

        filtered_vacancies_by_keyword = []
        if keyword:  # если задано ключевое слово
            for vacancy in vacancies:
                # Приводим оба значения к нижнему регистру
                if keyword.lower() in vacancy.name.lower():
                    filtered_vacancies_by_keyword.append(vacancy)
        else:
            filtered_vacancies_by_keyword = vacancies

        if top_n:  # если задано кол-во вакансий для вывода, сортируем по зарплате
            filtered_vacancies_by_keyword = [
                v for v in filtered_vacancies_by_keyword
                if v.salary_from > 0  # Исключаем вакансии без зарплаты
            ]
            filtered_vacancies_by_keyword.sort(key=lambda x: x.salary_from, reverse=True)
            return filtered_vacancies_by_keyword[:top_n]
        return filtered_vacancies_by_keyword

    def delete_vacancies(self, data: Vacancy) -> bool:
        """Удаление данных о вакансии из файла"""
        data_vacancies = self._read_json()
        new_vacancies = []

        for vacancy in data_vacancies:
            if vacancy.id == data.id:
                continue
            new_vacancies.append(vacancy)

        data_for_file = []
        for item in new_vacancies:
            data_for_file.append(item.as_dict())

        return self._save_to_file(data_for_file)
