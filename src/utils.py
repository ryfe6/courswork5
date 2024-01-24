import time
from typing import Any

import requests

from src.classes import DBManager


def get_list_vacancy(dict_id: dict) -> list[dict[str, int | Any]] | None:
    """
    Функция делает запрос на сайт hh.ru, получает данные о вакансиях, нужные данные складывает в список.
    :param dict_id: Словарь в котором лежат название компаний и их id.
    :return: Преобразованный список вакансий.
    """
    vacancy_count = []
    id_count = 0
    print("Начинаем загрузку данных...")
    for value in dict_id.values():
        headers = {"User-Agent": "Your User Agent"}
        req = requests.get(url=f"https://api.hh.ru/vacancies?employer_id={value}", headers=headers)
        data = req.json()
        req.close()
        time.sleep(0.25)
        vacancies = data["items"]
        for data_vacancy in vacancies:
            id_count += 1
            try:
                vacancy_dict = {
                    "id": id_count,
                    "name": data_vacancy["name"],
                    "external_id": data_vacancy["employer"]["id"],
                    "description": data_vacancy["snippet"]["responsibility"],
                    "salary_to": data_vacancy["salary"]["to"],
                    "salary_from": data_vacancy["salary"]["from"],
                    "city": data_vacancy["area"]["name"],
                    "url": data_vacancy["url"],
                }
                if vacancy_dict["salary_to"] is None:
                    vacancy_dict["salary_to"] = 0
                if vacancy_dict["salary_from"] is None:
                    vacancy_dict["salary_from"] = 0
                vacancy_count.append(vacancy_dict)
            except TypeError:
                id_count -= 1
                continue
    if len(vacancy_count) > 0:
        return vacancy_count
    else:
        print("Не удалось получить данные \n" "проверьте соединение с интернетом ил повторите попытку позже")
        return None


def get_list_company(dict_id: dict) -> list[dict[str, int | Any]] | None:
    """
    Функция делает запрос на сайт hh.ru, получает данные о компаниях, данные складывает в список.
    :param dict_id: Словарь в котором лежат название компаний и их id.
    :return: Преобразованный список с данными о компаниях.
    """
    count_company = []
    id_count = 1
    print("Начинаем загрузку данных...")
    for value in dict_id.values():
        headers = {"User-Agent": "Your User Agent"}
        req = requests.get(url=f"https://api.hh.ru/employers/{value}", headers=headers)
        data = req.json()
        req.close()
        time.sleep(0.25)
        company_dict = {
            "id": id_count,
            "name": data["name"],
            "city": data["area"]["name"],
            "external_id": data["id"],
            "description": data["description"].replace("<p>", "").replace("</p>", ""),
            "site_url": data["site_url"],
        }
        count_company.append(company_dict)
        id_count += 1

    if len(count_company) > 0:
        return count_company
    else:
        print("Не удалось получить данные \n" "проверьте соединение с интернетом ил повторите попытку позже")
        return None


def refactoring_vacancy(company_data: list, vacancy_data: list) -> list:
    """
    Функция добавляет ещё один элемент в словарь вакансий, тем самым связывая две таблицы.
    :param company_data: Список вакансий и информация о вакансиях.
    :param vacancy_data: Список компаний и информация оо компаниях.
    :return: Преобразованный список вакансий.
    """
    vacancies = []
    for company in company_data:
        for vac in vacancy_data:
            if company["external_id"] == vac["external_id"]:
                vac["employer_id"] = company["id"]
                vacancies.append(vac)
    return vacancies


def script_work_bd(input_num: str) -> Any:
    """
    Функция для работы с классом, который работает с базой данных.
    :param input_num: Номер сценария, который ввел пользователь.
    :return: Информация, которую запросил пользователь.
    """
    dbm = DBManager()
    if input_num == "1":
        for data in dbm.get_all_vacancy():
            print(data)
    elif input_num == "2":
        for data in dbm.get_companies_and_vacancies_count():
            print(data)
    elif input_num == "3":
        for data in dbm.get_all_vacancies():
            print(data)
    elif input_num == "4":
        for data in dbm.get_avg_salary():
            print(data[0])
    elif input_num == "5":
        for data in dbm.get_vacancies_with_higher_salary():
            print(data)
    elif input_num == "6":
        for data in dbm.get_vacancies_with_keyword(input("Введите слово/слова - ")):
            print(data)
    else:
        print("Спасибо, что пользуетесь нашим приложением :)")
        quit()
