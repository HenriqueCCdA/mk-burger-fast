import pytest
from sqlalchemy import select

from app.cli import app as cli
from app.models import Optional


@pytest.fixture
def session_factory_runner(mocker, session):
    return mocker.patch("app.cli.optional.SessionFactory", return_value=session)


@pytest.mark.cli
def test_list(runner, session_factory_runner, optional_db):

    result = runner.invoke(cli, ["optional", "list"])

    assert result.exit_code == 0

    assert optional_db.tipo in result.stdout
    assert str(optional_db.id) in result.stdout


@pytest.mark.cli
def test_create(runner, session_factory_runner):

    result = runner.invoke(cli, ["optional", "create", "novo"])
    assert result.exit_code == 0

    with session_factory_runner() as session:
        assert session.scalars(select(Optional)).one_or_none() is not None


@pytest.mark.cli
def test_delete(runner, session_factory_runner, optional_db):

    result = runner.invoke(cli, ["optional", "delete", str(optional_db.id)])

    assert result.exit_code == 0

    with session_factory_runner() as session:
        assert session.scalars(select(Optional)).one_or_none() is None
