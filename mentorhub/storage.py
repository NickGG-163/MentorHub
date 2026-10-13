from enum import Enum
import json
from mentorhub.models import Goal, Task


class OpenStatus(Enum):
    SUCCESS = "success"
    NOT_FOUND_ERROR = "file_not_found"
    DECODE_ERROR = "file_is_broken"


def save_goals(goals: dict[str, Goal], filename: str) -> None:
    data = {}
    for goal in goals.values():
        data[goal.title] = [{'title': t.title, 'done': t.done}
                            for t in goal.tasks]

    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def open_goals(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            res = OpenStatus.SUCCESS
        goals = {}
        for goal_name, tasks in data.items():
            goals[goal_name] = Goal(
                goal_name, [Task(t['title'], t['done']) for t in tasks])
    except (FileNotFoundError, json.JSONDecodeError) as error:
        if isinstance(error, FileNotFoundError):
            res = OpenStatus.NOT_FOUND_ERROR
        elif isinstance(error, json.JSONDecodeError):
            res = OpenStatus.DECODE_ERROR
        goals = {}
    return (goals, res)
