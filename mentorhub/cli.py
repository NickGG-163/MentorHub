from mentorhub.domain import DoneStatus, add_goal, add_task, calc_progress, get_task_done
from mentorhub.storage import OpenStatus, open_goals, save_goals


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


def add_goal_cli(goals):
    goal_name = input('Введите название цели: ')
    created = add_goal(goals, goal_name)
    if created:
        print('Цель добавлена')
    else:
        print('Такая цель уже существует')


def add_task_cli(goals):
    goal_name = input('Введите название цели: ')
    task_name = input('Введите название задачи: ')
    created = add_task(goals, goal_name, task_name)
    if created:
        print('Задача добавлена')
    else:
        print('Такой цели нет')


def get_task_done_cli(goals):
    goal_name = input('Введите название цели: ')
    task_name = input('Введите название задачи: ')
    status = get_task_done(goals, goal_name, task_name)

    if status is DoneStatus.GOAL_ERROR:
        print('Такой цели нет')
    elif status is DoneStatus.TASK_ERROR:
        print('Такой задачи не существует')
    elif status is DoneStatus.SUCCESS:
        print('Задача отмечена выполненной')


def open_goals_cli(filename):
    goals, res = open_goals(filename)
    if res is OpenStatus.SUCCESS:
        return goals
    elif res is OpenStatus.NOT_FOUND_ERROR:
        print('Файл data.json не был найден, начинаем с пустого списка')
    elif res is OpenStatus.DECODE_ERROR:
        print('Не удалось прочитать data.json, начинаем с пустого списка')
    return goals


def run_cli():
    filename = 'data.json'
    goals = open_goals_cli(filename)

    while True:
        command = input('\nВведите команду: ').lower()

        if command == 'add-goal':
            add_goal_cli(goals)

        elif command == 'add-task':
            add_task_cli(goals)

        elif command == 'done':
            get_task_done_cli(goals)

        elif command == 'list':
            print_goals(goals)

        elif command == 'exit':
            save_goals(goals, filename)
            break

        else:
            print('Команда неизвестна, повторите ввод')
