from sqlalchemy import select
from sqlalchemy.orm import Session

from mentorhub.orm_models import GoalMemberORM, GoalORM


class GoalRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_goal_by_id(self, goal_id: int) -> GoalORM | None:
        goal = self.session.get(GoalORM, goal_id)
        return goal

    def add(self, goal: GoalORM) -> None:
        self.session.add(goal)

    def update(self, goal: GoalORM, changes: dict) -> None:
        for key, value in changes.items():
            setattr(goal, key, value)

    def delete(self, goal: GoalORM) -> None:
        self.session.delete(goal)

    def user_has_access(self, goal_id: int, user_id: int) -> bool:
        res = select(GoalMemberORM).where(GoalMemberORM.goal_id ==
                                          goal_id, GoalMemberORM.user_id == user_id)
        return self.session.scalar(res) is not None

    def add_member(self, goal_member: GoalMemberORM) -> None:
        self.session.add(goal_member)
