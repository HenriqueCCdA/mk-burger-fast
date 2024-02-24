from pydantic import BaseModel


class StatusOut(BaseModel):
    id: int
    tipo: str
