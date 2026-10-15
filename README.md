Название учебного проекта:
MentorHub
Version: 0.1"

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
ruff check . 
ruff format --check .

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