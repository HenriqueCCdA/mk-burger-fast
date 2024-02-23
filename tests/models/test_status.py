import pytest
from app.models import Status
from sqlalchemy import select


@pytest.mark.unit
def test_model_instance_obj(status):

    assert status.id is None
    assert status.tipo == "Solicitado"


@pytest.mark.unit
def test_model_bread(status):
    assert str(status) == "Status(tipo=Solicitado)"


@pytest.mark.integration
def test_model_persist_in_db(session, status):
    session.add(status)
    session.commit()
    session.reset()

    bread_from_db = session.scalar(select(Status))

    assert bread_from_db is not None
    assert bread_from_db is not status

    assert bread_from_db, id is not None
    assert bread_from_db.tipo == "Solicitado"
