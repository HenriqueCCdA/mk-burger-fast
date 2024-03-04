from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.db import ActiveSession
from app.models import Burger
from app.schemas import BurgerIn, BurgerOut
from app.service import CreatBurgerService, InvalidIgredients, InvalidOptionals

router = APIRouter()


@router.delete("/burgers/{id}/", status_code=status.HTTP_204_NO_CONTENT)
def delele_burger(session: ActiveSession, id: int):

    burger = session.scalar(select(Burger).where(Burger.id == id))

    if burger is None:
        raise HTTPException(
            detail="Buger não achado",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    session.delete(burger)
    session.commit()


@router.get("/burgers/", response_model=list[BurgerOut])
def list_burgers(session: ActiveSession):
    burgers = [to_dict(item) for item in session.scalars(select(Burger)).all()]
    return burgers


@router.post("/burgers/", response_model=BurgerOut, status_code=status.HTTP_201_CREATED)
def create_burger(session: ActiveSession, burger: BurgerIn):

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
