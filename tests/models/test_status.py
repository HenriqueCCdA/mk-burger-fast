import pytest
from sqlalchemy import select

from app.models import Status


@pytest.mark.unit
def test_model_instance_obj(status):

    assert status.id is None
    assert status.tipo == "Solicitado"
    assert status.created_at is None
    assert status.updated_at is None


@pytest.mark.unit
def test_model_status(status):
    assert str(status) == "Status(tipo=Solicitado)"


@pytest.mark.integration
def test_model_persist_in_db(session, status):
    session.add(status)
    session.commit()
    session.reset()

    status_from_db = session.scalar(select(Status))

    assert status_from_db is not None
    assert status_from_db is not status

    assert status_from_db, id is not None
    assert status_from_db.tipo == "Solicitado"

    assert status_from_db.created_at is not None
    assert status_from_db.updated_at is not None
