from sqlalchemy.orm import Session
from mentorhub.api_schemas import GoalCreate
from mentorhub.goals_repository import GoalRepository
from mentorhub.orm_models import GoalORM


class GoalService:
    def __init__(self, repository: GoalRepository, session: Session):
        self.repository = repository
        self.session = session

    def get_goal(self, goal_id: int) -> GoalORM | None:
        goal = self.repository.get_goal_by_id(goal_id)
        return goal

    def create_goal(self, title: str, description: str | None) -> GoalORM:
        new_goal = GoalORM(title=title, description=description)
        self.repository.add(new_goal)
        self.session.commit()
        self.session.refresh(new_goal)
        return new_goal

    def update_goal(self, goal: GoalORM, changes: dict) -> GoalORM:
        self.repository.update(goal, changes)
        self.session.commit()
        self.session.refresh(goal)
        return goal

    def delete_goal(self, goal: GoalORM) -> None:
        self.repository.delete(goal)
        self.session.commit()
