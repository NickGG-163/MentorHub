import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from mentorhub.api import app
from mentorhub.auth_dependencies import get_current_user
from mentorhub.database import get_db_session
from mentorhub.orm_models import UserORM

test_engine = create_engine(
    "postgresql+psycopg:///mentorhub_test"
)


@pytest.fixture
def db_client():
    with test_engine.connect() as connection:
        transaction = connection.begin()

        with Session(
            bind=connection,
            join_transaction_mode="create_savepoint"
        ) as session:

            def override_session():
                yield session

            app.dependency_overrides[get_db_session] = override_session

            user = UserORM(name="Test user")
            session.add(user)
            session.flush()

            app.dependency_overrides[get_current_user] = lambda: user

            try:
                with TestClient(app) as client:
                    yield client
            finally:
                app.dependency_overrides.pop(get_db_session, None)
                app.dependency_overrides.pop(get_current_user, None)

        transaction.rollback()


def test_create_goal_db(db_client):
    response = db_client.post(
        "/goals", json={'title': 'Тестовая цель', 'description': None})

    assert response.status_code == 201
    goal_id = response.json()["id"]

    response_get = db_client.get(f"/goals/{goal_id}")

    assert response_get.status_code == 200
    assert response_get.json()["title"] == "Тестовая цель"


def test_create_task_db(db_client):
    response_goal = db_client.post(
        "/goals", json={'title': 'Тестовая цель', 'description': None})

    assert response_goal.status_code == 201
    goal_id = response_goal.json()["id"]

    response_task = db_client.post(
        f"/goals/{goal_id}/tasks", json={"title": "Тестовая задача"})

    assert response_task.status_code == 201
    task_id = response_task.json()["id"]

    response_get = db_client.get(f"/goals/{goal_id}/tasks/{task_id}")

    assert response_get.status_code == 200
    assert response_get.json()["title"] == "Тестовая задача"
    assert response_get.json()["goal_id"] == goal_id
    assert response_get.json()["status_done"] is False


def test_update_delete_task_db(db_client):
    response_goal = db_client.post(
        "/goals", json={'title': 'Тестовая цель', 'description': None})

    assert response_goal.status_code == 201
    goal_id = response_goal.json()["id"]

    response_task = db_client.post(
        f"/goals/{goal_id}/tasks", json={"title": "Тестовая задача"})

    assert response_task.status_code == 201
    task_id = response_task.json()["id"]

    response_patch = db_client.patch(
        f"/goals/{goal_id}/tasks/{task_id}", json={"status_done": True})

    assert response_patch.status_code == 200
    assert response_patch.json()["status_done"] is True

    response_delete = db_client.delete(f"/goals/{goal_id}/tasks/{task_id}")

    assert response_delete.status_code == 204

    response_get = db_client.get(f"/goals/{goal_id}/tasks/{task_id}")

    assert response_get.status_code == 404
