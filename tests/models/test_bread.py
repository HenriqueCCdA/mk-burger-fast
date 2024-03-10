import pytest
from sqlalchemy import select

from app.models import Bread


@pytest.mark.unit
def test_model_instance_obj(bread):
    assert bread.id is None
    assert bread.tipo == "Integral"
    assert bread.create_at is None
    assert bread.update_at is None


@pytest.mark.unit
def test_model_bread(bread):
    assert str(bread) == "Bread(tipo=Integral)"


@pytest.mark.integration
def test_model_persist_in_db(session, bread):

    session.add(bread)
    session.commit()
    session.reset()

    bread_from_db = session.scalar(select(Bread))

    assert bread_from_db is not None
    assert bread_from_db is not bread

    assert bread_from_db, id is not None
    assert bread_from_db.tipo == "Integral"
    assert bread_from_db.create_at is not None
    assert bread_from_db.update_at is not None
