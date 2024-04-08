import pytest
from sqlalchemy import select
from typer.testing import CliRunner

from app.cli import app as cli
from app.models import Status

runner = CliRunner()


@pytest.mark.cli
def test_list(session_factory_runner, status_db):

    result = runner.invoke(cli, ["status", "list"])

    assert result.exit_code == 0

    assert status_db.tipo in result.stdout
    assert str(status_db.id) in result.stdout


@pytest.mark.cli
def test_create(runner, session_factory_runner):

    result = runner.invoke(cli, ["status", "create", "novo"])
    assert result.exit_code == 0

    with session_factory_runner() as session:
        assert session.scalars(select(Status)).one_or_none() is not None


@pytest.mark.cli
def test_delete(runner, session_factory_runner, status_db):

    result = runner.invoke(cli, ["status", "delete", str(status_db.id)])

    assert result.exit_code == 0

    with session_factory_runner() as session:
        assert session.scalars(select(Status)).one_or_none() is None
