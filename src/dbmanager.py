from typing import Any
import psycopg2
from src.config import config


class DBManager:
    """Класс для работы с таблицами."""

    def __init__(self, database_name="postgres"):
        params = config()
        self.database_name = database_name
        self.conn = psycopg2.connect(dbname=database_name, **params)
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self) -> Any:
        """Выводит список всех компаний и количество вакансий у каждой компании."""
        self.cur.execute(
            """
              SELECT employer_name, COUNT(vacancy_name) as vacancies_quantity
              FROM employers JOIN vacancies USING(employer_youtube_id)
              GROUP BY employer_name
              """
        )
        return self.cur.fetchall()

    def get_all_vacancies(self) -> Any:
        """Выводит все вакансии с указанием компании, зарплаты и ссылки."""
        self.cur.execute(
            """
            SELECT employer_name, vacancy_name, salary_from, salary_to, vacancy_url
            FROM vacancies
            JOIN employers USING(employer_youtube_id);
            """
        )
        return self.cur.fetchall()

    def get_avg_salary(self) -> Any:
        """Выводит среднюю зарплату по вакансиям."""
        self.cur.execute(
            """
            SELECT AVG((salary_from + salary_to) / 2) AS average_salary
            FROM vacancies
            """
        )
        return self.cur.fetchall()

    def get_vacancies_with_higher_salary(self) -> Any:
        """Выводит вакансии, у которых зарплата выше средней."""

        self.cur.execute(
            """
        SELECT vacancy_name, salary_from, salary_to, vacancy_url
        FROM vacancies
        WHERE salary_from > ((salary_from + salary_to) / 2) OR salary_to > ((salary_from + salary_to) / 2);
        """
        )
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> Any:
        """Выводит вакансии, в названии которых содержатся конкретные слова."""
        for_query = " OR ".join(["vacancy_name ILIKE %s " for _ in keyword])
        query = f"""
            SELECT employer_name, vacancy_name, salary_from, salary_to, vacancy_url
            FROM vacancies
            JOIN employers USING(employer_youtube_id)
            WHERE {for_query}
            """
        params = [f"%{word}%" for word in keyword]
        self.cur.execute(query, params)
        return self.cur.fetchall()


if __name__ == "__main__":
    first = DBManager()
    companies_and_vacancies_count = first.get_companies_and_vacancies_count()
    all_vacancies = first.get_all_vacancies()
    get_avg_salary = first.get_avg_salary()
    vacancies_with_higher_salary = first.get_vacancies_with_higher_salary()
    vacancies_with_keyword = first.get_vacancies_with_keyword()
