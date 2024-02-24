from fastapi import APIRouter
from sqlalchemy import select

from app.db import ActiveSession
from app.models import Status
from app.schemas import StatusOut

router = APIRouter()


@router.get("/status/", response_model=list[StatusOut])
def list_status(session: ActiveSession):
    return session.scalars(select(Status)).all()
