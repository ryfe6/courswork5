from src.classes import DBManager
from src.utils import get_list_company, get_list_vacancy, refactoring_vacancy, script_work_bd

count_company = {
    "сбербанк": "3529",
    "ozon": "2180",
    "wildberries": "5805898",
    "газпром нефть": "39305",
    "роснефть": "6596",
    "gusi_group": "3786084",
    "skyeng": "1122462",
    "яндекс": "1740",
    "2gis": "64174",
    "1c": "882",
}
if __name__ == "__main__":
    print(
        "Приветствую тебя пользователь!\n"
        "Приложение предоставляет актуальные вакансии 10 популярных компаний мира\n"
        "Хотите увидеть список компаний с которыми работает приложение?"
    )
    user_input = input("Введите y/n\n")
    if user_input == "y":
        for key in count_company.keys():
            print(key)
    company_data = get_list_company(count_company)
    vacancy_data = get_list_vacancy(count_company)
    ref_vacancy_data = refactoring_vacancy(company_data, vacancy_data)
    dbm = DBManager()
    dbm.script_create_and_filling_table(company_data, ref_vacancy_data)
    print("Все данные получены и сохранены в базе данных")
    while True:
        print(
            "Список взаимодействия с БД\n"
            "Чтобы завершить работу приложения, ничего не надо вводить\n"
            "1 - Получить список всех вакансий\n"
            "2 - Получить список компаний с подсчитанным количеством актуальных вакансий\n"
            "3 - Получить список всех актуальных вакансий с указанием названия "
            "компании, вакансий, зарплаты и ссылки на вакансию\n"
            "4 - Получить среднюю зарплату по вакансиям\n"
            "5 - Получить все вакансии у которых зп выше среднего\n"
            "6 - Передать слова которые должны содержаться в имени вакансии\n"
        )
        script_work_bd(input("Введите число - "))
