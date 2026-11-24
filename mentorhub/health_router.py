from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from mentorhub.database import get_db_session

router_health = APIRouter(prefix='/health', tags=['health'])


@router_health.get('')
async def check_health():
    return {'status': 'ok'}


@router_health.get('/db')
def check_db_health(session: Annotated[Session, Depends(get_db_session)]):
    res = session.scalar(select(1))
    return {'status': 'ok', 'res': res}
