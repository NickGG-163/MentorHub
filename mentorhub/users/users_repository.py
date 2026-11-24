from sqlalchemy import select
from sqlalchemy.orm import Session

from mentorhub.orm_models import UserORM


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_email(self, email: str) -> UserORM | None:
        req = select(UserORM).where(UserORM.email == email)
        user = self.session.scalar(req)
        return user

    def add(self, user: UserORM) -> None:
        self.session.add(user)

    def get_by_id(self, user_id: int) -> UserORM | None:
        user = self.session.get(UserORM, user_id)
        return user