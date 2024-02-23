import pytest
from app.conf import settings
from app.models import Base, Bread, Burger, Meat, Optional, Status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


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
def burger(session, bread, meat, optional, status):

    session.add_all([bread, meat, optional, status])
    session.commit()

    return Burger(name="João", meat_id=meat.id, bread_id=bread.id, optional_id=optional.id, status_id=status.id)
