import psycopg2
import requests


def get_vacancies(employer_id):
    """
    Получение вакансий
    :param employer_id: id кампании
    :return: список с данными по вакансиям
    """

    params = {
        'area': 1,
        'page': 100,
        'per_page': 10
    }
    vacancies_data = []

    data = requests.get(f"https://api.hh.ru/vacancies?employer_id={employer_id}", params)
    data_vacancies = data.json()

    for vacancy in data_vacancies["items"]:
        vacancies = {
            'id': int(vacancy['id']),
            'name': str(vacancy['name']),
            'payment': vacancy["salary"]["from"] if vacancy["salary"] else None,
            'url': str(vacancy['alternate_url']),
            'employer_id': employer_id
        }

        if vacancies['payment'] is not None:
            vacancies_data.append(vacancies)

    return vacancies_data


def get_employer(employer_id):
    """
    Получение работодателей
    """

    data = requests.get(f"https://api.hh.ru/employers/{employer_id}")
    data_vacancies = data.json()
    employers = {
        "employer_id": int(employer_id),
        "name": data_vacancies['name'],
        "open_vacancies": data_vacancies['open_vacancies']
    }

    return employers


def db_tables():
    """
    Создание базы данных и таблиц в ней
    """

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

    db_connect = psycopg2.connect(
        host="localhost",
        database="coursework",
        user="postgres",
        password="dmaster8"
    )

    db_connect.cursor().execute(
        """CREATE TABLE employers (
        employer_id INTEGER PRIMARY KEY,
        name varchar(255),
        open_vacancies INTEGER)"""
    )

    db_connect.cursor().execute(
        """CREATE TABLE vacancies (
        vacancy_id SERIAL PRIMARY KEY,
        vacancies_name varchar(255),
        payment INTEGER,
        vacancies_url TEXT,
        employer_id INTEGER REFERENCES employers(employer_id))"""
    )

    db_connect.commit()
    db_connect.close()


def filling_in_tables(employers_list):
    """
    Заполняет таблицы баз данных
    """

    db_connect = psycopg2.connect(
        host="localhost",
        database="coursework",
        user="postgres",
        password="dmaster8")

    cursor_db = db_connect.cursor()

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

        db_connect.commit()

    finally:
        cursor_db.close()
        db_connect.close()
