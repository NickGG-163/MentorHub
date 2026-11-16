from sqlalchemy.orm import Session
from mentorhub.orm_models import GoalORM


class GoalRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_goal_by_id(self, goal_id: int) -> GoalORM | None:
        goal = self.session.get(GoalORM, goal_id)
        return goal

    def add(self, goal: GoalORM) -> None:
        self.session.add(goal)
        return

    def update(self, goal: GoalORM, changes: dict):
        for key, value in changes.items():
            setattr(goal, key, value)

    def delete(self, goal: GoalORM):
        self.session.delete(goal)
