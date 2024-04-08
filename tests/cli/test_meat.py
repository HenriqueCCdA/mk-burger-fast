import pytest
from sqlalchemy import select

from app.cli import app as cli
from app.models import Meat


@pytest.fixture
def session_factory_runner(mocker, session):
    return mocker.patch("app.cli.meat.SessionFactory", return_value=session)


@pytest.mark.cli
def test_list(runner, session_factory_runner, meat_db):

    result = runner.invoke(cli, ["meat", "list"])

    assert result.exit_code == 0

    assert meat_db.tipo in result.stdout
    assert str(meat_db.id) in result.stdout


@pytest.mark.cli
def test_create(runner, session_factory_runner):

    result = runner.invoke(cli, ["meat", "create", "novo"])
    assert result.exit_code == 0

    with session_factory_runner() as session:
        assert session.scalars(select(Meat)).one_or_none() is not None


@pytest.mark.cli
def test_delete(runner, session_factory_runner, meat_db):

    result = runner.invoke(cli, ["meat", "delete", str(meat_db.id)])

    assert result.exit_code == 0

    with session_factory_runner() as session:
        assert session.scalars(select(Meat)).one_or_none() is None
