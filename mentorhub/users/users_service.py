from sqlalchemy.orm import Session

from mentorhub.exceptions import InvalidCredentialsError, UserAlreadyExistsError
from mentorhub.orm_models import UserORM
from mentorhub.security import create_access_token, hash_password, verify_password
from mentorhub.users.users_repository import UserRepository


class UserService:
    def __init__(self, session: Session, repository: UserRepository):
        self.session = session
        self.repository = repository

    def register_user(self, name: str, email: str, password: str) -> UserORM:
        user = self.repository.get_by_email(email)
        if user:
            raise UserAlreadyExistsError()
        hashed = hash_password(password)
        new_user = UserORM(name=name, email=email, password_hash=hashed)
        self.repository.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user

    def authenticate_user(self, email: str, password: str) -> str:
        user = self.repository.get_by_email(email)
        if not user or not user.password_hash:
            raise InvalidCredentialsError()
        if not verify_password(password, user.password_hash):
            raise InvalidCredentialsError()
        token = create_access_token(user.id)
        return token

    def get_user_by_id(self, user_id: int) -> UserORM:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise InvalidCredentialsError()
        return user
