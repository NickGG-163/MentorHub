## Название учебного проекта:
MentorHub
Version: "0.5.0"

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