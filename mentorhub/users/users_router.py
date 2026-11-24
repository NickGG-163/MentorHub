from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from mentorhub.api_schemas import TokenResponse, UserLogin, UserRegister, UserResponse
from mentorhub.auth_dependencies import get_current_user
from mentorhub.exceptions import InvalidCredentialsError, UserAlreadyExistsError
from mentorhub.orm_models import UserORM
from mentorhub.users.users_dependencies import get_user_service
from mentorhub.users.users_service import UserService

router_users = APIRouter(prefix='/auth', tags=['auth'])


@router_users.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_users(user: UserRegister, service: Annotated[UserService, Depends(get_user_service)]) -> UserResponse:
    try:
        new_user = service.register_user(
            name=user.name, email=user.email, password=user.password)
        return UserResponse(id=new_user.id, name=new_user.name, email=new_user.email)
    except UserAlreadyExistsError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="Пользователь с данным email уже существует")


@router_users.post("/login", response_model=TokenResponse)
def login_users(user: UserLogin, service: Annotated[UserService, Depends(get_user_service)]) -> TokenResponse:
    try:
        token = service.authenticate_user(
            email=user.email, password=user.password)
        return TokenResponse(access_token=token)
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный email или пароль")


@router_users.get("/me", response_model=UserResponse)
def get_me(current_user: Annotated[UserORM, Depends(get_current_user)]) -> UserResponse:
    return UserResponse(id=current_user.id, name=current_user.name, email=current_user.email)
