from typing import Any

from pydantic import BaseModel, Field, field_validator


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
