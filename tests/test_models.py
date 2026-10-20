from copy import deepcopy

import pytest

from mentorhub.models import Goal, Task


@pytest.fixture
def test_goal():
    test_goal_1 = Goal("test", [Task("task_1", True), Task("task_2", False)])
    return test_goal_1


def test_calc_progress(test_goal: Goal):
    res = test_goal.progress
    assert res == 50


@pytest.mark.unit
@pytest.mark.parametrize(
    "tasks, tasks_done, expected", [(0, 0, 0), (2, 0, 0), (2, 1, 50), (2, 2, 100)]
)
def test_calc_progress_param(tasks, tasks_done, expected):
    test_goal = Goal("test_goal", [])
    for i in range(tasks):
        if i < tasks_done:
            test_goal.add_task(Task(str(i), True))
        else:
            test_goal.add_task(Task(str(i), False))
    res = test_goal.progress
    assert res == expected


def test_get_task_done_happy(test_goal: Goal):
    res = test_goal.get_task_done("task_2")
    assert res is True
    assert test_goal.tasks[1].done is True


def test_get_task_done_negative(test_goal: Goal):
    check = deepcopy(test_goal)
    res = test_goal.get_task_done("task_unknown")
    assert res is False
    assert test_goal == check
