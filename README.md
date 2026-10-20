Название учебного проекта:
MentorHub
Version: 0.3.0"

Описание:
Task-tracker

Цель:
Практика для собеседований и практика для "потрогать технологии руками"

Требования к окружению:
Python >= 3.10

Последовательность действий от клонированного репозитория до запуска (Development setup / Запуск для разработки):
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e .
python3 -m pip install --group dev 
mentorhub

## Команда в bash для проверки качества и тестирования (&& - оператор, позволяющий запустить следующую проверку только после успешного прохождения предыдущей):
ruff format --check && ruff check . && mypy mentorhub && pytest -v

Возможности:
- создание целей;
- добавление задач;
- отметка выполнения;
- расчёт прогресса;
- сохранение состояния в JSON.

Команды:
add-goal
add-task
list
done
exit