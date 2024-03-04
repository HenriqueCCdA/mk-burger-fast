from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.db import ActiveSession
from app.models import Bread, Burger, Meat, Optional, Status
from app.schemas import IngredientsOut, StatusOut

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


@router.get("/status/", response_model=list[StatusOut])
def list_status(session: ActiveSession):
    return session.scalars(select(Status)).all()


@router.get("/ingredientes/", response_model=IngredientsOut)
def list_ingredients(session: ActiveSession):

    meats = session.scalars(select(Meat)).all()
    optionals = session.scalars(select(Optional)).all()
    breads = session.scalars(select(Bread)).all()

    return {"carnes": meats, "paes": breads, "opcionais": optionals}
