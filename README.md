# Inforce Python Task

## Requirements
- Docker & docker-compose OR Python 3.11 + Postgres

## Quick start (Docker)
1. docker-compose up --build
2. docker-compose exec web python manage.py migrate
3. docker-compose exec web python manage.py createsuperuser

## Local without Docker
1. Create virtualenv, pip install -r requirements.txt
2. Configure Postgres and env vars
3. python manage.py migrate
4. python manage.py runserver

## API
- POST /api/auth/register/ — реєстрація (username, password, email)
- POST /api/auth/token/ — отримати JWT (username, password)
- POST /api/restaurants/ — створити ресторан (auth)
- POST /api/menus/ — створити меню (restaurant, date, items) (auth)
- GET /api/menus/today/ — меню на сьогодні (auth)

## Tests
Запуск тестів:
pytest
