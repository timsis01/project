# Менеджер задач (Task Manager)

Веб-приложение для ведения списка дел с разбивкой по дням.

## Возможности

- Регистрация, вход и выход (аутентификация Django)
- Изоляция данных: пользователь работает только со своими задачами
- Просмотр задач по дням с навигацией и кнопкой «Сегодня»
- Создание, редактирование, удаление задач и переключение статуса «выполнено»
- Переключение статуса без перезагрузки страницы (HTMX)

## Технологии

- Django
- PostgreSQL
- HTML + CSS
- Gunicorn + Nginx
- Docker
- pytest

## Запуск через Docker (рекомендуется)

Нужен установленный Docker. В корне проекта должен лежать файл `.env` (см. ниже).

```bash
docker compose up -d --build
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser   # по желанию
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

Файл не коммитится. Сгенерировать `SECRET_KEY`:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Запуск локально (без Docker)

Нужен запущенный PostgreSQL. Подними только базу в Docker (`docker compose up -d db`) или поставь Postgres на ПК, и укажи в `.env` `DB_HOST=localhost`.

```bash
python -m venv venv      
source venv/bin/activate       
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Приложение: http://127.0.0.1:8000

## Тесты

```bash
pytest
```

