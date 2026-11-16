from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine("postgresql+psycopg:///mentorhub", echo=True)


def get_db_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session
