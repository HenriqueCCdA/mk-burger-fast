import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.conf import settings
from app.db import get_session
from app.main import app
from app.models import Base, Bread, Burger, Meat, Optional, Status


@pytest.fixture
def session():
    engine = create_engine(f"{settings.DATABASE_URL}_test", echo=settings.ECHO)
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    with Session() as session:
        yield session
        session.rollback()
    Base.metadata.drop_all(engine)


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def bread():
    return Bread(tipo="Integral")


@pytest.fixture
def meat():
    return Meat(tipo="Alcatra")


@pytest.fixture
def optional():
    return Optional(tipo="Cebola roxa")


@pytest.fixture
def status():
    return Status(tipo="Solicitado")


@pytest.fixture
def status_list(session):
    list_ = [
        Status(tipo="Solicitado"),
        Status(tipo="Em produção"),
    ]

    session.add_all(list_)
    session.commit()

    return list_


@pytest.fixture
def burger(session, bread, meat, optional, status):

    session.add_all([bread, meat, optional, status])
    session.commit()

    return Burger(name="João", meat_id=meat.id, bread_id=bread.id, optional_id=optional.id, status_id=status.id)
