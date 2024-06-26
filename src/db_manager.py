import psycopg2
from hh_api import get_employer, get_vacancies


class DBManager:
    """
    Подключается к БД PostgreSQL
    """

    db_connect = None

    def __init__(self):
        self.connection = None
        self.db_create()
        self.connect()

    def db_create(self):
        db_connect = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="dmaster8"
        )

        db_connect.autocommit = True
        cursor_db = db_connect.cursor()

        cursor_db.execute("CREATE DATABASE coursework")

        db_connect.close()

    def connect(self):
        if not self.connection:
            try:
                self.connection = psycopg2.connect(
                    host="localhost",
                    database="coursework",
                    user="postgres",
                    password="dmaster8"
                )
                DBManager.db_connect = self.connection
            except psycopg2.Error as e:
                print("Ошибка подключения к базе данных: ", e)
                raise

    def db_tables(self):
        """
        Создание базы данных и таблиц в ней
        """

        try:

            DBManager.db_connect.cursor().execute(
                """CREATE TABLE employers (
                employer_id INTEGER PRIMARY KEY,
                name varchar(255),
                open_vacancies INTEGER)"""
            )

            DBManager.db_connect.cursor().execute(
                """CREATE TABLE vacancies (
                vacancy_id SERIAL PRIMARY KEY,
                vacancies_name varchar(255),
                payment INTEGER,
                vacancies_url TEXT,
                employer_id INTEGER REFERENCES employers(employer_id))"""
            )

            DBManager.db_connect.commit()
        except psycopg2.Error as e:
            print("Ошибка создания базы данных и таблиц: ", e)
            raise

    def filling_in_tables(self, employers_list):
        """
        Заполняет таблицы баз данных
        """

        cursor_db = DBManager.db_connect.cursor()

        try:
            cursor_db.execute(
                'TRUNCATE TABLE employers, vacancies RESTART IDENTITY;'
            )

            for employer in employers_list:
                employer_list = get_employer(employer)
                cursor_db.execute(
                    'INSERT INTO employers (employer_id, name, open_vacancies) '
                    'VALUES (%s, %s, %s) RETURNING employer_id',
                    (employer_list['employer_id'],
                     employer_list['name'],
                     employer_list['open_vacancies'])
                )

            for employer in employers_list:
                vacancy_list = get_vacancies(employer)
                for vacancy in vacancy_list:
                    cursor_db.execute(
                        'INSERT INTO vacancies (vacancy_id, vacancies_name, '
                        'payment, vacancies_url, employer_id) '
                        'VALUES (%s, %s, %s, %s, %s)',
                        (vacancy['id'], vacancy['name'], vacancy['payment'], vacancy['url'], vacancy['employer_id']))

            DBManager.db_connect.commit()

        finally:
            cursor_db.close()

    def get_companies_and_vacancies_count(self):
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        """
        with DBManager.db_connect.cursor() as cur:
            cur.execute(
                "SELECT name, COUNT(vacancies_name) AS count_vacancies  "
                "FROM employers "
                "JOIN vacancies USING (employer_id) "
                "GROUP BY employers.name"
            )
            set_db = cur.fetchall()
        return set_db

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
        """
        with DBManager.db_connect.cursor() as cur:
            cur.execute(
                "SELECT employers.name, vacancies.vacancies_name, "
                "vacancies_url "
                "FROM employers "
                "JOIN vacancies USING (employer_id)"
            )
            set_db = cur.fetchall()
        return set_db

    def get_avg_salary(self):
        """
        Получает среднюю зарплату по вакансиям.
        """
        with DBManager.db_connect.cursor() as cur:
            cur.execute(
                "SELECT AVG(payment) as avg_payment FROM vacancies "
            )
            set_db = cur.fetchall()
        return set_db

    def get_vacancies_with_higher_salary(self):
        """
        Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        with DBManager.db_connect.cursor() as cur:
            cur.execute(
                "SELECT  *  FROM vacancies "
                "WHERE payment > (SELECT AVG(payment) FROM vacancies) "
            )
            set_db = cur.fetchall()
        return set_db

    def get_vacancies_with_keyword(self, word):
        """
        Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.
        """
        with DBManager.db_connect.cursor() as cur:
            cur.execute(
                "SELECT  *  FROM vacancies "
                f"WHERE lower(vacancies_name) LIKE lower('%{word}%') "
                f"OR lower(vacancies_name) LIKE lower('%{word}') "
                f"OR lower(vacancies_name) LIKE lower('{word}%');"
            )
            set_db = cur.fetchall()
        return set_db

    def close(self):
        DBManager.db_connect.close()
