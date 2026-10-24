from database import engine
from sqlalchemy import select
from sqlalchemy.orm import Session

from mentorhub.orm_models import GoalORM

with Session(engine) as session:
    goal = session.scalar(select(GoalORM).where(GoalORM.title == "HTTP"))
    for member in goal.users:
        session.delete(member)
    session.delete(goal)
    session.commit()
