import pytest

from mentorhub.models import Goal, Task


@pytest.fixture
def test_goal():
    test_goal_1 = Goal('test', [Task('task_1', True), Task('task_2', False)])
    return test_goal_1


def test_calc_progress(test_goal: Goal):
    res = test_goal.progress
    assert res == 50
