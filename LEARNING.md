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



Этап 01 — Базовый Python

Статус: завершен
Реализовал CLI MentorHub 0.1.
Практика:
- dict/list и вложенные структуры;
- функции;
- работа с файлами через with;
- json.dump/json.load;
- FileNotFoundError и JSONDecodeError;
- сохранение состояния между запусками.

Этап 02 - Инженерный Python

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