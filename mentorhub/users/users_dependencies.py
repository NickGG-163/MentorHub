from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from mentorhub.database import get_db_session
from mentorhub.users.users_repository import UserRepository
from mentorhub.users.users_service import UserService


def get_user_service(session: Annotated[Session, Depends(get_db_session)]) -> UserService:
    repository = UserRepository(session)
    service = UserService(session, repository)
    return service
