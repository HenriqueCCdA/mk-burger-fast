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
def bread_db(session, bread):

    session.add(bread)
    session.commit()

    return bread


@pytest.fixture
def meat():
    return Meat(tipo="Alcatra")


@pytest.fixture
def meat_db(session, meat):

    session.add(meat)
    session.commit()

    return meat


@pytest.fixture
def optional():
    return Optional(tipo="Cebola roxa")


@pytest.fixture
def optional_list(session):

    list_ = [
        Optional(tipo="Cebola roxa"),
        Optional(tipo="Cebola roxa"),
    ]

    session.add_all(list_)
    session.commit()

    return list_


@pytest.fixture
def status():
    return Status(tipo="Solicitado")


@pytest.fixture
def status_db(session, status):

    session.add(status)
    session.commit()

    return status


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
def burger_list(session):

    bread = Bread(tipo="Integral")
    meat = Meat(tipo="Alcatra")
    optional1 = Optional(tipo="Cebola roxa")
    optional2 = Optional(tipo="Bacon")
    status = Status(tipo="Solicitado")

    session.add_all([bread, meat, optional1, optional2, status])
    session.commit()

    b1 = Burger(name="João", meat_id=meat.id, bread_id=bread.id, status_id=status.id)
    b1.optionals.extend([optional1, optional2])
    b2 = Burger(name="Maria", meat_id=meat.id, bread_id=bread.id, status_id=status.id)
    b2.optionals.append(optional1)

    list_ = [b1, b2]

    session.add_all(list_)
    session.commit()

    return list_


@pytest.fixture
def ingredients(session):

    obj1 = Bread(tipo="Integral")
    obj2 = Meat(tipo="Alcatra")
    obj3 = Meat(tipo="Maminha")
    obj4 = Optional(tipo="Cebola roxa")

    session.add_all([obj1, obj2, obj3, obj4])
    session.commit()

    return {"breads": [obj1], "meats": [obj2, obj3], "optionals": [obj4]}


@pytest.fixture
def burger(session, bread, meat, optional, status):

    session.add_all([bread, meat, optional, status])
    session.commit()

    burger = Burger(name="João", meat_id=meat.id, bread_id=bread.id, status_id=status.id)
    burger.optionals.append(optional)

    return burger


@pytest.fixture
def burger_db(session, burger):

    session.add(burger)
    session.commit()

    return burger


@pytest.fixture
def payload_create(session):

    bread = Bread(tipo="Integral")
    meat = Meat(tipo="Alcatra")
    optional1 = Optional(tipo="Cebola roxa")
    optional2 = Optional(tipo="Bacon")
    status = Status(tipo="Solicitado")

    session.add_all([bread, meat, optional1, optional2, status])
    session.commit()

    payload = {
        "nome": "João",
        "carne": meat.id,
        "pao": bread.id,
        "status": status.id,
        "opcionais": [optional1.id, optional2.id],
    }

    return payload
