from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.conf import settings

engine = create_engine(url=settings.DATABASE_URL, echo=settings.ECHO)

SessionFactory = sessionmaker(engine)


def get_session():
    with SessionFactory() as session:
        yield session


ActiveSession = Annotated[Session, Depends(get_session)]
