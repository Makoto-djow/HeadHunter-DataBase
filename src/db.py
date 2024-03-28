# import psycopg2
#
#
# class DBManager:
#     """
#     Подключается к БД PostgreSQL
#     """
#
#     def get_companies_and_vacancies_count(self):
#         """
#         Получает список всех компаний и количество вакансий у каждой компании.
#         """
#
#         with psycopg2.connect(
#                 host="localhost",
#                 database="coursework",
#                 user="postgres",
#                 password="dmaster8") as conn:
#
#             with conn.cursor() as cur:
#                 cur.execute(
#                     "SELECT name, COUNT(vacancies_name) AS count_vacancies  "
#                     "FROM employers "
#                     "JOIN vacancies USING (employer_id) "
#                     "GROUP BY employers.name"
#                 )
#                 set_db = cur.fetchall()
#             conn.commit()
#         return set_db
#
#     def get_all_vacancies(self):
#         """
#         Получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
#         """
#         with psycopg2.connect(
#                 host="localhost",
#                 database="coursework",
#                 user="postgres",
#                 password="dmaster8") as conn:
#
#             with conn.cursor() as cur:
#                 cur.execute(
#                     "SELECT employers.name, vacancies.vacancies_name, "
#                     "vacancies_url "
#                     "FROM employers "
#                     "JOIN vacancies USING (employer_id)"
#                 )
#                 set_db = cur.fetchall()
#             conn.commit()
#         return set_db
#
#     def get_avg_salary(self):
#         """
#         Получает среднюю зарплату по вакансиям.
#         """
#         with psycopg2.connect(
#                 host="localhost",
#                 database="coursework",
#                 user="postgres",
#                 password="dmaster8") as conn:
#
#             with conn.cursor() as cur:
#                 cur.execute(
#                     "SELECT AVG(payment) as avg_payment FROM vacancies "
#                 )
#                 set_db = cur.fetchall()
#             conn.commit()
#         return set_db
#
#     def get_vacancies_with_higher_salary(self):
#         """
#         Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
#         """
#
#         with psycopg2.connect(
#                 host="localhost",
#                 database="coursework",
#                 user="postgres",
#                 password="dmaster8") as conn:
#
#             with conn.cursor() as cur:
#                 cur.execute(
#                     "SELECT * FROM vacancies "
#                     "WHERE payment > (SELECT AVG(payment) FROM vacancies) "
#                 )
#                 set_db = cur.fetchall()
#             conn.commit()
#         return set_db
#
#     def get_vacancies_with_keyword(self, word):
#         """
#         Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например python.
#         """
#
#         with psycopg2.connect(
#                 host="localhost",
#                 database="coursework",
#                 user="postgres",
#                 password="dmaster8") as conn:
#
#             with conn.cursor() as cur:
#                 cur.execute(
#                     "SELECT * FROM vacancies "
#                     f"WHERE lower(vacancies_name) LIKE lower('%{word}%') "
#                     f"OR lower(vacancies_name) LIKE lower('%{word}') "
#                     f"OR lower(vacancies_name) LIKE lower('{word}%');"
#                 )
#                 set_db = cur.fetchall()
#             conn.commit()
#         return set_db
