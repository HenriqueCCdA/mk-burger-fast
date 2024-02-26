from fastapi import APIRouter
from sqlalchemy import select

from app.db import ActiveSession
from app.models import Bread, Burger, Meat, Optional, Status
from app.schemas import BurgerOut, IngredientsOut, StatusOut

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

    burgers = [
        {
            "id": item.id,
            "nome": item.name,
            "pao": item.bread.tipo,
            "carne": item.meat.tipo,
            "status": item.status.tipo,
            "opcionais": [it.tipo for it in item.optionals],
        }
        for item in session.scalars(select(Burger)).all()
    ]
    return burgers
