import json


def add_goal(goals):
    goal_name = input('Введите название цели: ')
    if goal_name in goals:
        print('Такая цель уже существует')
        return

    goals[goal_name] = []


def add_task(goals):
    goal_name = input('Введите название цели: ')
    if goal_name not in goals:
        print('Такой цели нет')
        return

    task_name = input('Введите название задачи: ')
    goals[goal_name].append({'title': task_name, 'done': False})


def print_goals(goals):
    if not goals:
        print('Список целей пуст')
        return

    for goal_name, tasks in goals.items():

        progress = 0
        if tasks:
            progress = round(
                len([t for t in tasks if t['done']]) / len(tasks) * 100, 1)

        print(f'\nЦель: {goal_name} -> {progress}%')

        if not tasks:
            print('  Задач пока нет')
            continue

        for task in tasks:
            if task['done']:
                print(f' [X] - {task['title']}')
            else:
                print(f' [ ] - {task['title']}')


def get_task_done(goals):
    goal_name = input('Введите название цели: ')
    if goal_name not in goals:
        print('Такой цели нет')
        return

    task_name = input('Введите название задачи: ')
    not_found = True
    for task in goals[goal_name]:
        if task['title'] == task_name:
            task['done'] = True
            not_found = False
            break

    if not_found:
        print('Такой задачи не существует')


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
            add_goal(goals)

        elif command == 'add-task':
            add_task(goals)

        elif command == 'list':
            print_goals(goals)

        elif command == 'done':
            get_task_done(goals)

        elif command == 'exit':

            with open(filename, 'w', encoding='utf-8') as file:
                save_goals(goals, file)

            print('Программа завершается')
            break

        else:
            print('Команда неизвестна, повторите ввод')


run_cli()
