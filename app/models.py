from datetime import datetime
from typing import Optional as OptionalType

from sqlalchemy import Column, DateTime, ForeignKey, String, Table, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

TYPE_NAME_LENGTH = 100


class Base(DeclarativeBase): ...


class TimestampMixin:
    created_at: Mapped[OptionalType[datetime]] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[OptionalType[datetime]] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())


burger_optional_table = Table(
    "burger_optional",
    Base.metadata,
    Column("burger_id", ForeignKey("burgers.id")),
    Column("optional_id", ForeignKey("optionals.id")),
)


class Bread(TimestampMixin, Base):
    __tablename__ = "breads"

    id: Mapped[int] = mapped_column(primary_key=True)
    tipo: Mapped[str] = mapped_column(String(TYPE_NAME_LENGTH))

    burgers: Mapped[list["Burger"]] = relationship(
        back_populates="bread",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(tipo={self.tipo})"


class Meat(TimestampMixin, Base):
    __tablename__ = "meats"

    id: Mapped[int] = mapped_column(primary_key=True)
    tipo: Mapped[str] = mapped_column(String(TYPE_NAME_LENGTH))

    burgers: Mapped[list["Burger"]] = relationship(
        back_populates="meat",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(tipo={self.tipo})"


class Optional(TimestampMixin, Base):
    __tablename__ = "optionals"

    id: Mapped[int] = mapped_column(primary_key=True)
    tipo: Mapped[str] = mapped_column(String(TYPE_NAME_LENGTH))

    burgers: Mapped[list["Burger"]] = relationship(
        secondary=burger_optional_table,
        back_populates="optionals",
    )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(tipo={self.tipo})"


class Status(TimestampMixin, Base):
    __tablename__ = "status"

    id: Mapped[int] = mapped_column(primary_key=True)
    tipo: Mapped[str] = mapped_column(String(TYPE_NAME_LENGTH))

    burgers: Mapped[list["Burger"]] = relationship(
        back_populates="status",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(tipo={self.tipo})"


class Burger(TimestampMixin, Base):
    __tablename__ = "burgers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(TYPE_NAME_LENGTH))

    bread_id: Mapped[int] = mapped_column(ForeignKey("breads.id"))
    meat_id: Mapped[int] = mapped_column(ForeignKey("meats.id"))
    status_id: Mapped[int] = mapped_column(ForeignKey("status.id"))

    bread: Mapped[Bread] = relationship(back_populates="burgers")
    meat: Mapped[Meat] = relationship(back_populates="burgers")
    status: Mapped[Status] = relationship(back_populates="burgers")

    optionals: Mapped[list[Optional]] = relationship(secondary=burger_optional_table, back_populates="burgers")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name})"
