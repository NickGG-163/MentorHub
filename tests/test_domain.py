from copy import deepcopy

import pytest

from mentorhub.domain import add_goal, add_task
from mentorhub.models import Goal, Task


@pytest.fixture
def test_goals() -> dict[str, Goal]:
    test_goals = {}
    test_goal = Goal("test_goal", [Task("task_1", False)])
    test_goals["test_goal"] = test_goal
    return test_goals


def test_add_goal_happy(test_goals: dict[str, Goal]):
    res_happy = add_goal(test_goals, "test_goal_1")
    assert res_happy is True
    assert test_goals["test_goal_1"].title == "test_goal_1"


def test_add_goal_negative(test_goals: dict[str, Goal]):
    check = deepcopy(test_goals)
    check_goal = test_goals["test_goal"]
    res_negative = add_goal(test_goals, "test_goal")
    assert res_negative is False
    assert test_goals == check
    assert test_goals["test_goal"] is check_goal


def test_add_task_happy(test_goals: dict[str, Goal]):
    test_task = "task_2"
    test_goal = "test_goal"
    res = add_task(test_goals, test_goal, test_task)
    assert res is True
    assert test_goals[test_goal].tasks[1].title == "task_2"


def test_add_task_negative(test_goals: dict[str, Goal]):
    check = deepcopy(test_goals)
    test_task = "task_1"
    test_goal = "test_goal"
    res = add_task(test_goals, test_goal, test_task)
    assert res is False
    assert test_goals == check
