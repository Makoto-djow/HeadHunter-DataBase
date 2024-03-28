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
