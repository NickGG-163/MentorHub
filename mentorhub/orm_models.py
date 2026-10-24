from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Identity,
    PrimaryKeyConstraint,
    Text,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    configure_mappers,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    pass


class GoalORM(Base):
    __tablename__ = "goals"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    title: Mapped[str] = mapped_column(Text, unique=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    tasks: Mapped[list["TaskORM"]] = relationship(back_populates="goal")
    users: Mapped[list["GoalMemberORM"]] = relationship(back_populates="goal")


class TaskORM(Base):
    __tablename__ = "tasks"
    __table_args__ = (UniqueConstraint("goal_id", "title"),)

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    status_done: Mapped[bool] = mapped_column(
        nullable=False, default=False, server_default=text("False")
    )
    goal_id: Mapped[int] = mapped_column(ForeignKey("goals.id"), nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    goal: Mapped["GoalORM"] = relationship(back_populates="tasks")


class UserORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)

    goals: Mapped[list["GoalMemberORM"]] = relationship(back_populates="user")


class GoalMemberORM(Base):
    __tablename__ = "goal_members"
    __table_args__ = (PrimaryKeyConstraint("user_id", "goal_id"),)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    goal_id: Mapped[int] = mapped_column(ForeignKey("goals.id"))

    user: Mapped["UserORM"] = relationship(back_populates="goals")
    goal: Mapped["GoalORM"] = relationship(back_populates="users")


configure_mappers()
