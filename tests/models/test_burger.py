import pytest
from sqlalchemy import select

from app.models import Burger


@pytest.mark.unit
def test_model_instance_obj(burger):

    assert burger.id is None
    assert burger.meat_id is not None
    assert burger.bread_id is not None
    assert burger.status_id is not None
    assert burger.optional_id is not None

    assert burger.name == "João"
    assert burger.bread is None
    assert burger.meat is None
    assert burger.optional is None
    assert burger.status is None


@pytest.mark.unit
def test_model_burger_repr(session, burger):
    assert str(burger) == "Burger(name=João)"


@pytest.mark.integration
def test_model_persist_in_db(session, burger):
    session.add(burger)
    session.commit()
    session.reset()

    burger_from_db = session.scalar(select(Burger))

    assert burger_from_db is not None
    assert burger_from_db is not burger

    assert burger_from_db is not None
    assert burger_from_db.name == "João"
    assert burger_from_db.bread.tipo == "Integral"
    assert burger_from_db.meat.tipo == "Alcatra"
    assert burger_from_db.optional.tipo == "Cebola roxa"
    assert burger_from_db.status.tipo == "Solicitado"


@pytest.mark.integration
def test_model_relationship(session, bread, meat, optional, status):

    session.add_all([bread, meat, optional, status])
    session.commit()

    b1 = Burger(name="João", meat_id=meat.id, bread_id=bread.id, optional_id=optional.id, status_id=status.id)
    b2 = Burger(name="Maria", meat_id=meat.id, bread_id=bread.id, optional_id=optional.id, status_id=status.id)

    session.add_all([b1, b2])
    session.commit()

    assert len(bread.burgers) == 2
    assert len(meat.burgers) == 2
    assert len(optional.burgers) == 2
    assert len(status.burgers) == 2

    assert bread.burgers[0].id == b1.id
    assert bread.burgers[1].id == b2.id

    assert meat.burgers[0].id == b1.id
    assert meat.burgers[1].id == b2.id

    assert optional.burgers[0].id == b1.id
    assert optional.burgers[1].id == b2.id

    assert status.burgers[0].id == b1.id
    assert status.burgers[1].id == b2.id
