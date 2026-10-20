import pytest

from mentorhub.models import Goal, Task
from mentorhub.storage import JsonStorage
from mentorhub.storage_base import StorageDecodeError, StorageNotFoundError


def test_storage(tmp_path):
    test_goals = {
        "test_goal": Goal("test_goal", [Task("task_1", True), Task("task_2", False)])
    }
    file_path = tmp_path / "test_data.json"
    test_storage = JsonStorage(file_path)

    test_storage.save(test_goals)
    assert file_path.is_file()
    res = test_storage.load()
    assert res == test_goals


def test_load_storage_not_found(tmp_path):
    file_path = tmp_path / "test_data.json"
    test_storage = JsonStorage(file_path)
    with pytest.raises(StorageNotFoundError):
        test_storage.load()


def test_storage_decode_error(tmp_path):
    test_goals = (
        "{'test_goal': Goal('test_goal', [Task('task_1', True), Task('task_2', False)])"
    )
    file_path = tmp_path / "test_data.json"
    file_path.write_text(test_goals, encoding="utf-8")
    test_storage = JsonStorage(file_path)
    with pytest.raises(StorageDecodeError):
        test_storage.load()
