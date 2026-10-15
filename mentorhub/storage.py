import json
from copy import deepcopy

from mentorhub.models import Goal, Task
from mentorhub.storage_base import (
    Storage,
    StorageDecodeError,
    StorageNotFoundError,
    StorageSaveDataError,
)


class JsonStorage(Storage):
    def __init__(self, filename: str):
        self.filename = filename

    def save(self, goals: dict[str, Goal]) -> None:
        data = {}
        for goal in goals.values():
            data[goal.title] = [{"title": t.title, "done": t.done} for t in goal.tasks]
        try:
            with open(self.filename, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2)
        except OSError as error:
            raise StorageSaveDataError() from error

    def load(self) -> dict[str, Goal]:
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
            goals = {}
            for goal_name, tasks in data.items():
                goals[goal_name] = Goal(
                    goal_name, [Task(t["title"], t["done"]) for t in tasks]
                )
        except (FileNotFoundError, json.JSONDecodeError) as error:
            if isinstance(error, FileNotFoundError):
                raise StorageNotFoundError() from error
            if isinstance(error, json.JSONDecodeError):
                raise StorageDecodeError() from error
        return goals


class InMemoryStorage(Storage):
    def __init__(self):
        self.goals = {}

    def save(self, goals: dict[str, Goal]) -> None:
        self.goals = deepcopy(goals)

    def load(self) -> dict[str, Goal]:
        return deepcopy(self.goals)
