import json
from mentorhub.domain import DoneStatus, add_goal, add_task, calc_progress, get_task_done


def print_goals(goals):
    if not goals:
        print('Список целей пуст')
        return

    for goal_name, tasks in goals.items():
        progress = calc_progress(tasks)
        print(f'\nЦель: {goal_name} -> {progress}%')

        if not tasks:
            print('  Задач пока нет')
            continue

        for task in tasks:
            if task['done']:
                print(f' [X] - {task['title']}')
            else:
                print(f' [ ] - {task['title']}')


def save_goals(goals, file):
    json.dump(goals, file, ensure_ascii=False, indent=2)


def run_cli():
    filename = 'data.json'

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            goals = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as error:
        if isinstance(error, FileNotFoundError):
            print('Файл data.json не был найден, начинаем с пустого списка')
        elif isinstance(error, json.JSONDecodeError):
            print('Не удалось прочитать data.json, начинаем с пустого списка')
        goals = {}

    while True:
        command = input('\nВведите команду: ').lower()

        if command == 'add-goal':
            goal_name = input('Введите название цели: ')
            created = add_goal(goals, goal_name)
            if created:
                print('Цель добавлена')
            else:
                print('Такая цель уже существует')

        elif command == 'add-task':
            goal_name = input('Введите название цели: ')
            task_name = input('Введите название задачи: ')
            created = add_task(goals, goal_name, task_name)
            if created:
                print('Задача добавлена')
            else:
                print('Такой цели нет')

        elif command == 'done':
            goal_name = input('Введите название цели: ')
            task_name = input('Введите название задачи: ')
            status = get_task_done(goals, goal_name, task_name)

            if status is DoneStatus.GOAL_ERROR:
                print('Такой цели нет')
            elif status is DoneStatus.TASK_ERROR:
                print('Такой задачи не существует')
            elif status is DoneStatus.SUCCESS:
                print('Задача отмечена выполненной')

        elif command == 'list':
            print_goals(goals)

        elif command == 'exit':

            with open(filename, 'w', encoding='utf-8') as file:
                save_goals(goals, file)

            print('Программа завершается')
            break

        else:
            print('Команда неизвестна, повторите ввод')


run_cli()
