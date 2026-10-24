### Этап 00 - инициализация

Что сделал:
- Инициализировал Git-репозиторий
- Создал .venv и .gitignore
- Добавил запуск проекта из терминала
- Описал запуск в README

Что понял:
- git add помещает изменения в staging area
- .venv не хранится в Git, окружение воспроизводится локально

Ошибки / нюансы:
- На macOS глобально используется python3, после активации venv доступен python
- Перед commit нужно добавить изменения в staging

Что дальше:
- Создать удалённый репозиторий и пройти branch/PR workflow


### Этап 01 — Базовый Python

Статус: завершен
Реализовал CLI MentorHub 0.1.
Практика:
- dict/list и вложенные структуры;
- функции;
- работа с файлами через with;
- json.dump/json.load;
- FileNotFoundError и JSONDecodeError;
- сохранение состояния между запусками.


### Этап 02 - Инженерный Python

Статус: завершен
Реализовал CLI MentorHub 0.2.
Что сделал:
- разбил монолитный main.py на пакет mentorhub
- разделил CLI / domain / models / storage
- добавил модели Goal и Task
- сделал Storage abstraction
- реализовал JsonStorage и InMemoryStorage
- добавил dependency injection
- добавил storage exceptions и exception chaining
- настроил pyproject.toml
- добавил CLI entry point
- настроил editable install
- добавил Ruff
- обновил README с development setup_

Что изучил:
- package vs module
- absolute / relative imports
- dataclass
- composition
- encapsulation
- @property
- ABC / abstractmethod
- ABC vs Protocol
- Dependency Inversion
- Dependency Injection
- composition root
- shallow copy / deepcopy
- exception translation / chaining
- pyproject.toml
- runtime vs dev dependencies
- editable install
- linting vs formatting

Что могу объяснить:
- зачем разделять CLI, domain и storage и почему бизнес-логика не должна зависеть от интерфейса и конкретного хранилища;
- зачем выделять Goal и Task в отдельные доменные сущности и инкапсулировать поведение внутри них;
- зачем нужен общий контракт Storage через ABC и как это позволяет заменять JsonStorage на InMemoryStorage;
- где в проекте используется Dependency Injection и почему __main__.py выступает composition root;
- зачем нужен pyproject.toml, чем [project] отличается от [build-system] и как работает [project.scripts];
- чем editable install через `pip install -e .` отличается от обычной установки и почему он удобен при разработке;
- почему Ruff относится к dev dependencies, а не к runtime dependencies, и чем `ruff check` отличается от `ruff format`;
- зачем нужны собственные storage exceptions и почему низкоуровневые ошибки вроде JSONDecodeError лучше переводить в ошибки уровня Storage.


### Этап 03 — Тестирование, отладка и качество (MentorHub 0.3)

**Что сделал:**
- Написал 15 тестовых случаев на pytest: unit-тесты моделей и бизнес-логики, integration-тесты JSON-хранилища и тест CLI.
- Освоил fixtures, parametrization, markers, pytest.raises, tmp_path и unittest.mock.patch.
- Исправил баг повторного добавления задачи по циклу RED → GREEN → REFACTOR.
- Изучил Coverage, Debugger, Breakpoints, Watch, Call Stack и логирование.
- Настроил Ruff Formatter, Ruff Linter, mypy и pytest с запуском одной командой.
- Обновил dev-зависимости, .gitignore и README.

**Что понял:**
- Различия между unit-, integration- и E2E-тестами.
- Как обеспечивать изоляцию тестов и проверять изменение состояния объектов.
- Когда применять Mock/Patch и почему не нужно мокировать всё подряд.
- Почему 100% coverage не гарантирует корректность программы.
- Разницу между форматированием, статическим анализом, проверкой типов и тестированием поведения.

**Ошибки и выводы:**
- Ошибался при параметризации тестов и подготовке тестовых данных.
- Разобрал причины AssertionError, ошибок фикстур и несоответствия типов.
- Научился локализовать проблемы через traceback, debugger и логи.

**Результат:** 15 проходящих тестов, исправленный баг с регрессионным тестом и единая команда автоматических проверок.


## Этап 04 — HTTP и API (MentorHub 0.4.0)

### Что реализовал

- Разработал HTTP-сервер на стандартной библиотеке Python (`http.server`).
- Реализовал endpoints: `GET /health`, `GET /goals`, `POST /goals`.
- Интегрировал HTTP API с существующими слоями Domain и Storage.
- Реализовал десериализацию и валидацию JSON-запросов.
- Добавил обработку ошибок с корректными HTTP-статусами: `200`, `201`, `400`, `404`, `409`, `500`.
- Проверил API через `curl`, построил архитектурную схему прохождения запроса.
- Выполнил проверку проекта через pytest и Ruff: 15 тестов пройдены, ошибок линтера нет.

### Что изучил и могу объяснить

- Как работают DNS, IP-адреса, TCP-соединения и сетевые порты.
- Структуру URL: scheme, host, port, path, query, fragment.
- Структуру HTTP request/response: method, headers, body, status code.
- Назначение HTTP-методов GET, POST, PUT, PATCH, DELETE.
- Разницу между безопасностью HTTP-методов и идемпотентностью.
- Почему повторный POST может создавать дубликаты и когда необходим retry.
- Как HTTPS и TLS обеспечивают защиту данных при передаче.
- Разницу между идентификацией, аутентификацией и авторизацией.
- Принципы работы Cookies, Sessions и Bearer Tokens.
- Основные принципы REST, включая Stateless.
- Как анализировать HTTP-запросы через Chrome DevTools.
- Как HTTP-слой взаимодействует с Domain и Storage без дублирования бизнес-логики.

### Результат

MentorHub 0.4.0 поддерживает CLI и HTTP API. Сервер принимает запросы, обрабатывает их через существующую бизнес-логику и сохраняет состояние в JSON-хранилище.


## Этап 05 - PostreSQL, SQLAlchemy и Alembic

### Изучено и реализовано

**PostgreSQL и SQL**

- Создание и изменение таблиц через DDL.
- PRIMARY KEY, FOREIGN KEY, UNIQUE, составные ключи.
- INNER JOIN, LEFT JOIN и связи 1:N / M:N.
- Агрегации, GROUP BY, FILTER, CTE.
- Индексы и анализ производительности через EXPLAIN ANALYZE BUFFERS.
- Транзакции, COMMIT, ROLLBACK, уровни изоляции.
- SQL Injection и параметризованные запросы.
- Резервное копирование через pg_dump и основы восстановления.

**Psycopg 3**

- Подключение Python к PostgreSQL.
- Выполнение параметризованных SQL-запросов.
- Использование cursor, execute, fetchone, fetchall.
- INSERT ... RETURNING и ON CONFLICT.
- Работа с транзакциями через контекстные менеджеры.
- Перенос данных из JSON в PostgreSQL.
- Реализация PostgresStorage через интерфейс Storage.

**SQLAlchemy ORM**

- Engine и Session.
- DeclarativeBase, Mapped, mapped_column.
- ORM-модели и двусторонние relationship.
- ForeignKey и UniqueConstraint.
- SELECT, INSERT, UPDATE, DELETE через ORM.
- Жизненный цикл транзакции: add, flush, commit, rollback.
- Dirty Checking — автоматическое отслеживание изменений ORM-объектов.
- Lazy Loading, selectinload и joinedload.
- Причины возникновения N+1 и способы предотвращения.

**Alembic**

- Инициализация и конфигурация Alembic.
- Связь Alembic с SQLAlchemy metadata.
- Автоматическая генерация миграций.
- Начальная миграция существующей схемы (baseline).
- Регистрация версии через stamp.
- Применение и откат миграций через upgrade и downgrade.
- Проверка соответствия схем через alembic check.
- Добавление столбца description без потери существующих записей.

### Что могу объяснить

- Чем SQLAlchemy ORM отличается от прямой работы через Psycopg.
- Как связаны Python-объекты и строки PostgreSQL.
- Почему relationship не заменяет ForeignKey.
- Чем flush отличается от commit.
- Как ORM формирует SQL-запросы.
- Почему возникает N+1 и как работает selectinload.
- Зачем нужны миграции и почему схема БД должна версионироваться.
- Чем revision, upgrade, downgrade и stamp отличаются друг от друга.
- Как заменить реализацию хранилища без изменения доменной логики.

### Практический результат

MentorHub работает с PostgreSQL через PostgresStorage. Выполнен импорт JSON-данных, реализовано сохранение связанных сущностей и проверены операции через CLI.

Созданы ORM-модели и миграции Alembic, протестированы чтение, создание, изменение, удаление и откат транзакций.

Pytest: 15 тестов пройдены.