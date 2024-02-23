from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase): ...


class PlaceHolderModel(Base):
    __tablename__ = "place_holder_model"

    id: Mapped[int] = mapped_column(primary_key=True)
    field: Mapped[str] = mapped_column(String)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(field={self.field})"
