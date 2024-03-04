from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.db import ActiveSession
from app.models import Bread, Burger, Meat, Optional, Status
from app.schemas import BurgerIn, BurgerOut, IngredientsOut, StatusOut
from app.service import CreatBurgerService, InvalidIgredients, InvalidOptionals

router = APIRouter()


@router.get("/status/", response_model=list[StatusOut])
def list_status(session: ActiveSession):
    return session.scalars(select(Status)).all()


@router.get("/ingredientes/", response_model=IngredientsOut)
def list_ingredients(session: ActiveSession):

    meats = session.scalars(select(Meat)).all()
    optionals = session.scalars(select(Optional)).all()
    breads = session.scalars(select(Bread)).all()

    return {"carnes": meats, "paes": breads, "opcionais": optionals}


@router.get("/burgers/", response_model=list[BurgerOut])
def list_burgers(session: ActiveSession):
    burgers = [to_dict(item) for item in session.scalars(select(Burger)).all()]
    return burgers


@router.post("/burgers", response_model=BurgerOut, status_code=status.HTTP_201_CREATED)
def create_burgers(session: ActiveSession, burger: BurgerIn):

    create_service = CreatBurgerService(session)

    try:
        burger_new = create_service.create(burger)
    except (InvalidIgredients, InvalidOptionals) as e:
        raise HTTPException(
            detail=e.args[0],
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        ) from e

    return to_dict(burger_new)


def to_dict(burger: Burger) -> dict[str, int | str | list[str]]:
    return {
        "id": burger.id,
        "nome": burger.name,
        "carne": burger.meat.tipo,
        "pao": burger.bread.tipo,
        "status": burger.status.tipo,
        "opcionais": [it.tipo for it in burger.optionals],
    }
