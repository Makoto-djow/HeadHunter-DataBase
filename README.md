# HeadHunter-DataBase

Программа получает данные о компаниях и вакансиях с сайта hh.ru, 
проектирует таблицы в БД PostgreSQL и загружает полученные данные в созданные таблицы.

Пользователю нужно ввести только ключевые слова для фильтрации вакансий по ним
Остальная информация выводится автоматически

Шаги для установки:

1. Клонировать репозиторий
2. Установить зависимости из файла pyproject.toml
3. В папке "src" файл "main.py". В файле содержится переменная "employers_list". В ней можно заменить значения ID компаний на свои.
