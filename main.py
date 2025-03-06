from src.api_connection import HeadHunter
from src.utils import FileRepository
from src.vacancy import Vacancy


def user_interaction() -> None:
    """
    Запрос данных у пользователя, вывод результатов работы программы
    """
    user_keyword = (input("Введите слово для поиска вакансии\n")).lower()
    user_top_n = int(input("Введите количество вакансий, которые нужно вывести\n"))

    # Получение данных с hh.ru
    vacancies_from_hh = HeadHunter(user_keyword)
    formated_vacancies = vacancies_from_hh.get_vacancies()
    # print(formated_vacancies)

    # Сохраняем вакансии в файл
    file_repository = FileRepository("../coursework_oop/data/data.json")
    file_repository.add(formated_vacancies)

    # Фильтруем вакансии
    filtered_vacancies = file_repository.get_by_filters(
        top_n=user_top_n, keyword=user_keyword
    )

    for vacancy in filtered_vacancies:
        print(vacancy)


if __name__ == "__main__":
    user_interaction()
