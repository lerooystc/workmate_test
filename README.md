
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
* Активация виртуального окружения и создание зависимостей:
  ```sh
  python -m venv venv
  ./venv/Scripts/activate
  cd backend
  pip install -r requirements.txt
  ```
* В ./backend создайте ```.env``` и задайте значения переменных:
    ```sh
    DB_NAME =
    DB_USER =
    DB_USER_PASSWORD =
    DB_HOST =
    DB_PORT =
    SECRET_KEY =
    DJANGO_PORT =
    ```
* Запуск сервера:
    ```sh
    docker compose up
    ```
* API:

  Для Swagger добавьте в конец адресной строки "/docs".

* Работа с приложением:

  - TBD
