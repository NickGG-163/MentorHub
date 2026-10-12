from enum import Enum


class DoneStatus(Enum):
    SUCCESS = "success"
    GOAL_ERROR = "goal_error"
    TASK_ERROR = "task_error"


def calc_progress(tasks):
    progress = 0

    if tasks:
        progress = round(
            len([t for t in tasks if t['done']]) / len(tasks) * 100, 1)

    return progress


def add_goal(goals, goal_name):
    if goal_name in goals:
        return False
    goals[goal_name] = []
    return True


def add_task(goals, goal_name, task_name):
    if goal_name not in goals:
        return False
    goals[goal_name].append({'title': task_name, 'done': False})
    return True


def get_task_done(goals, goal_name, task_name):
    if goal_name not in goals:
        return DoneStatus.GOAL_ERROR

    for task in goals[goal_name]:
        if task['title'] == task_name:
            task['done'] = True
            return DoneStatus.SUCCESS

    return DoneStatus.TASK_ERROR
