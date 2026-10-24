from database import engine
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from mentorhub.orm_models import GoalORM

with Session(engine) as session:
    goals = session.scalars(select(GoalORM).options(selectinload(GoalORM.tasks))).all()
    for goal in goals:
        print(goal.title)
        for task in goal.tasks:
            print(task.title)
