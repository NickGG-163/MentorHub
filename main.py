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
        print(f'\nЦель: {goal_name}')

        if not tasks:
            print('  Задач пока нет')
            continue

        for task in tasks:
            if task['done']:
                print(f'  - {task['title']}  [V]')
            else:
                print(f'  - {task['title']}')


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


def run_cli():
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
            print('Программа завершается')
            break

        else:
            print('Команда неизвестна, повторите ввод')


run_cli()
