from typing import Any

from pydantic import BaseModel, EmailStr, Field, field_validator


class GoalCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100, description='Имя цели')
    description: str | None = Field(
        max_length=500, description='Описание цели', default=None)

    @field_validator("title", mode='before')
    @classmethod
    def normalize_title(cls, value: Any) -> Any:
        if isinstance(value, str):
            return value.strip()
        return value


class GoalUpdate(BaseModel):
    title: str | None = Field(
        default=None, min_length=3, max_length=100, description='Имя цели')
    description: str | None = Field(
        max_length=500, description='Описание цели', default=None)

    @field_validator("title", mode='before')
    @classmethod
    def normalize_title(cls, value: Any) -> Any:
        if value is None:
            raise ValueError('Название цели не может быть пустым')
        if isinstance(value, str):
            return value.strip()
        return value


class GoalResponse(BaseModel):
    id: int
    title: str
    description: str | None = None


class ErrorInfo(BaseModel):
    code: str
    message: str
    details: list[dict[str, Any]]


class ErrorEnvelope(BaseModel):
    error: ErrorInfo


class TaskCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100, description='Имя задачи')

    @field_validator("title", mode='before')
    @classmethod
    def normalize_title(cls, value: Any) -> Any:
        if isinstance(value, str):
            return value.strip()
        return value


class TaskResponse(BaseModel):
    id: int
    goal_id: int
    title: str
    status_done: bool


class TaskUpdate(BaseModel):
    title: str | None = Field(
        default=None, min_length=3, max_length=100, description='Имя задачи')
    status_done: bool | None = None

    @field_validator("title", mode='before')
    @classmethod
    def normalize_title(cls, value: Any) -> Any:
        if value is None:
            raise ValueError("Название задачи не может быть null")
        if isinstance(value, str):
            return value.strip()
        return value

    @field_validator("status_done", mode="before")
    @classmethod
    def validate_status(cls, value: Any) -> Any:
        if value is None:
            raise ValueError("Статус задачи не может быть null")
        return value


class UserRegister(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserResponse(BaseModel):
    id: int
    name: str
    email: str


class UserLogin(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"