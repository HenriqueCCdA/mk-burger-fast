from fastapi import APIRouter
from sqlalchemy import select

from app.db import ActiveSession
from app.models import Bread, Meat, Optional, Status
from app.schemas import IngredientsOut, StatusOut

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
