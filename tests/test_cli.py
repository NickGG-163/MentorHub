from unittest.mock import patch

from mentorhub.cli import add_goal_cli


def test_add_goal_cli():
    goals = {}
    with patch("builtins.input", return_value="goal_1"):
        add_goal_cli(goals)
    assert "goal_1" in goals
