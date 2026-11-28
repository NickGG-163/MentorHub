## Название учебного проекта:
MentorHub
Version: "0.6.0"

## Описание:
Task-tracker

## Цель:
Практика для собеседований и практика для "потрогать технологии руками"

## Требования к окружению:
Python >= 3.10

## Последовательность действий от клонированного репозитория до запуска (Development setup / Запуск для разработки):
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e .
python3 -m pip install --group dev 
mentorhub

## Команда в bash для проверки качества и тестирования (&& - оператор, позволяющий запустить следующую проверку только после успешного прохождения предыдущей):
ruff format --check && ruff check . && mypy mentorhub && pytest -v

## Возможности:
- создание целей;
- добавление задач;
- отметка выполнения;
- расчёт прогресса;
- сохранение состояния в JSON.

## Команды:
add-goal
add-task
list
done
exit

## HTTP API — MentorHub 0.4.0

Реализован HTTP-сервер на стандартной библиотеке Python (`http.server`) с использованием существующих слоёв Domain и Storage.

### Запуск HTTP-сервера

Из корня проекта:

`python3 -m mentorhub.http_server`

Адрес сервера: `http://127.0.0.1:8000`

### Доступные endpoints

| Метод | Endpoint | Описание |
|---|---|---|
| GET | `/health` | Проверка работоспособности сервера |
| GET | `/goals` | Получение списка целей и задач |
| POST | `/goals` | Создание новой цели |

Пример тела запроса для `POST /goals`:

`{"title": "Изучить HTTP"}`

### HTTP-статусы

- `200 OK` — успешное получение данных.
- `201 Created` — цель успешно создана.
- `400 Bad Request` — некорректные входные данные.
- `404 Not Found` — неизвестный ресурс.
- `409 Conflict` — цель уже существует.
- `500 Internal Server Error` — ошибка хранилища.

Данные загружаются и сохраняются в локальном файле `data.json`.

HTTP API использует существующую бизнес-логику MentorHub. CLI продолжает работать независимо от HTTP-сервера.

## PostgreSQL, SQLAlchemy и Alembic

MentorHub поддерживает хранение целей и задач в PostgreSQL с сохранением существующей слоистой архитектуры.

### Реализовано

- PostgreSQL: таблицы `users`, `goals`, `tasks`, `goal_members`, ограничения PK, FK и UNIQUE.
- `PostgresStorage` на Psycopg 3: загрузка и сохранение целей и задач, UPSERT, транзакции.
- Импорт существующих данных из JSON в PostgreSQL.
- Автоматическая запись `completed_at` при изменении статуса задачи.
- SQL-запросы с JOIN, CTE, FILTER, агрегациями и анализом планов через `EXPLAIN ANALYZE`.
- SQLAlchemy ORM: модели, `relationship`, Session, CRUD, `selectinload` и `joinedload`.
- Alembic: начальная схема, версионирование БД, применение и откат миграций.
- Добавлен необязательный столбец `description` для целей.

### Архитектура

- `domain.py`, `models.py` — бизнес-логика и доменные модели.
- `storage_base.py` — интерфейс хранилища.
- `storage.py` — реализация JSON-хранилища.
- `postgres_storage.py` — реализация PostgreSQL-хранилища.
- `orm_models.py` — ORM-модели SQLAlchemy.
- `database.py` — настройка SQLAlchemy Engine.
- `migrations/` — миграции Alembic.
- `SQL/` — учебные SQL-запросы.

CLI использует `PostgresStorage` на Psycopg. SQLAlchemy изучен и проверен отдельно, без необходимости переписывать бизнес-логику.

### Работа с базой данных

Для новой пустой PostgreSQL-базы:

```bash
alembic upgrade head
```

Проверка текущей ревизии и соответствия схемы:

```bash
alembic current
alembic check
```

При развёртывании требуется настроенная локальная PostgreSQL и установленные зависимости проекта.

### Проверки качества

- Pytest — 15 успешных тестов.
- Ruff — форматирование и статический анализ Python-кода.
- Интеграционная проверка сохранения и загрузки данных через CLI.
- Проверка миграций Alembic: upgrade, downgrade, check.


## FastAPI Backend — MentorHub 0.6.0

Реализован REST API на FastAPI с хранением данных в PostgreSQL, JWT-аутентификацией и разграничением доступа к целям и задачам.

### Реализовано

- FastAPI: маршрутизация, валидация запросов и формирование HTTP-ответов.
- Pydantic: схемы создания, обновления и получения данных.
- Архитектура Router → Service → Repository.
- SQLAlchemy ORM: работа с PostgreSQL через Session.
- Регистрация пользователей и безопасное хеширование паролей через Argon2.
- JWT access tokens с проверкой подписи и срока действия.
- Dependency Injection через FastAPI Depends.
- Проверка прав доступа пользователей к целям и связанным задачам.
- Централизованная обработка HTTP-ошибок.
- Unit- и интеграционные тесты с pytest.

### Архитектура

- `api.py` — создание FastAPI-приложения, подключение роутеров, обработка ошибок.
- `api_schemas.py` — Pydantic-схемы запросов и ответов.
- `goals/` — Router, Service и Repository для целей.
- `tasks/` — Router, Service и Repository для задач.
- `users/` — регистрация, авторизация и работа с пользователями.
- `auth_dependencies.py` — получение текущего пользователя по JWT.
- `security.py` — хеширование паролей, создание и проверка JWT.
- `database.py` — SQLAlchemy Engine и управление сессиями.
- `orm_models.py` — ORM-модели PostgreSQL.
- `migrations/` — миграции Alembic.

### Запуск FastAPI

Из корня проекта после установки зависимостей и настройки PostgreSQL:

`alembic upgrade head`

Установить JWT_SECRET_KEY в текущем терминале:

`export JWT_SECRET_KEY="$(openssl rand -hex 32)"`

Запустить сервер:

`uvicorn mentorhub.api:app --reload`

Адрес API: `http://127.0.0.1:8000`

Swagger UI: `http://127.0.0.1:8000/docs`

### Локальный запуск через Docker Compose

Запусти Docker Desktop. Из корня свежего клона создай локальный файл настроек:

```bash
cp .env.example .env
```

Укажи в `.env` свой `POSTGRES_PASSWORD`. Для локального запуска подойдёт пароль из букв и цифр.

Выполни команды по порядку в одной вкладке терминала:

```bash
export JWT_SECRET_KEY="$(openssl rand -hex 32)"
docker compose up --wait db
docker compose run --build --rm mentorhub alembic upgrade head
docker compose up -d mentorhub
curl -i --retry 5 --retry-connrefused --retry-delay 1 http://127.0.0.1:8000/health
```

Ожидаемый ответ — `HTTP/1.1 200 OK` и `{"status":"ok"}`.

Чтобы найти запись о запросе в логах приложения:

```bash
docker compose logs --tail=30 mentorhub
```

В JSON-записи `request_completed` для `GET /health` поле `request_id`
совпадает со значением заголовка `X-Request-ID` из HTTP-ответа.

Если Docker сообщает, что порт `8000` уже занят, проверьте через `docker ps`,
какой контейнер публикует этот порт. После освобождения порта пересоздайте
контейнер приложения командой `docker compose up -d --force-recreate mentorhub`.

### CI

GitHub Actions запускает юнит-тесты для pull request и при пуше в `main`.
Ту же проверку можно запустить локально после установки dev-зависимостей:

```bash
python -m pytest -m unit -q
```

### Доступные endpoints

| Метод | Endpoint | Описание |
|---|---|---|
| GET | `/health` | Проверка работоспособности |
| POST | `/auth/register` | Регистрация пользователя |
| POST | `/auth/login` | Авторизация и получение JWT |
| GET | `/auth/me` | Получение текущего пользователя |
| POST | `/goals` | Создание цели |
| GET | `/goals/{goal_id}` | Получение цели |
| PATCH | `/goals/{goal_id}` | Обновление цели |
| DELETE | `/goals/{goal_id}` | Удаление цели |
| POST | `/goals/{goal_id}/tasks` | Создание задачи |
| GET | `/goals/{goal_id}/tasks/{task_id}` | Получение задачи |
| PATCH | `/goals/{goal_id}/tasks/{task_id}` | Обновление задачи |
| DELETE | `/goals/{goal_id}/tasks/{task_id}` | Удаление задачи |

Защищённые endpoints требуют заголовок `Authorization: Bearer <JWT>`.

### Аутентификация и права доступа

- Пароли хранятся в виде Argon2-хешей.
- После успешного входа пользователь получает JWT access token сроком на 30 минут.
- FastAPI-зависимость `get_current_user` проверяет JWT и получает пользователя из PostgreSQL.
- Создатель цели автоматически становится её участником.
- Доступ к целям и задачам ограничивается участием пользователя в цели.
- Используются HTTP-статусы 401, 403, 404, 409 и 422.

### Тестирование

- Unit-тесты с Mock и dependency_overrides.
- Интеграционные тесты с PostgreSQL.
- Изоляция тестов через savepoint и rollback.
- Pytest — 26 успешных тестов.
- Ruff — проверка без ошибок.

Команды:

`pytest -q`

`ruff check .`

Для интеграционных тестов используется отдельная база `mentorhub_test`.

### Отложенные задачи

- Middleware: логирование HTTP-запросов и измерение времени обработки.
- Дополнительные интеграционные тесты авторизации с настоящими JWT.
- Централизованная конфигурация PostgreSQL и JWT.
- Финальная проверка пограничных случаев и обработка отдельных ошибок.