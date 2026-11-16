from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from mentorhub.api_schemas import ErrorEnvelope, GoalCreate, GoalResponse, GoalUpdate
from mentorhub.database import get_db_session
from mentorhub.goals_repository import GoalRepository
from mentorhub.goals_service import GoalService
from mentorhub.orm_models import GoalORM

router_goals = APIRouter(prefix='/goals', tags=['goals'])


def get_goal_service(session: Annotated[Session, Depends(get_db_session)]) -> GoalService:
    repository = GoalRepository(session)
    service = GoalService(repository, session)
    return service


def goal_availability(goal_id: int, service: Annotated[GoalService, Depends(get_goal_service)]) -> GoalORM:
    goal = service.get_goal(goal_id)
    if not goal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Цель не найдена')
    return goal


@router_goals.post("", response_model=GoalResponse, status_code=status.HTTP_201_CREATED)
def post_goals(goal: GoalCreate, service: Annotated[GoalService, Depends(get_goal_service)]) -> GoalResponse:
    new_goal = service.create_goal(goal.title, goal.description)
    return GoalResponse(id=new_goal.id, title=new_goal.title, description=new_goal.description)


@router_goals.get("/{goal_id}", response_model=GoalResponse, responses={404: {"model": ErrorEnvelope, "description": "Цель не найдена"},
                                                                        422: {"model": ErrorEnvelope, "description": "Некорректный ID цели"}})
def get_goal(goal: Annotated[GoalORM, Depends(goal_availability)]) -> GoalResponse:
    return {'id': goal.id, 'title': goal.title, 'description': goal.description}


@router_goals.patch("/{goal_id}")
def goal_update(goal_update: GoalUpdate, goal: Annotated[GoalORM, Depends(goal_availability)], service: Annotated[GoalService, Depends(get_goal_service)]) -> GoalResponse:
    changes = goal_update.model_dump(exclude_unset=True)
    new_goal = service.update_goal(goal, changes)
    return GoalResponse(id=new_goal.id, title=new_goal.title, description=new_goal.description)


@router_goals.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
def goal_delete(goal: Annotated[GoalORM, Depends(goal_availability)], service: Annotated[GoalService, Depends(get_goal_service)]) -> None:
    service.delete_goal(goal)
