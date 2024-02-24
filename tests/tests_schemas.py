from app.schemas import StatusOut


def test_schemas_status():

    status = StatusOut(id=1, tipo="Em produção")

    assert status.id == 1
    assert status.tipo == "Em produção"
