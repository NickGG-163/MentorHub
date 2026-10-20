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