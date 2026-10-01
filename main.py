def add_goal(goals):
    goals.append(input())


def print_goals(goals):
    if goals:
        print(goals)
    else:
        print('Список целей пуст')


def run_cli():
    goals = []

    while True:
        command = input()

        if command.lower() == 'add':
            add_goal(goals)
        elif command.lower() == 'list':
            print_goals(goals)
        elif command.lower() == 'exit':
            print('Программа завершается')
            break
        else:
            print('Команда неизвестна, повторите ввод')


run_cli()