import unittest
from unittest.mock import patch, MagicMock, mock_open

from src.api_connection import HeadHunter
from src.vacancy import Vacancy
from tests.conftest import hh_vacancy


class TestHeadHunter(unittest.TestCase):
    """Тестирование класса HeadHunter"""

    def  setUp(self):
        # Инициализация тестовых данных
        self.mock_response_data = {
            'items': [
                {
                    'id': '117539614',
                    'name': 'Разработчик бэк-энда Python',
                    'alternate_url': 'https://hh.ru/vacancy/117539614',
                    'salary': None,
                    'area': {'name': 'Ташкент'},
                    'snippet': {'responsibility': 'Work closely with mobile...'}
                }
            ]
        }

        # Параметры для инициализации HeadHunter
        self.hh_params = {
            'url': "https://api.hh.ru/vacancies",
            'headers': {'User-Agent': 'HH-User-Agent'},
            'params': {'text': '', 'page': 0, 'per_page': 100},
            'city': 'Moscow',
            'number_of_city': 1,
            'page': 1,
            'keyword': 'Python'
        }


    @patch('requests.get')
    def test_get_row_vacancies_success(self, mock_get):
        """Проверяет получение необработанных данных о вакансиях с сайта hh.ru"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = self.mock_response_data

        mock_get.return_value = mock_response

        hh = HeadHunter(**self.hh_params)

        result = hh.get_row_vacancies()

        mock_get.assert_called_once_with(
            self.hh_params['url'],
            headers=self.hh_params['headers'],
            params=self.hh_params['params'],
        )
        self.assertEqual(result, self.mock_response_data)


    @patch('requests.get')
    def test_get_row_vacancies_failure(self, mock_get):
        """Проверка обработки ошибки при запросе"""
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = Exception("API Error")
        mock_get.return_value = mock_response

        hh = HeadHunter(**self.hh_params)

        with self.assertRaises(Exception) as context:
            hh.get_row_vacancies()

        self.assertIn("API Error", str(context.exception))
        mock_response.raise_for_status.assert_called_once()


def test_get_vacancies_success(mock_response, hh_vacancy):
    """Проверяем возврат объектов класса Vacancy в нужном формате"""
    with patch('requests.get', return_value=mock_response):
        hh = HeadHunter()
        result = hh.get_vacancies()
        assert str(result) == str(hh_vacancy)


def test_get_row_vacancies(mock_response, row_vacancies):
    """Проверяет получение необработанных данных о вакансиях с сайта hh.ru"""
    with patch('requests.get', return_value=mock_response) as mock_get:
        hh = HeadHunter()
        result = hh.get_row_vacancies()
        assert result == row_vacancies
        mock_get.assert_called_once()
