import pytest
from app.models import Optional
from sqlalchemy import select


@pytest.mark.unit
def test_model_instance_obj(optional):

    assert optional.id is None
    assert optional.tipo == "Cebola roxa"


@pytest.mark.unit
def test_model_bread(optional):
    assert str(optional) == "Optional(tipo=Cebola roxa)"


@pytest.mark.integration
def test_model_persist_in_db(session, optional):
    session.add(optional)
    session.commit()
    session.reset()

    bread_from_db = session.scalar(select(Optional))

    assert bread_from_db is not None
    assert bread_from_db is not optional

    assert bread_from_db, id is not None
    assert bread_from_db.tipo == "Cebola roxa"
