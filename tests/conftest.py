from unittest.mock import Mock

import pytest

from src.vacancy import Vacancy


@pytest.fixture
def row_vacancies():
    return {
        "items": [
            {
                "id": "117539614",
                "premium": False,
                "name": "Разработчик бэк-энда Python",
                "department": None,
                "has_test": False,
                "response_letter_required": False,
                "area": {
                    "id": "2759",
                    "name": "Ташкент",
                    "url": "https://api.hh.ru/areas/2759",
                },
                "salary": None,
                "type": {"id": "open", "name": "Открытая"},
                "address": {
                    "city": "Ташкент 69.20983, 41.354485",
                    "street": None,
                    "building": None,
                    "lat": 41.354485,
                    "lng": 69.20983,
                    "description": None,
                    "raw": "Ташкент 69.20983, 41.354485",
                    "metro": None,
                    "metro_stations": [],
                    "id": "14443296",
                },
                "response_url": None,
                "sort_point_distance": None,
                "published_at": "2025-02-20T21:37:38+0300",
                "created_at": "2025-02-20T21:37:38+0300",
                "archived": False,
                "apply_alternate_url": "https://hh.ru/applicant/vacancy_response?vacancyId=117539614",
                "show_logo_in_search": None,
                "insider_interview": None,
                "url": "https://api.hh.ru/vacancies/117539614?host=hh.ru",
                "alternate_url": "https://hh.ru/vacancy/117539614",
                "relations": [],
                "employer": {
                    "id": "6023237",
                    "name": "UzVIP",
                    "url": "https://api.hh.ru/employers/6023237",
                    "alternate_url": "https://hh.ru/employer/6023237",
                    "logo_urls": {
                        "original": "https://img.hhcdn.ru/employer-logo-original/1054210.png",
                        "90": "https://img.hhcdn.ru/employer-logo/5837481.png",
                        "240": "https://img.hhcdn.ru/employer-logo/5837482.png",
                    },
                    "vacancies_url": "https://api.hh.ru/vacancies?employer_id=6023237",
                    "accredited_it_employer": False,
                    "trusted": True,
                },
                "snippet": {
                    "requirement": "Experience with and an understanding of how to successfully lead complex projects, breaking down the work into components and milestones...",
                    "responsibility": "Work closely with mobile and frontend engineers to design APIs that work today and can evolve for future functionality. ",
                },
                "contacts": None,
                "schedule": {"id": "fullDay", "name": "Полный день"},
                "working_days": [],
                "working_time_intervals": [],
                "working_time_modes": [],
                "accept_temporary": False,
                "fly_in_fly_out_duration": [],
                "work_format": [{"id": "ON_SITE", "name": "На\xa0месте работодателя"}],
                "working_hours": [{"id": "HOURS_8", "name": "8\xa0часов"}],
                "work_schedule_by_days": [{"id": "SIX_ON_ONE_OFF", "name": "6/1"}],
                "night_shifts": False,
                "professional_roles": [
                    {"id": "96", "name": "Программист, разработчик"}
                ],
                "accept_incomplete_resumes": False,
                "experience": {"id": "between1And3", "name": "От 1 года до 3 лет"},
                "employment": {"id": "full", "name": "Полная занятость"},
                "employment_form": {"id": "FULL", "name": "Полная"},
                "internship": False,
                "adv_response_url": None,
                "is_adv_vacancy": False,
                "adv_context": None,
            }
        ]
    }


@pytest.fixture
def mock_response(row_vacancies):
    mock = Mock()
    mock.json.return_value = row_vacancies
    mock.status_code = 200
    return mock


@pytest.fixture
def hh_vacancy():
    return [
        Vacancy(
            id=117539614,
            name="Разработчик бэк-энда Python",
            link="https://hh.ru/vacancy/117539614",
            salary=None,
            area="Ташкент",
            description="Work closely with mobile...",
        )
    ]


@pytest.fixture
def instance_vacancy_without_salary():
    return Vacancy(
        id=117539614,
        name="Разработчик бэк-энда Python",
        link="https://hh.ru/vacancy/117539614",
        salary=None,
        area="Ташкент",
        description="Work closely with mobile...",
    )


@pytest.fixture
def instance_vacancy():
    return Vacancy(
        id=117539614,
        name="Разработчик бэк-энда Python",
        link="https://hh.ru/vacancy/117539614",
        salary={
            "from": 100000,
            "to": 500000,
        },
        area="Ташкент",
        description="Work closely with mobile...",
    )


@pytest.fixture
def instance_vacancy_high_salary():
    return Vacancy(
        id=117539614,
        name="Разработчик бэк-энда Python",
        link="https://hh.ru/vacancy/117539614",
        salary={
            "from": 300000,
            "to": 800000,
        },
        area="Ташкент",
        description="Work closely with mobile...",
    )


@pytest.fixture
def mock_vacancies_from_json_file():
    return [
        {
            "id": "117539614",
            "name": "Разработчик бэк-энда Python",
            "link": "https://hh.ru/vacancy/117539614",
            "area": "Ташкент",
            "description": "Work closely with mobile and frontend engineers to design APIs that work today and can evolve for future functionality. ",
        },
        {
            "id": "117627973",
            "name": "Java разработчик (middle)",
            "link": "https://hh.ru/vacancy/117627973",
            "area": "Москва",
            "description": "Участие в развитии новых и текущих проектов, обсуждение требований. Разработка нового функционала. Поддержка, рефакторинг и оптимизация существующих проектов. ",
            "salary_from": 180000,
            "salary_to": 240000,
        },
        {
            "id": "106883136",
            "name": "Frontend-разработчик в Only (Next.js, React)",
            "link": "https://hh.ru/vacancy/106883136",
            "area": "Москва",
            "description": "Внутренний проект Only с командой. Разработка текущих клиентских проектов вместе с командой отдела разработки. Разработка клиентской части веб-приложений. ",
            "salary_from": 140000,
        },
    ]


@pytest.fixture
def new_vacancies_for_add_to_file():
    return [
        Vacancy(
            id=117539614,  # Существующий ID (должен быть проигнорирован)
            name="Обновленная вакансия",
            link="https://hh.ru/new_link",
            salary={"from": 200000, "to": 300000},
            area="Москва",
            description="Новое описание",
        ),
        Vacancy(
            id=12345,  # Новая вакансия
            name="New vacancy",
            link="https://hh.ru/new",
            salary=None,
            area="Санкт-Петербург",
            description="Описание новой вакансии",
        ),
    ]


@pytest.fixture
def mock_vacancies_for_filter():
    return [
        {
            "id": 117539614,
            "name": "Разработчик бэк-энда Python",
            "link": "https://hh.ru/vacancy/117539614",
            "salary": {"from": 100000, "to": 180000},
            "area": "Ташкент",
            "description": "Work closely with mobile and frontend engineers to design APIs that work today and can evolve for future functionality. ",
        },
        {
            "id": 117627973,
            "name": "Java разработчик (middle)",
            "link": "https://hh.ru/vacancy/117627973",
            "salary": {"from": 180000, "to": 240000},
            "area": "Москва",
            "description": "Участие в развитии новых и текущих проектов, обсуждение требований. Разработка нового функционала. Поддержка, рефакторинг и оптимизация существующих проектов. ",
        },
        {
            "id": 106883136,
            "name": "Frontend-разработчик в Only (Next.js, React)",
            "link": "https://hh.ru/vacancy/106883136",
            "salary": {"from": 140000, "to": 200000},
            "area": "Москва",
            "description": "Внутренний проект Only с командой. Разработка текущих клиентских проектов вместе с командой отдела разработки. Разработка клиентской части веб-приложений. ",
        },
    ]


@pytest.fixture
def mock_vacancies_for_filter_without_salary():
    return [
        {
            "id": 117539614,
            "name": "Разработчик бэк-энда Python",
            "link": "https://hh.ru/vacancy/117539614",
            "salary": None,
            "area": "Ташкент",
            "description": "Work closely with mobile and frontend engineers to design APIs that work today and can evolve for future functionality. ",
        },
        {
            "id": 117627973,
            "name": "Java разработчик (middle)",
            "link": "https://hh.ru/vacancy/117627973",
            "salary": None,
            "area": "Москва",
            "description": "Участие в развитии новых и текущих проектов, обсуждение требований. Разработка нового функционала. Поддержка, рефакторинг и оптимизация существующих проектов. ",
        },
        {
            "id": 106883136,
            "name": "Frontend-разработчик в Only (Next.js, React)",
            "link": "https://hh.ru/vacancy/106883136",
            "salary": None,
            "area": "Москва",
            "description": "Внутренний проект Only с командой. Разработка текущих клиентских проектов вместе с командой отдела разработки. Разработка клиентской части веб-приложений. ",
        },
    ]
