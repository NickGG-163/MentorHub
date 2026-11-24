from sqlalchemy.orm import Session

from mentorhub.orm_models import TaskORM


class TaskRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_task_by_id(self, task_id: int) -> TaskORM | None:
        task = self.session.get(TaskORM, task_id)
        return task

    def add(self, task: TaskORM) -> None:
        self.session.add(task)

    def update(self, task: TaskORM, changes: dict) -> None:
        for key, value in changes.items():
            setattr(task, key, value)

    def delete(self, task: TaskORM) -> None:
        self.session.delete(task)
