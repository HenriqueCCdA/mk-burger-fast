from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

TYPE_NAME_LENGTH = 100


class Base(DeclarativeBase): ...


class Bread(Base):
    __tablename__ = "breads"

    id: Mapped[int] = mapped_column(primary_key=True)
    tipo: Mapped[str] = mapped_column(String(TYPE_NAME_LENGTH))

    burgers: Mapped[list["Burger"]] = relationship(
        back_populates="bread",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(tipo={self.tipo})"


class Meat(Base):
    __tablename__ = "meats"

    id: Mapped[int] = mapped_column(primary_key=True)
    tipo: Mapped[str] = mapped_column(String(TYPE_NAME_LENGTH))

    burgers: Mapped[list["Burger"]] = relationship(
        back_populates="meat",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(tipo={self.tipo})"


class Optional(Base):
    __tablename__ = "optionals"

    id: Mapped[int] = mapped_column(primary_key=True)
    tipo: Mapped[str] = mapped_column(String(TYPE_NAME_LENGTH))

    burgers: Mapped[list["Burger"]] = relationship(
        back_populates="optional",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(tipo={self.tipo})"


class Status(Base):
    __tablename__ = "status"

    id: Mapped[int] = mapped_column(primary_key=True)
    tipo: Mapped[str] = mapped_column(String(TYPE_NAME_LENGTH))

    burgers: Mapped[list["Burger"]] = relationship(
        back_populates="status",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(tipo={self.tipo})"


class Burger(Base):
    __tablename__ = "burgers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(TYPE_NAME_LENGTH))

    bread_id: Mapped[int] = mapped_column(ForeignKey("breads.id"))
    meat_id: Mapped[int] = mapped_column(ForeignKey("meats.id"))
    optional_id: Mapped[int] = mapped_column(ForeignKey("optionals.id"))
    status_id: Mapped[int] = mapped_column(ForeignKey("status.id"))

    bread: Mapped[Bread] = relationship(back_populates="burgers")
    meat: Mapped[Meat] = relationship(back_populates="burgers")
    optional: Mapped[Optional] = relationship(back_populates="burgers")
    status: Mapped[Status] = relationship(back_populates="burgers")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name})"
