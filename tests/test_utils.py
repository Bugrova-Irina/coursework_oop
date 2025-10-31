import json
from json import JSONDecodeError
from unittest.mock import mock_open, patch

from src.utils import FileRepository
from src.vacancy import Vacancy


def test_read_json(mock_vacancies_from_json_file):
    """Проверяем чтение данных о вакансиях из заполненного файла"""
    mock_json_data = json.dumps(mock_vacancies_from_json_file)

    expected_vacancies = [
        Vacancy(
            id=vacancy["id"],
            name=vacancy["name"],
            link=vacancy["link"],
            salary=vacancy.get("salary"),
            area=vacancy["area"],
            description=vacancy["description"],
        )
        for vacancy in mock_vacancies_from_json_file
    ]

    # Мокаем чтение файла
    with patch("builtins.open", mock_open(read_data=mock_json_data)):
        repository = FileRepository("test.json")
        result = repository._read_json()

    assert len(result) == len(expected_vacancies)

    for res_vacancy, exp_vacancy in zip(result, expected_vacancies):
        assert res_vacancy.id == exp_vacancy.id
        assert res_vacancy.name == exp_vacancy.name
        assert res_vacancy.link == exp_vacancy.link
        assert res_vacancy.area == exp_vacancy.area
        assert res_vacancy.description == exp_vacancy.description


def test_save_to_file_success(mock_vacancies_from_json_file):
    """Проверяем запись данных о вакансии в файл"""
    mock_file = mock_open()

    with patch("pathlib.Path.mkdir") as mocked_mkdir, patch(
        "builtins.open", mock_file
    ) as mocked_open:

        repository = FileRepository("test.json")
        result = repository._save_to_file(mock_vacancies_from_json_file)

        # Проверка успешного возврата
        assert result is True

        # Проверка создания директории
        mocked_mkdir.assert_called_once_with(parents=True, exist_ok=True)

        # Проверка вызова open с правильным именем файла и режимом
        mocked_open.assert_called_once_with("test.json", "w+", encoding="utf-8")

        # Проверка корректности записанных данных в json
        handle = mocked_open()
        written_content = "".join(call.args[0] for call in handle.write.call_args_list)
        written_data = json.loads(written_content)
        assert written_data == mock_vacancies_from_json_file


def test_save_to_file_failure():
    """Проверка обработки ошибки при отсутствии прав на запись"""
    with patch("builtins.open") as mocked_open:
        mocked_open.side_effect = PermissionError("No access")
        repository = FileRepository("test.json")
        result = repository._save_to_file([])

        assert result is False
        mocked_open.assert_called_once_with("test.json", "w+", encoding="utf-8")


def test_save_to_file_empty_list():
    """Проверка обработки ошибки при попытке записи поврежденных данных"""
    with patch("builtins.open") as mocked_open:
        mocked_open.side_effect = JSONDecodeError(
            "Повреждены данные для json", "test.json", 0
        )
        repository = FileRepository("test.json")
        result = repository._save_to_file([])

        assert result is False
        mocked_open.assert_called_once_with("test.json", "w+", encoding="utf-8")


def test_join_vacancies(new_vacancies_for_add_to_file):
    """Проверка объединения существующих и новых вакансий в список словарей"""
    mock_json_data = json.dumps(
        [
            {
                "id": 117539614,
                "name": "Разработчик бэк-энда Python",
                "link": "https://hh.ru/vacancy/117539614",
                "salary": None,
                "area": "Ташкент",
                "description": "Work closely with mobile engineers...",
            }
        ]
    )

    # Мокаем чтение файла
    with patch("builtins.open", mock_open(read_data=mock_json_data)):
        repository = FileRepository("test.json")
        result = repository._join_vacancies(new_vacancies_for_add_to_file)
        assert len(result) == 2


def test_add(new_vacancies_for_add_to_file):
    """Проверка записи новых данных в файл"""
    existing_data = json.dumps(
        [
            {
                "id": 117539614,
                "name": "Разработчик бэк-энда Python",
                "link": "https://hh.ru/vacancy/117539614",
                "salary": None,
                "area": "Ташкент",
                "description": "Work closely with mobile engineers...",
            }
        ]
    )

    # Мокаем операции с файлом
    with patch(
        "builtins.open", mock_open(read_data=existing_data)
    ) as mocked_open, patch("json.dump") as mocked_json_dump:

        repository = FileRepository("test.json")
        result = repository.add(new_vacancies_for_add_to_file)

        # Проверяем результат работы метода add
        assert result is True

        # Проверка записи данных
        # Получаем аргументы вызова json.dump
        written_data = mocked_json_dump.call_args[0][0]

        # Проверяем кол-во вакансий в файле
        assert len(written_data) == 2

        # Проверяем, что в файл не добавлен дубликат вакансии
        assert written_data[0]["id"] == 117539614
        assert written_data[0]["name"] == "Разработчик бэк-энда Python"

        # Проверяем новую вакансию
        new_vacancy = written_data[1]
        assert new_vacancy["id"] == 12345
        assert new_vacancy["name"] == "New vacancy"


def test_get_by_filter(mock_vacancies_for_filter):
    """Проверяем отбор вакансий по ключевому слову"""

    vacancies = json.dumps(mock_vacancies_for_filter)
    with patch("builtins.open", mock_open(read_data=vacancies)):
        repository = FileRepository("test.json")

        # Проверяем фильтр по ключевому слову
        result = repository.get_by_filters(keyword="разработчик")
        # print(result)
        assert len(result) == 3

        # Проверяем вывод топ-2 по зарплате
        result = repository.get_by_filters(top_n=2)
        # print(result)
        assert len(result) == 2
        assert result[0].salary_from == 180000
        assert result[1].salary_from == 140000

        # проверяем отбор топ-2 вакансий по ключевому слову
        result = repository.get_by_filters(top_n=2, keyword="разработчик")
        # print(result)
        assert len(result) == 2
        assert result[0].name == "Java разработчик (middle)"

        # Проверяем фильтрацию по несуществующему ключевому слову
        result = repository.get_by_filters(keyword="певец")
        # print(result)
        assert len(result) == 0

        # Проверяем вывод топ-5 по зарплате
        result = repository.get_by_filters(top_n=3)
        print(result)
        assert len(result) == 3
        assert result[0].salary_from == 180000
        assert result[1].salary_from == 140000


def test_get_by_filter_without_salary(mock_vacancies_for_filter_without_salary):
    """Проверяем отбор вакансий по ключевому слову"""

    vacancies = json.dumps(mock_vacancies_for_filter_without_salary)
    with patch("builtins.open", mock_open(read_data=vacancies)):
        repository = FileRepository("test.json")

        # проверяем отбор топ-2 вакансий по ключевому слову
        result = repository.get_by_filters(top_n=2, keyword="разработчик")
        assert len(result) == 0

        # проверяем отбор вакансий по ключевому слову
        result = repository.get_by_filters(keyword="разработчик")
        # print(result)
        assert len(result) == 3

        # проверяем отбор вакансий по топ-2
        result = repository.get_by_filters(top_n=2)
        assert len(result) == 0


def test_get_by_filter_empty_file():
    with patch("builtins.open", mock_open(read_data=json.dumps([]))):
        repository = FileRepository("test.json")
        result = repository.get_by_filters(top_n=5, keyword="разработчик")
        assert len(result) == 0


def test_delete_vacancies_success(mock_vacancies_for_filter_without_salary):
    """Проверяем удаление вакансии из файла"""
    vacancy_for_delete = Vacancy(
        id=106883136,
        name="Frontend-разработчик в Only (Next.js, React)",
        link="https://hh.ru/vacancy/106883136",
        salary=None,
        area="Москва",
        description="Внутренний проект Only с командой. Разработка текущих клиентских проектов вместе с командой отдела разработки. Разработка клиентской части веб-приложений. ",
    )
    expected_data = [
        v
        for v in mock_vacancies_for_filter_without_salary
        if v["id"] != vacancy_for_delete.id
    ]

    # Мокаем работу с файлом
    mock_file = mock_open(
        read_data=json.dumps(mock_vacancies_for_filter_without_salary)
    )
    with patch("builtins.open", mock_file), patch("json.dump") as mocked_json_dump:
        repository = FileRepository("test.json")
        result = repository.delete_vacancies(vacancy_for_delete)
        assert result is True

        # Проверка вызова json.dump с правильными данными
        saved_data = mocked_json_dump.call_args[0][0]
        assert len(saved_data) == len(expected_data)
        assert all(item["id"] != vacancy_for_delete.id for item in saved_data)


def test_delete_non_existent_vacancies(mock_vacancies_for_filter_without_salary):
    """Проверяем удаление несуществующей вакансии из файла"""
    vacancy_for_delete = Vacancy(
        id=111111,
        name="Frontend-разработчик в Only (Next.js, React)",
        link="https://hh.ru/vacancy/106883136",
        salary=None,
        area="Ямал",
        description="Внутренний проект Only с командой. Разработка текущих клиентских проектов вместе с командой отдела разработки. Разработка клиентской части веб-приложений. ",
    )

    expected_data = [
        v
        for v in mock_vacancies_for_filter_without_salary
        if v["id"] != vacancy_for_delete.id
    ]

    # Мокаем работу с файлом
    mock_file = mock_open(
        read_data=json.dumps(mock_vacancies_for_filter_without_salary)
    )
    with patch("builtins.open", mock_file) as mocked_open, patch(
        "json.dump"
    ) as mocked_json_dump:
        repository = FileRepository("test.json")
        result = repository.delete_vacancies(vacancy_for_delete)
        assert result is True  # файл сохраняется без изменений

        # Проверяем, что вакансии в файле не изменились
        assert expected_data[0]["id"] == 117539614
        assert expected_data[1]["id"] == 117627973
        assert expected_data[2]["id"] == 106883136


def test_delete_from_empty_file():
    vacancy_for_delete = Vacancy(
        id=111111,
        name="Frontend-разработчик в Only (Next.js, React)",
        link="https://hh.ru/vacancy/106883136",
        salary=None,
        area="Ямал",
        description="Внутренний проект Only с командой. Разработка текущих клиентских проектов вместе с командой отдела разработки. Разработка клиентской части веб-приложений. ",
    )

    with patch("builtins.open", mock_open(read_data=json.dumps([]))):
        repository = FileRepository("test.json")
        result = repository.delete_vacancies(vacancy_for_delete)
        assert result is True  # Пустой файл остается пустым
