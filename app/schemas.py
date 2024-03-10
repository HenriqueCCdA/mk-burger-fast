from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BaseItemOut(BaseModel):
    id: int
    tipo: str
    criado_em: Optional[datetime] = None
    atualizado_em: Optional[datetime] = None


class StatusOut(BaseItemOut): ...


class IngredientsOut(BaseModel):
    paes: list[BaseItemOut]
    carnes: list[BaseItemOut]
    opcionais: list[BaseItemOut]


class BurgerOut(BaseModel):
    id: int
    nome: str
    pao: str
    carne: str
    status: str
    opcionais: list[str]
    criado_em: Optional[datetime] = None
    atualizado_em: Optional[datetime] = None


class BurgerIn(BaseModel):
    nome: str
    pao: int
    carne: int
    status: int
    opcionais: list[int]


class StatusUpdate(BaseModel):
    status: int
