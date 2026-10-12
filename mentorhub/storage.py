from enum import Enum
import json


class OpenStatus(Enum):
    SUCCESS = "success"
    NOT_FOUND_ERROR = "file_not_found"
    DECODE_ERROR = "file_is_broken"


def save_goals(goals, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(goals, file, ensure_ascii=False, indent=2)


def open_goals(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            goals = json.load(file)
            res = OpenStatus.SUCCESS
    except (FileNotFoundError, json.JSONDecodeError) as error:
        if isinstance(error, FileNotFoundError):
            res = OpenStatus.NOT_FOUND_ERROR
        elif isinstance(error, json.JSONDecodeError):
            res = OpenStatus.DECODE_ERROR
        goals = {}
    return (goals, res)


