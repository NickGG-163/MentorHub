from datetime import datetime, timezone

from sqlalchemy.orm import Session

from mentorhub.exceptions import GoalNotFoundError, TaskNotFoundError
from mentorhub.goals.goals_repository import GoalRepository
from mentorhub.orm_models import TaskORM
from mentorhub.tasks.tasks_repository import TaskRepository


class TaskService:
    def __init__(self, repository: TaskRepository, goal_repository: GoalRepository, session: Session):
        self.repository = repository
        self.session = session
        self.goal_repository = goal_repository

    def get_task(self, goal_id: int, task_id: int) -> TaskORM:
        goal = self.goal_repository.get_goal_by_id(goal_id)
        if not goal:
            raise GoalNotFoundError()
        task = self.repository.get_task_by_id(task_id)
        if not task or task.goal_id != goal_id:
            raise TaskNotFoundError()
        return task

    def create_task(self, goal_id: int, title: str) -> TaskORM:
        goal = self.goal_repository.get_goal_by_id(goal_id)
        if not goal:
            raise GoalNotFoundError()
        new_task = TaskORM(goal_id=goal.id, title=title)
        self.repository.add(new_task)
        self.session.commit()
        self.session.refresh(new_task)
        return new_task

    def update_task(self, goal_id: int, task_id: int, changes: dict) -> TaskORM:
        task = self.get_task(goal_id, task_id)
        check_status = task.status_done
        self.repository.update(task, changes)
        if check_status is False and task.status_done is True:
            task.completed_at = datetime.now(timezone.utc)
        elif check_status is True and task.status_done is False:
            task.completed_at = None
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete_task(self, goal_id: int, task_id: int) -> None:
        task = self.get_task(goal_id, task_id)
        self.repository.delete(task)
        self.session.commit()