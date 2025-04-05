from typing import Any
import requests


class HHApi:
    """Класс для получения данных о работодателях и вакансиях  с hh.ru с помощью api"""

    def get_employer_api(self, employer_id: int) -> Any:
        """Метод, получающий данные о работодателях посредством api."""
        companies_datas = []
        try:
            employer_response = requests.get(f"https://api.hh.ru/employers/{employer_id}")
            if employer_response.status_code == 200:
                employer_response.raise_for_status()  # проверка на ошибки
                company_datas = employer_response.json()
                companies_datas.append(company_datas)
        except Exception as e:
            print(f"Ошибка получения данных: {e}. Работодатели не найдены.")
            companies_datas = []
        return companies_datas

    def get_vacancies_api(self, employer_id: int) -> Any:
        """Метод, получающий данные о вакансиях посредством api."""
        vacancies_datas = []
        try:
            vacan_response = requests.get(f"https://api.hh.ru/vacancies?employer_id={employer_id}&per_page=100&page=0")
            if vacan_response.status_code == 200:
                vacan_response.raise_for_status()  # проверка на ошибки
                vacancies_datas = vacan_response.json().get("items", [])
        except Exception as e:
            print(f"Ошибка получения данных: {e}. Вакансии не найдены")
            vacancies_datas = []
        return vacancies_datas


if __name__ == "__main__":
    employers_ids = [1749518, 78638, 816969, 46387, 41144, 903111, 9641588, 1440683, 4770322, 1373]
    for employer_id in employers_ids:
        c = HHApi()
        employer_datas = c.get_employer_api(employer_id)
        vacancies_datas = c.get_vacancies_api(employer_id)
        for v in vacancies_datas:
            print(v.get("employer").get("id"))
