from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from mentorhub.exceptions import InvalidCredentialsError
from mentorhub.orm_models import UserORM
from mentorhub.security import decode_access_token
from mentorhub.users.users_dependencies import UserService, get_user_service

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
                     service: Annotated[UserService, Depends(get_user_service)]) -> UserORM:
    if not credentials:
        raise HTTPException(status_code=401, detail="Токен отсутствует")
    try:
        user_id = decode_access_token(credentials.credentials)
        user = service.get_user_by_id(user_id)
        return user
    except (jwt.InvalidTokenError, ValueError, InvalidCredentialsError):
        raise HTTPException(status_code=401, detail="Недействительный токен")
