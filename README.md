# Tasks

Веб-приложение для ведения списка дел с разбивкой по дням.

## Скрины и функционал
### Форма входа
<img width="1854" height="948" alt="Снимок экрана 2026-06-09 225334" src="https://github.com/user-attachments/assets/18ca72c2-9859-4939-9248-875cecd21cd3" />

### Форма регистрации
<img width="1852" height="949" alt="Снимок экрана 2026-06-09 225301" src="https://github.com/user-attachments/assets/773fc22f-2f10-4267-8ca3-28f410098f65" />

### Главная страница с задачами пользователя
<img width="1783" height="946" alt="Снимок экрана 2026-06-09 231514" src="https://github.com/user-attachments/assets/997f5a54-8cf2-49cd-95c5-490954263e29" />

### Форма создания новой задачи
<img width="1853" height="949" alt="Снимок экрана 2026-06-09 225206" src="https://github.com/user-attachments/assets/a9fa02c7-bf8d-4beb-8ff1-97997f29f5d8" />

## Технологии

- Django, PostgreSQL, HTML, CSS, Gunicorn, Nginx, Docker, pytest

## Запуск через Docker

Нужен установленный Docker. В корне проекта должен лежать файл `.env`.

```bash
docker compose up -d --build
docker compose exec web python manage.py migrate
```

Приложение: http://localhost

Остановить: `docker compose down`.

## Файл `.env`

В корне проекта (рядом с `manage.py`):

```ini
SECRET_KEY=ваш-секретный-ключ
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost,web
DB_NAME=tasks_db
DB_USER=tasks_user
DB_PASSWORD=ваш-пароль-postgresql
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

