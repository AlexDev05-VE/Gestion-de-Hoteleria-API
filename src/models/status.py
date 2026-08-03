from typing import TYPE_CHECKING, List
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
if TYPE_CHECKING:
    from src.models.room import Room

"""
Declarar Modelo de Base de DeclarativeBase
Clase de Herencia para los modelos de SQLAlchemy.
"""
class Base(DeclarativeBase):
    pass

"""
Modelo de Status:
- status_id: Integer, Primary Key, Autoincrement, Index
- name: String(50), Not Null, Unique
- rooms: Relationship with Room

"""
class Status(Base):
    __tablename__ = "statuses"

    # Atributos propios de la tabla
    status_id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True, 
        autoincrement=True, 
        index=True
    )
    name: Mapped[str] = mapped_column(
        String(50), 
        nullable=False, 
        unique=True
    )

    # Relación con Room
    rooms: Mapped[List["Room"]] = relationship(
        "Room", 
        back_populates="status"
        )