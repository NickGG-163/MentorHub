import logging
from enum import Enum

from mentorhub.models import Goal, Task

logger = logging.getLogger(__name__)


class DoneStatus(Enum):
    SUCCESS = "success"
    GOAL_ERROR = "goal_error"
    TASK_ERROR = "task_error"


def add_goal(goals: dict[str, Goal], goal_name: str) -> bool:
    if goal_name in goals:
        return False
    goals[goal_name] = Goal(goal_name)
    return True


def add_task(goals: dict[str, Goal], goal_name: str, task_name: str) -> bool:
    if goal_name not in goals:
        return False
    for task in goals[goal_name].tasks:
        if task.title == task_name:
            logger.debug("Founded dublicate: %s in %s", task.title, goals[goal_name])
            return False
    goals[goal_name].add_task(Task(task_name))
    return True


def get_task_done(goals: dict[str, Goal], goal_name: str, task_name: str) -> DoneStatus:
    if goal_name not in goals:
        return DoneStatus.GOAL_ERROR
    if goals[goal_name].get_task_done(task_name):
        return DoneStatus.SUCCESS
    return DoneStatus.TASK_ERROR
