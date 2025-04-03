from typing import Any
import psycopg2
from src.api_datas import HHApi
from src.config import config


class CreateTable:
    """Класс для создания таблицы и работы с ней."""

    def create_database(self, database_name, params: dict) -> None:
        """Создание базы данных и таблиц."""

        conn = psycopg2.connect(dbname="postgres", **params)
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
        cur.execute(f"CREATE DATABASE {database_name}")

        conn.close()

        conn = psycopg2.connect(dbname=database_name, **params)

        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE employers (
                   employer_youtube_id INT PRIMARY KEY,
                   employer_name VARCHAR,
                   employer_url TEXT
                );
                """
            )
        with conn.cursor() as cur:
            cur.execute(
                """
                        CREATE TABLE vacancies (
                           id SERIAL PRIMARY KEY,
                           vacancy_youtube_id INT,
                           vacancy_name VARCHAR(255),
                           salary_currency VARCHAR(10),
                           salary_from INT,
                           salary_to INT,
                           employer_youtube_id INT REFERENCES employers(employer_youtube_id),
                           requirement TEXT,
                           responsibility TEXT,
                           vacancy_url TEXT
                       );
        """
            )
        conn.commit()
        cur.close()
        conn.close()

    def save_employers_into_table(self, datas: Any, database_name: str, params: dict) -> None:
        """Сохранение данных о работодателях в соответствующую таблицу."""

        for empl in datas:
            empl_id = empl.get("id")
            empl_name = empl.get("name")
            empl_url = empl.get("alternate_url")
            if empl_id is None:
                empl_id = "Нет данных"
            if empl_name is None:
                empl_name = "Нет данных"
            if empl_url is None:
                empl_url = "Нет данных"
        conn = psycopg2.connect(dbname=database_name, **params)

        with conn.cursor() as cur:

            cur.execute(
                """
            INSERT INTO employers (employer_name, employer_youtube_id, employer_url)
            VALUES (%s, %s, %s)
            RETURNING employer_youtube_id
            """,
                (empl_name, empl_id, empl_url),
            )

        conn.commit()

        cur.close()
        conn.close()

    def save_vacancies_into_table(self, data: Any, database_name: str, params: dict) -> None:
        """Сохранение данных о вакансиях в соответствующую таблицу."""

        for vacancy in data:
            vacancy_youtube_id = vacancy.get("id")
            if vacancy_youtube_id is None:
                vacancy_youtube_id = 0
            else:
                vacancy_youtube_id = vacancy.get("id")
            if vacancy.get("name") is None:
                vacancy_name = "Нет данных"
            else:
                vacancy_name = vacancy.get("name")
            if vacancy.get("salary") is None:
                salary_currency = "Нет данных"
                salary_from = 0
                salary_to = 0
            else:
                if vacancy.get("salary").get("currency") is None:
                    salary_currency = "Нет данных"
                else:
                    salary_currency = vacancy.get("salary").get("currency")
                if vacancy.get("salary").get("from", 0) is None:
                    salary_from = 0
                else:
                    salary_from = vacancy.get("salary").get("from", 0)
                if vacancy.get("salary").get("to", 0) is None:
                    salary_to = 0
                else:
                    salary_to = vacancy.get("salary").get("to", 0)
            if vacancy.get("employer").get("id") is None:
                employer_youtube_id = 0
            else:
                employer_youtube_id = vacancy.get("employer").get("id")
            if vacancy.get("snippet").get("requirement") is None:
                requirement = "Нет данных"
            else:
                requirement = vacancy.get("snippet").get("requirement")
            if vacancy.get("snippet").get("responsibility") is None:
                responsibility = "Нет данных"
            else:
                responsibility = vacancy.get("snippet").get("responsibility")
            if vacancy.get("alternate_url") is None:
                vacancy_url = "Нет данных"
            else:
                vacancy_url = vacancy.get("alternate_url")

        conn = psycopg2.connect(dbname=database_name, **params)

        with conn.cursor() as cur:

            cur.execute(
                """
            INSERT INTO vacancies (vacancy_youtube_id, vacancy_name, salary_currency, salary_from,
            salary_to, employer_youtube_id, requirement, responsibility, vacancy_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING vacancy_youtube_id
            """,
                (
                    vacancy_youtube_id,
                    vacancy_name,
                    salary_currency,
                    salary_from,
                    salary_to,
                    employer_youtube_id,
                    requirement,
                    responsibility,
                    vacancy_url,
                ),
            )

        conn.commit()

        cur.close()
        conn.close()


if __name__ == "__main__":
    params = config()
    employers_ids = [1749518, 78638, 816969, 46387, 41144, 903111, 9641588, 1440683, 4770322, 1373]
    for employer_id in employers_ids:
        api = HHApi()
        emp = api.get_employer_api(employer_id)
        vac = api.get_vacancies_api(employer_id)
        a = CreateTable()
        new_database = a.create_database("kursov3hh", params)
        base_with_employers = a.save_employers_into_table(emp, "kursov3hh", params)
        base_with_vacancies = a.save_vacancies_into_table(vac, "kursov3hh", params)
