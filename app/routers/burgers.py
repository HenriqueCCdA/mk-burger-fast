from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.db import ActiveSession
from app.models import Burger, Status
from app.schemas import BurgerIn, BurgerOut, StatusUpdate
from app.service import CreatBurgerService, InvalidIgredients, InvalidOptionals

router = APIRouter()


@router.patch("/burgers/{id}/", status_code=status.HTTP_204_NO_CONTENT)
def update_burger_status(session: ActiveSession, id: int, status_update: StatusUpdate):

    if (status_ := session.get(Status, status_update.status)) is None:
        raise HTTPException(
            detail="Status inválido.",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    if (burger := session.get(Burger, id)) is None:
        raise HTTPException(
            detail="Buger não achado.",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    burger.status_id = status_.id

    session.commit()


@router.delete("/burgers/{id}/", status_code=status.HTTP_204_NO_CONTENT)
def delele_burger(session: ActiveSession, id: int):

    if (burger := session.get(Burger, id)) is None:
        raise HTTPException(
            detail="Buger não achado.",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    session.delete(burger)
    session.commit()


@router.get("/burgers/", response_model=list[BurgerOut])
def list_burgers(session: ActiveSession):
    return [to_dict(item) for item in session.scalars(select(Burger)).all()]


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


def to_dict(burger: Burger) -> dict:

    return {
        "id": burger.id,
        "nome": burger.name,
        "carne": burger.meat.tipo,
        "pao": burger.bread.tipo,
        "status": burger.status.tipo,
        "opcionais": [it.tipo for it in burger.optionals],
        "criado_em": burger.created_at,
        "atualizado_em": burger.updated_at,
    }
