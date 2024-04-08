import pytest
from sqlalchemy import select

from app.cli import app as cli
from app.models import Bread


@pytest.mark.cli
def test_list(runner, session_factory_runner, bread_db):

    result = runner.invoke(cli, ["bread", "list"])

    assert result.exit_code == 0

    assert bread_db.tipo in result.stdout
    assert str(bread_db.id) in result.stdout


@pytest.mark.cli
def test_create(runner, session_factory_runner):

    result = runner.invoke(cli, ["bread", "create", "novo"])
    assert result.exit_code == 0

    with session_factory_runner() as session:
        assert session.scalars(select(Bread)).one_or_none() is not None


@pytest.mark.cli
def test_delete(runner, session_factory_runner, bread_db):

    result = runner.invoke(cli, ["bread", "delete", str(bread_db.id)])

    assert result.exit_code == 0

    with session_factory_runner() as session:
        assert session.scalars(select(Bread)).one_or_none() is None
