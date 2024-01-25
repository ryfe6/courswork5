from os import getenv
from typing import Any

import psycopg2
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
load_dotenv()


class DBManager:
    """
    Класс для работы с базой данных.
    """

    def __init__(self) -> None:
        self.conn = psycopg2.connect(
            host=getenv("HOST"),
            database=getenv("DATABASE"),
            user=getenv("USER"),
            password=getenv("PASSWORD"),
            port=getenv("PORT"),
        )

    def script_create_and_filling_table(self, company_data: list, ref_vacancy_data: list) -> None:
        """
        Метод для создания таблиц и заполнения таблиц данными
        :param company_data: Список данных о компаниях
        :param ref_vacancy_data: Список данных о вакансиях.
        :return: None
        """
        try:
            with self.conn:
                self.conn.autocommit = True
                with self.conn.cursor() as cur:
                    cur.execute("DROP TABLE IF EXISTS vacancy;" "DROP TABLE IF EXISTS company;"),


                    cur.execute(
                        """CREATE TABLE company(
                                       id INTEGER PRIMARY KEY NOT NULL,
                                       name varchar(50) NOT NULL,
                                       city varchar(50) NOT NULL,
                                       external_id INTEGER NOT NULL,
                                       description text NOT NULL,
                                       site_url varchar(200) NOT NULL)"""
                    ),

                    cur.execute(
                        """CREATE TABLE vacancy(
                                       id INTEGER,
                                       name varchar(200),
                                       external_id INTEGER,
                                       description text,
                                       salary_to INTEGER,
                                       salary_from INTEGER,
                                       city varchar(100),
                                       url varchar(100),
                                       employer_id INTEGER REFERENCES company(id) NOT NULL)"""
                    ),

                    for company in company_data:
                        cur.execute(
                            "INSERT INTO company VALUES (%s, %s, %s, %s, %s, %s)",
                            (
                                company["id"],
                                company["name"],
                                company["city"],
                                company["external_id"],
                                company["description"],
                                company["site_url"],
                            ),
                        ),

                    for vacancy in ref_vacancy_data:
                        cur.execute(
                            "INSERT INTO vacancy VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                            (
                                vacancy["id"],
                                vacancy["name"],
                                vacancy["external_id"],
                                vacancy["description"],
                                vacancy["salary_to"],
                                vacancy["salary_from"],
                                vacancy["city"],
                                vacancy["url"],
                                vacancy["employer_id"],
                            ),
                        )

        finally:
            cur.close()
            self.conn.close()

    def get_all_vacancy(self) -> Any:
        """
        Метод возвращает весь список вакансий по порядку.
        :return: Список вакансий.
        """
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.execute("""SELECT * FROM vacancy""")
                    get = cur.fetchall()
        finally:
            cur.close()
            self.conn.close()
            return get

    def get_companies_and_vacancies_count(self) -> Any:
        """
        Выводит список всех компаний у которых есть актуальные вакансии
         и количество актуальных вакансий у каждой компании.
        :return Список компаний (имя компании, количество вакансий).
        """
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.execute(
                        """SELECT
                                   company.name,
                                   COUNT(*)
                                   FROM vacancy,
                                   company
                                   WHERE vacancy.employer_id = company.id
                                   GROUP BY company.id, company.name"""
                    )
                    get = cur.fetchall()
        finally:
            cur.close()
            self.conn.close()
            return get

    def get_all_vacancies(self) -> Any:
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию.
        :return Список вакансий (имя компании, имя вакансии, зп, ссылка).
        """
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.execute(
                        """SELECT company.name, vacancy.name, salary_to, salary_from, url 
                           FROM company, vacancy
                           WHERE vacancy.employer_id = company.id
                           GROUP BY company.name, vacancy.name, vacancy.salary_to, vacancy.salary_from, vacancy.url"""
                                )
                    get = cur.fetchall()
        finally:
            cur.close()
            self.conn.close()
            return get

    def get_avg_salary(self) -> Any:
        """
        Метод выводит среднюю зарплату по вакансиям.
        :return Средняя зарплата.
        """
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.execute("""SELECT CAST((SELECT AVG(salary_to) FROM vacancy) AS INTEGER);""")
                    get = cur.fetchall()

        finally:
            cur.close()
            self.conn.close()
            return get

    def get_vacancies_with_higher_salary(self) -> Any:
        """
        Метод выводит список всех вакансий, у которых зарплата выше средней.
        :return Список вакансий с зарплатой выше средней.
        """
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.execute(
                        """SELECT * FROM vacancy
                                   WHERE vacancy.salary_to > (SELECT AVG(salary_to) FROM vacancy);"""
                    )
                    get = cur.fetchall()
        finally:
            cur.close()
            self.conn.close()
            return get

    def get_vacancies_with_keyword(self, user_input: str) -> Any:
        """
        Метод выводит список всех вакансий, в наименовании которых содержатся переданное в метод слово/слова/символы.
        :return Список вакансий с указанным именем.
        """
        try:
            with self.conn:
                with self.conn.cursor() as cur:
                    cur.execute(
                        f"""SELECT * FROM vacancy
                                    WHERE vacancy.name LIKE '%{user_input}%';"""
                    )
                    get = cur.fetchall()
        finally:
            cur.close()
            self.conn.close()
            return get
