import pytest
from app.models import PlaceHolderModel
from sqlalchemy import select


@pytest.mark.unit
def test_model_instance_obj():
    obj = PlaceHolderModel(field="name")

    assert obj.id is None
    assert obj.field == "name"


@pytest.mark.unit
def test_model_repr():
    obj = PlaceHolderModel(field="name")
    assert str(obj) == "PlaceHolderModel(field=name)"


@pytest.mark.integration
def test_model_persist_in_db(session):
    obj = PlaceHolderModel(field="name")

    session.add(obj)
    session.commit()
    session.reset()

    obj_from_db = session.scalar(select(PlaceHolderModel).where(PlaceHolderModel.field == "name"))

    assert obj_from_db is not None
    assert obj_from_db is not obj

    assert obj_from_db, id is not None
    assert obj_from_db.field == "name"
