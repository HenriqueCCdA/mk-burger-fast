import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.conf import settings
from app.models import Base
from typer.testing import CliRunner
import app.db


@pytest.fixture
def session_runner(mocker):
    engine = create_engine(f"{settings.DATABASE_URL}_test", echo=settings.ECHO)
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)

    session = Session()
    yield mocker.patch.object(app.db, "SessionFactory", autospec=True, return_value=session)
    session.close()

    Base.metadata.drop_all(engine)

@pytest.fixture
def runner():
    return CliRunner()
