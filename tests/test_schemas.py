import pytest

from app.schemas import BaseItemOut, IngredientsOut, StatusOut


@pytest.mark.unit
def test_base_item():

    status = BaseItemOut(id=2, tipo="Item genêrico")

    assert status.id == 2
    assert status.tipo == "Item genêrico"


@pytest.mark.unit
def test_status():

    status = StatusOut(id=1, tipo="Em produção")

    assert status.id == 1
    assert status.tipo == "Em produção"


@pytest.mark.unit
def test_indredientes():

    ingredientes = IngredientsOut(
        paes=[
            {"id": 2, "tipo": "3 Queijos"},
            {"id": 4, "tipo": "Integral"},
        ],
        carnes=[
            {"id": 4, "tipo": "Veggie burger"},
        ],
        opcionais=[{"id": 6, "tipo": "Pepino"}, {"id": 3, "tipo": "Salame"}, {"id": 4, "tipo": "Tomate"}],
    )

    assert len(ingredientes.paes) == 2
    assert len(ingredientes.carnes) == 1
    assert len(ingredientes.opcionais) == 3

    assert ingredientes.paes[0] == BaseItemOut(id=2, tipo="3 Queijos")
    assert ingredientes.carnes[0] == BaseItemOut(id=4, tipo="Veggie burger")
    assert ingredientes.opcionais[0] == BaseItemOut(id=6, tipo="Pepino")
