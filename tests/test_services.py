import pytest
from sqlalchemy import func, select

from app.models import Bread, Burger, Meat, Status
from app.schemas import BurgerIn
from app.service import (
    CreatBurgerService,
    InvalidIgredients,
    InvalidOptionals,
)


@pytest.mark.unit
def test_positive_meat_get_infos_in_db(session, meat_db):
    obj = CreatBurgerService(session).get_infos_in_db(Meat, 1)
    assert obj is meat_db


@pytest.mark.unit
def test_positive_bread_get_infos_in_db(session, bread_db):
    obj = CreatBurgerService(session).get_infos_in_db(Bread, 1)
    assert obj is bread_db


@pytest.mark.unit
def test_positive_status_get_infos_in_db(session, status_db):
    obj = CreatBurgerService(session).get_infos_in_db(Status, 1)
    assert obj is status_db


@pytest.mark.unit
@pytest.mark.parametrize(
    "Model, msg",
    [
        (Meat, "Carne com id '1' não existe."),
        (Bread, "Pao com id '1' não existe."),
        (Status, "Status com id '1' não existe."),
    ],
    ids=[
        "Carne",
        "Pao",
        "Status",
    ],
)
def test_negative_bread_get_infos_in_db(session, Model, msg):

    with pytest.raises(InvalidIgredients, match=msg):
        CreatBurgerService(session).get_infos_in_db(Model, 1)


@pytest.mark.unit
def test_positive_get_optionals_in_db(session, optional_list):

    objs = CreatBurgerService(session).get_optionals_in_db([1, 2])

    assert set(objs) == set(optional_list)


@pytest.mark.unit
def test_negative_get_optionals_in_db(session, optional_list):

    msg = "Opcional com id '4' não existe."
    with pytest.raises(InvalidOptionals, match=msg):
        CreatBurgerService(session).get_optionals_in_db([1, 2, 4])


@pytest.mark.unit
def test_positive_get_buger_infos_in_db(session, meat_db, bread_db, status_db, optional_list):

    burger = BurgerIn(nome="João", pao=1, carne=1, status=1, opcionais=[1, 2])

    validated = CreatBurgerService(session).get_burger_infos_in_db(burger=burger)

    assert validated == {
        "name": "João",
        "meat": meat_db,
        "bread": bread_db,
        "status": status_db,
        "optionals": optional_list,
    }


@pytest.mark.unit
def test_positive_create(session, meat_db, bread_db, status_db, optional_list):

    burger = BurgerIn(nome="João", pao=1, carne=1, status=1, opcionais=[1, 2])

    burger_db = CreatBurgerService(session).create(burger=burger)

    assert burger_db.id is not None

    assert session.scalar(select(func.count()).select_from(Burger)) == 1
