import pytest
from app.cli import app as cli


@pytest.mark.cli
def test_list(runner, session_runner):

    result = runner.invoke(cli, ["bread", "list"])

    assert result.exit_code == 0


# @pytest.mark.cli
# def test_create(runner, session_runner):

#     result = runner.invoke(cli, ["bread", "create", "novo"])

#     assert result.exit_code == 0


# @pytest.mark.cli
# def test_delete(runner, session_runner, bread_db):
#     result = runner.invoke(cli, ["bread", "delete", str(bread_db.id)])

#     assert result.exit_code == 0
