from src.api_datas import HHApi
from src.config import config
from src.dbmanager import DBManager
from src.utils import CreateTable

employers_ids = [1749518, 78638, 816969, 46387, 41144, 903111, 9641588, 1440683, 4770322, 1373]


def user_interaction():
    """Итоговая функция для взаимодействия с пользователем."""
    params = config()
    employers_ids = [1749518, 78638, 816969, 46387, 41144, 903111, 9641588, 1440683, 4770322, 1373]
    print(
        "Добрый день. Это программа по поиску вакансий с hh.ru. Данные сохраняются в таблицы postgress. "
        "Перед началом работы проверьте данные для создания базы данных и таблиц в файле."
    )
    print("Информация о вакансиях будет выгружена по определённым работодателям.")
    first = HHApi()
    if_employers = str(input("Для начала, хотите увидеть информацию по работадателям? да/нет  ______").lower())
    if if_employers == "да":
        for employer_id in employers_ids:
            all_employers = first.get_employer_api(employer_id)
            for employer in all_employers:
                print(
                    f"employer_id: {employer.get('id')}, employer_name: {employer.get('name')}, "
                    f"employer_url: {employer.get('alternate_url')}"
                )
        print(
            "При желаниии можете осуществить поиск по другим работодателям. "
            "Для этого введите номера id организаций через запятую."
        )
        others = str(input("Желаете осуществить поиск по другим работодателям? да/нет ___").lower())
        if others == "да":
            other_employers = input("Введите номера id организаций из hh.ru через запятую.")
            employers_ids = other_employers.split(", ")
            for employer_id in employers_ids:
                all_employers = first.get_employer_api(employer_id)
                for empl in all_employers:
                    print(
                        f"employer_id: {empl.get('id')}, employer_name: {empl.get('name')}, "
                        f"employer_url: {empl.get('alternate_url')}"
                    )

    print("Переходим к вакансиям.")
    all_vacancies = first.get_vacancies_api(employer_id)
    for vacancy in all_vacancies:
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
        print(
            f"vacancy_youtube_id: {vacancy_youtube_id}, vacancy_name: {vacancy_name}, "
            f"salary_currency: {salary_currency}, salary_from: {salary_from}, salary_to: {salary_to}, "
            f"employer_youtube_id: {employer_youtube_id}, requirement: {requirement}, "
            f"responsibility: {responsibility}, vacancy_url: {vacancy_url}"
        )

    print("Сохраняем полученную информацию в таблицы.")
    database_name = str(input("Введите название Базы данных для сохранения в неё таблиц._____"))
    second = CreateTable()
    second.create_database(database_name, params)
    second.save_employers_into_table(all_employers, database_name, params)
    second.save_vacancies_into_table(all_vacancies, database_name, params)
    print("Данные сохранены в таблицы.")

    print("Поработаем с вакансиями.")
    for_work = DBManager(database_name)
    answer_first = str(input("Вывести список всех компаний и количество вакансий у каждой компании? да/нет  ").lower())
    if answer_first == "да":
        companies_and_vacancies_count = for_work.get_companies_and_vacancies_count()
        for comp_result in companies_and_vacancies_count:
            print(f"Работодатель: {comp_result[0]}, Количество вакансий: {comp_result[1]}")
    answer_second = str(input("Вывести все вакансии с указанием компании, зарплаты и ссылки?  да/нет     ").lower())
    if answer_second == "да":
        all_vacancies = for_work.get_all_vacancies()
        for comp_result in all_vacancies:
            print(
                f"Работодатель: {comp_result[0]}, Вакансия: {comp_result[1]}, Зарплата_от: {comp_result[2]},"
                f"Зарплата_до: {comp_result[3]}, url-адрес: {comp_result[4]}"
            )
    answer_third = str(input("Вывести среднюю зарплату по вакансиям?  да/нет     ").lower())
    if answer_third == "да":
        avg_salary = for_work.get_avg_salary()
        for av_salary in avg_salary:
            print(f"Средняя зарплата: {av_salary[0]}")
    answer_forth = str(input("Вывести все вакансии, у которых зарплата выше средней?  да/нет     ").lower())
    if answer_forth == "да":
        vacancies_with_higher_salary = for_work.get_vacancies_with_higher_salary()
        for comp_result in vacancies_with_higher_salary:
            print(
                f"Вакансия: {comp_result[0]}, Зарплата_от: {comp_result[1]},"
                f"Зарплата_до: {comp_result[2]}, url-адрес: {comp_result[3]}"
            )
    answer_fifth = str(input("Вывести вакансии, в названии которые содержат конкретные слова? да/нет   ").lower())
    if answer_fifth == "да":
        search_word = str(input("Введите слова для поиска через пробел...     "))
        vacancies_with_keyword = for_work.get_vacancies_with_keyword(search_word)
        for comp_result in vacancies_with_keyword:
            print(
                f"Работодатель: {comp_result[0]}, Вакансия: {comp_result[1]}, Зарплата_от: {comp_result[2]},"
                f"Зарплата_до: {comp_result[3]}, url-адрес: {comp_result[4]}"
            )
    print("Программа завершается.")


if __name__ == "__main__":
    user_interaction()
