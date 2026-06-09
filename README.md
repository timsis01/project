# Tasks

Веб-приложение для ведения списка дел с разбивкой по дням.

## Скрины и функционал



## Технологии

- Django
- PostgreSQL
- HTML + CSS
- Gunicorn + Nginx
- Docker
- pytest

## Запуск через Docker

Нужен установленный Docker. В корне проекта должен лежать файл `.env` (см. ниже).

```bash
docker compose up -d --build
docker compose exec web python manage.py migrate
```

Приложение: http://localhost

Остановить: `docker compose down` (данные БД сохраняются в volume).

## Файл `.env`

В корне проекта (рядом с `manage.py`):

```ini
SECRET_KEY=ваш-секретный-ключ
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost,web
DB_NAME=tasks_db
DB_USER=tasks_user
DB_PASSWORD=ваш-пароль
DB_HOST=db
DB_PORT=5432
```

Сгенерировать `SECRET_KEY`:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Тесты

```bash
pytest
```

