from sqlalchemy.orm import Session

from mentorhub.goals.goals_repository import GoalRepository
from mentorhub.orm_models import GoalMemberORM, GoalORM


class GoalService:
    def __init__(self, repository: GoalRepository, session: Session):
        self.repository = repository
        self.session = session

    def get_goal(self, goal_id: int) -> GoalORM | None:
        goal = self.repository.get_goal_by_id(goal_id)
        return goal

    def create_goal(self, title: str, description: str | None, user_id: int) -> GoalORM:
        new_goal = GoalORM(title=title, description=description)
        self.repository.add(new_goal)
        self.session.flush()
        goal_member = GoalMemberORM(goal_id=new_goal.id, user_id=user_id)
        self.repository.add_member(goal_member)
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

    def user_has_access(self, goal_id: int, user_id: int) -> bool:
        res = self.repository.user_has_access(goal_id, user_id)
        return res