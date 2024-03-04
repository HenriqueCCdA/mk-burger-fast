from typing import Self, Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Base, Bread, Burger, Meat, Optional, Status
from app.schemas import BurgerIn


class InvalidIgredients(Exception): ...


class InvalidOptionals(Exception): ...


class CreatBurgerService:

    def __init__(self: Self, session: Session):
        self._session = session

    def get_infos_in_db(self: Self, Model, id: int):

        if Model == Meat:
            msg = f"Carne com id '{id}' não existe."
        elif Model == Bread:
            msg = f"Pao com id '{id}' não existe."
        elif Model == Status:
            msg = f"Status com id '{id}' não existe."

        if (obj := self._session.scalar(select(Model).where(Model.id == id))) is None:
            raise InvalidIgredients(msg)

        return obj

    def get_optionals_in_db(self: Self, opcionals: list[int]) -> Sequence[Optional]:

        list_opt_db = self._session.scalars(select(Optional).where(Optional.id.in_(opcionals))).all()

        if len(list_opt_db) != len(opcionals):
            for op in opcionals:
                opt_db = self._session.scalar(select(Optional).where(Optional.id == op))
                if opt_db is None:
                    raise InvalidOptionals(f"Opcional com id '{op}' não existe.")

        return list_opt_db

    def get_burger_infos_in_db(self: Self, burger: BurgerIn) -> dict[str, str | Base | Sequence[Base]]:

        meat = self.get_infos_in_db(Meat, burger.carne)
        bread = self.get_infos_in_db(Bread, burger.pao)
        status = self.get_infos_in_db(Status, burger.status)
        list_opt = self.get_optionals_in_db(burger.opcionais)

        return {
            "name": burger.nome,
            "meat": meat,
            "bread": bread,
            "status": status,
            "optionals": list_opt,
        }

    def create(self: Self, burger: BurgerIn) -> Burger:

        validated = self.get_burger_infos_in_db(burger)

        burger_new = Burger(**validated)

        self._session.add(burger_new)
        self._session.commit()
        self._session.refresh(burger_new)

        return burger_new
