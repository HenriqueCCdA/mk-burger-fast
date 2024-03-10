import pytest
from sqlalchemy import select

from app.models import Meat


@pytest.mark.unit
def test_model_instance_obj(meat):

    assert meat.id is None
    assert meat.tipo == "Alcatra"
    assert meat.create_at is None
    assert meat.update_at is None


@pytest.mark.unit
def test_model_meat(meat):
    assert str(meat) == "Meat(tipo=Alcatra)"


@pytest.mark.integration
def test_model_persist_in_db(session, meat):
    session.add(meat)
    session.commit()
    session.reset()

    meat_from_db = session.scalar(select(Meat))

    assert meat_from_db is not None
    assert meat_from_db is not meat

    assert meat_from_db, id is not None
    assert meat_from_db.tipo == "Alcatra"
    assert meat_from_db.create_at is not None
    assert meat_from_db.update_at is not None
