from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from mentorhub.api import app
from mentorhub.auth_dependencies import get_current_user
from mentorhub.goals.goals_router import get_goal_service
from mentorhub.orm_models import GoalORM, UserORM

client = TestClient(app)


@pytest.fixture()
def fake_goal_service():
    fake_goal_service = Mock()
    fake_goal_service.user_has_access.return_value = True
    app.dependency_overrides[get_goal_service] = lambda: fake_goal_service
    yield fake_goal_service
    app.dependency_overrides.pop(get_goal_service, None)


@pytest.fixture(autouse=True)
def authenticated_user():
    user = UserORM(id=1, name="Tester")

    app.dependency_overrides[get_current_user] = lambda: user

    yield

    app.dependency_overrides.pop(get_current_user, None)


def test_health_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_invalid_goal_id():
    response = client.get("/goals/abc")

    assert response.status_code == 422
    assert "error" in response.json()


def test_get_goal_ok(fake_goal_service):
    fake_goal_service.get_goal.return_value = GoalORM(
        id=1, title='Тестовая цель', description=None)

    response = client.get("/goals/1")

    assert response.status_code == 200
    assert response.json()['id'] == 1
    fake_goal_service.get_goal.assert_called_once_with(1)


def test_goal_not_found(fake_goal_service):
    fake_goal_service.get_goal.return_value = None

    response = client.get("/goals/999")

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "not_found"
    fake_goal_service.get_goal.assert_called_once_with(999)
