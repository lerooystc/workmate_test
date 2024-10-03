
  <h3 align="center">REST API для онлайн выставки котов</h3>


### Используемый стек технологий в проекте:
* Django
* Django REST Framework
* PostgreSQL
* Docker
* Другие либы (drf-spectacular, django-filter)

### Для работы необходимо:
* Склонировать репозиторий в локальную директорию:
  ```sh
  git clone https://github.com/lerooystc/workmate_test
  ```
* В ./backend создайте ```.env``` (или используйте .env.example) и задайте значения переменных:
    ```sh
    DB_NAME = Название базы данных
    DB_USER = Пользователь базы
    DB_USER_PASSWORD = Пароль пользователя
    DB_HOST = Хост (используйте 'db')
    DB_PORT = Порт (изменить, если 5432 занят)
    SECRET_KEY = Секретный ключ Django (сгенерировать можно с get_random_secret_key() из core.management.utils)
    DJANGO_PORT = Порт, на котором будет расположено приложение
    ```
* Запуск сервера:
    ```sh
    docker compose up
    ```
* Загрузить тестовые данные:
    ```sh
    docker exec НАЗВАНИЕ_КОНТЕЙНЕРА python core/manage.py loaddata basic_db_data
    ```
* API:

  Для Swagger: "/api/v1/schema/swagger-ui/".

* Запустить тесты:
    ```sh
    docker exec НАЗВАНИЕ_КОНТЕЙНЕРА sh -c "cd core && pytest ../tests"
    ```
* Работа с приложением:

  - Породы: Получить список пород может любой, добавлять, изменять или удалять только админ.
  - Коты: CRUD, изменять или удалять кота может лишь его создатель.
  - Оценки: У каждого кота можно получить его оценки, добавить, изменить и получить оценку нынешнего пользователя, а также получить все оценки нынешнего пользователя.
  - Auth: Получение access токена либо по реквизитам для входа, либо по refresh токену, регистрация по email, username и password.
