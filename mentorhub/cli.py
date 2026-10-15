from mentorhub.domain import DoneStatus, add_goal, add_task, get_task_done
from mentorhub.models import Goal
from mentorhub.storage_base import (
    Storage,
    StorageDecodeError,
    StorageNotFoundError,
    StorageSaveDataError,
)


def print_goals(goals: dict[str, Goal]):
    if not goals:
        print("Список целей пуст")
        return

    for goal in goals.values():
        print(f"\nЦель: {goal.title} -> {goal.progress}%")

        if not goal.tasks:
            print("  Задач пока нет")
            continue

        for task in goal.tasks:
            if task.done:
                print(f" [X] - {task.title}")
            else:
                print(f" [ ] - {task.title}")


def add_goal_cli(goals):
    goal_name = input("Введите название цели: ")
    created = add_goal(goals, goal_name)
    if created:
        print("Цель добавлена")
    else:
        print("Такая цель уже существует")


def add_task_cli(goals):
    goal_name = input("Введите название цели: ")
    task_name = input("Введите название задачи: ")
    created = add_task(goals, goal_name, task_name)
    if created:
        print("Задача добавлена")
    else:
        print("Такой цели нет")


def get_task_done_cli(goals):
    goal_name = input("Введите название цели: ")
    task_name = input("Введите название задачи: ")
    status = get_task_done(goals, goal_name, task_name)

    if status is DoneStatus.GOAL_ERROR:
        print("Такой цели нет")
    elif status is DoneStatus.TASK_ERROR:
        print("Такой задачи не существует")
    elif status is DoneStatus.SUCCESS:
        print("Задача отмечена выполненной")


def run_cli(storage: Storage):
    try:
        goals = storage.load()
    except StorageNotFoundError:
        goals = {}
        print("Хранилище не было найдено, начинаем с пустого списка")
    except StorageDecodeError:
        goals = {}
        print("Не удалось прочитать данные хранилища, начинаем с пустого списка")

    while True:
        command = input("\nВведите команду: ").lower()

        if command == "add-goal":
            add_goal_cli(goals)

        elif command == "add-task":
            add_task_cli(goals)

        elif command == "done":
            get_task_done_cli(goals)

        elif command == "list":
            print_goals(goals)

        elif command == "exit":
            try:
                storage.save(goals)
                break
            except StorageSaveDataError:
                print("Не удалось сохранить данные. Повторите ввод команды.")
                continue

        else:
            print("Команда неизвестна, повторите ввод")
