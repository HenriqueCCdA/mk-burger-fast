import pytest
from sqlalchemy import select

from app.models import Optional


@pytest.mark.unit
def test_model_instance_obj(optional):

    assert optional.id is None
    assert optional.tipo == "Cebola roxa"
    assert optional.created_at is None
    assert optional.updated_at is None


@pytest.mark.unit
def test_model_bread(optional):
    assert str(optional) == "Optional(tipo=Cebola roxa)"


@pytest.mark.integration
def test_model_persist_in_db(session, optional):
    session.add(optional)
    session.commit()
    session.reset()

    optional_from_db = session.scalar(select(Optional))

    assert optional_from_db is not None
    assert optional_from_db is not optional

    assert optional_from_db, id is not None
    assert optional_from_db.tipo == "Cebola roxa"
    assert optional_from_db.created_at is not None
    assert optional_from_db.updated_at is not None
