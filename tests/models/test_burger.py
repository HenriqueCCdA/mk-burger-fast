import pytest
from sqlalchemy import select

from app.models import Bread, Burger, Meat, Optional, Status


@pytest.mark.unit
def test_model_instance_obj(burger):

    assert burger.id is None
    assert burger.meat_id is not None
    assert burger.bread_id is not None
    assert burger.status_id is not None

    assert burger.name == "João"
    assert len(burger.optionals) == 1

    assert burger.created_at is None
    assert burger.updated_at is None


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
    assert burger_from_db.optionals[0].tipo == "Cebola roxa"
    assert burger_from_db.status.tipo == "Solicitado"

    assert burger_from_db.created_at is not None
    assert burger_from_db.updated_at is not None


@pytest.mark.integration
def test_model_relationship(session, bread, meat, optional, status):

    session.add_all([bread, meat, optional, status])
    session.commit()

    b1 = Burger(name="João", meat_id=meat.id, bread_id=bread.id, status_id=status.id)
    b2 = Burger(name="Maria", meat_id=meat.id, bread_id=bread.id, status_id=status.id)

    b1.optionals.append(optional)
    b2.optionals.append(optional)

    session.add_all([b1, b2])
    session.commit()
    session.reset()

    bread_from_db = session.scalar(select(Bread))
    meat_from_db = session.scalar(select(Meat))
    optionals_from_db = session.scalars(select(Optional)).one()
    status_from_db = session.scalar(select(Status))

    burgers_from_db = session.scalars(select(Burger)).all()

    assert len(bread_from_db.burgers) == 2
    assert len(meat_from_db.burgers) == 2
    assert len(optionals_from_db.burgers) == 2
    assert len(status_from_db.burgers) == 2
    assert set(bread_from_db.burgers) == set(burgers_from_db)
    assert set(meat_from_db.burgers) == set(burgers_from_db)
    assert set(optionals_from_db.burgers) == set(burgers_from_db)
    assert set(status_from_db.burgers) == set(burgers_from_db)

    assert burgers_from_db[0].optionals[0] == optionals_from_db
    assert burgers_from_db[1].optionals[0] == optionals_from_db
