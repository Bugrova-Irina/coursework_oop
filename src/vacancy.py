from typing import Any, Optional


class Vacancy:
    """Класс для обработки вакансий"""
    __slots__ = ('id', 'name', 'link', 'area', '_salary', 'description', 'salary_from', 'salary_to')

    def __init__(
            self,
            id: int,
            name: str,
            link: str,
            salary: Optional[dict[str, Any]],
            area: str,
            description: str,
    ):
        self.id = id
        self.name = name
        self.link = link
        self.area = area
        self._salary = salary
        self.description = description
        self.salary_from = 0
        self.salary_to = 0
        self.get_salary()

    def get_salary(self):
        """Отбор вакансий по зарплате"""
        if self._salary:
            self.salary_from = self._salary.get('from') or 0
            self.salary_to = self._salary.get('to') or 0
            self.salary_from = int(self.salary_from) if self.salary_from else 0
            self.salary_to = int(self.salary_to) if self.salary_to else 0

            # self.salary_from = self._salary['from'] if self._salary.get('from') else 0
            # self.salary_to = self._salary['to'] if self._salary.get('to') else 0
        else:
            self.salary_from = 0
            self.salary_to = 0

    def __gte__(self, other):
        """Сравнение зарплат"""
        if self.salary_from >= other.salary_from:
            return self.salary_from

    def __lte__(self, other):
        """Сравнение зарплат"""
        if self.salary_from <= other.salary_from:
            return self.salary_from

    def as_dict(self) -> dict[str, Any]:
        """Представление данных в виде словаря"""
        salary_data = {}
        if self.salary_from > 0:
            salary_data['salary_from'] = self.salary_from
        if self.salary_to > 0:
            salary_data['salary_to'] = self.salary_to

        result = {
            'id': self.id,
            'name': self.name,
            'link': self.link,
            'area': self.area,
            # 'salary': self.get_salary(),
            'description': self.description,
            # 'salary_from': self.salary_from,
            # 'salary_to': self.salary_to,
            **salary_data,
        }

        # if self._salary:
        #     result['salary'] = self._salary

        return result

    def __repr__(self):
        """ Представление для объектов класса Vacancy"""
        return (
            f"Vacancy(id={self.id}, name ='{self.name}', salary_from={self.salary_from}, "
            f"salary_to={self.salary_to}, link='{self.link}')")
