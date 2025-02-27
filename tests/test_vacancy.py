def test_get_none_salary(instance_vacancy_without_salary):
    """Тестируем обработку данных о зарплате, равной None"""
    assert instance_vacancy_without_salary.salary_to == 0
    assert instance_vacancy_without_salary.salary_from == 0


def test_get_salary(instance_vacancy):
    """Тестируем обработку данных о зарплате, не равной нулю"""
    assert instance_vacancy.salary_to == 500000
    assert instance_vacancy.salary_from == 100000


def test_as_dict_with_salary(instance_vacancy):
    """
    Проверяем представление данных о вакансии
    в виде словаря при указанной зарплате
    """
    result = {
        "id": 117539614,
        "name": "Разработчик бэк-энда Python",
        "link": "https://hh.ru/vacancy/117539614",
        "area": "Ташкент",
        "description": "Work closely with mobile...",
        "salary_from": 100000,
        "salary_to": 500000,
    }
    assert instance_vacancy.as_dict() == result


def test_as_dict_without_salary(instance_vacancy_without_salary):
    """Проверяем представление данных о вакансии в виде словаря"""
    result = {
        "id": 117539614,
        "name": "Разработчик бэк-энда Python",
        "link": "https://hh.ru/vacancy/117539614",
        "area": "Ташкент",
        "description": "Work closely with mobile...",
    }
    assert instance_vacancy_without_salary.as_dict() == result


def test_gte_when_salary_higher(instance_vacancy_high_salary, instance_vacancy):
    """Проверяем случай, когда одна зарплата выше другой"""
    assert instance_vacancy_high_salary.salary_from >= instance_vacancy.salary_from


def test_gte_when_salary_is_the_same(instance_vacancy):
    """Проверяем случай, когда одна зарплата равна другой"""
    instance_vacancy_same_salary = instance_vacancy
    assert instance_vacancy_same_salary.salary_from >= instance_vacancy.salary_from


def test_gte_without_salary(instance_vacancy_without_salary, instance_vacancy):
    """Проверяем случай, когда в одной вакансии зарплата не указана"""
    assert instance_vacancy.salary_from >= instance_vacancy_without_salary.salary_from
