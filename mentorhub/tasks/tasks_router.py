from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from mentorhub.api_schemas import TaskCreate, TaskResponse, TaskUpdate
from mentorhub.database import get_db_session
from mentorhub.exceptions import GoalNotFoundError, TaskNotFoundError
from mentorhub.goals.goals_repository import GoalRepository
from mentorhub.goals.goals_router import goal_availability
from mentorhub.tasks.tasks_repository import TaskRepository
from mentorhub.tasks.tasks_service import TaskService

router_tasks = APIRouter(
    prefix='/goals/{goal_id}/tasks', tags=['tasks'], dependencies=[Depends(goal_availability)])


def get_task_service(session: Annotated[Session, Depends(get_db_session)]) -> TaskService:
    repository = TaskRepository(session)
    goal_repository = GoalRepository(session)
    service = TaskService(repository, goal_repository, session)
    return service


@router_tasks.get("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def get_task(goal_id: int, task_id: int, service: Annotated[TaskService, Depends(get_task_service)]) -> TaskResponse:
    try:
        task = service.get_task(goal_id, task_id)
        return TaskResponse(id=task.id, goal_id=task.goal_id, title=task.title, status_done=task.status_done)
    except GoalNotFoundError:
        raise HTTPException(status_code=404, detail='Цель не найдена')
    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail='Задача не найдена')


@router_tasks.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def post_tasks(goal_id: int, task: TaskCreate, service: Annotated[TaskService, Depends(get_task_service)]) -> TaskResponse:
    try:
        new_task = service.create_task(goal_id=goal_id, title=task.title)
        return TaskResponse(id=new_task.id, goal_id=new_task.goal_id, title=new_task.title, status_done=new_task.status_done)
    except GoalNotFoundError:
        raise HTTPException(status_code=404, detail='Цель не найдена')


@router_tasks.patch("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_200_OK)
def update_task(goal_id: int, task_id: int, task_update: TaskUpdate, service: Annotated[TaskService, Depends(get_task_service)]) -> TaskResponse:
    try:
        changes = task_update.model_dump(exclude_unset=True)
        new_task = service.update_task(goal_id, task_id, changes)
        return TaskResponse(id=new_task.id, goal_id=new_task.goal_id, title=new_task.title, status_done=new_task.status_done)
    except GoalNotFoundError:
        raise HTTPException(status_code=404, detail='Цель не найдена')
    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail='Задача не найдена')


@router_tasks.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(goal_id: int, task_id: int, service: Annotated[TaskService, Depends(get_task_service)]) -> None:
    try:
        service.delete_task(goal_id, task_id)
    except GoalNotFoundError:
        raise HTTPException(status_code=404, detail='Цель не найдена')
    except TaskNotFoundError:
        raise HTTPException(status_code=404, detail='Задача не найдена')
