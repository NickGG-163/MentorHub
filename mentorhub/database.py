import os

from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

database_url = os.getenv("DATABASE_URL", "postgresql+psycopg:///mentorhub")

engine = create_engine(database_url, echo=True)


def get_db_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session
