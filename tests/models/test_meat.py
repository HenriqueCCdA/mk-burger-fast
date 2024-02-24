import pytest
from sqlalchemy import select

from app.models import Meat


@pytest.mark.unit
def test_model_instance_obj(meat):

    assert meat.id is None
    assert meat.tipo == "Alcatra"


@pytest.mark.unit
def test_model_bread(meat):
    assert str(meat) == "Meat(tipo=Alcatra)"


@pytest.mark.integration
def test_model_persist_in_db(session, meat):
    session.add(meat)
    session.commit()
    session.reset()

    bread_from_db = session.scalar(select(Meat))

    assert bread_from_db is not None
    assert bread_from_db is not meat

    assert bread_from_db, id is not None
    assert bread_from_db.tipo == "Alcatra"
