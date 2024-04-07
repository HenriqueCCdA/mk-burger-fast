import pytest
from typer.testing import CliRunner

from app.cli import app

runner = CliRunner()


@pytest.mark.cli
def test_list():

    result = runner.invoke(app, ["status", "list"])

    assert result.exit_code == 0
