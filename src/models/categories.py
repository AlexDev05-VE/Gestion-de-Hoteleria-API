from typing import TYPE_CHECKING, List
from sqlalchemy import CheckConstraint, Integer, Numeric, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
if TYPE_CHECKING:
    from src.models.room import Room
    from src.models.reservation import Reservation


"""
Declarar Modelo de Base de DeclarativeBase
Clase de Herencia para los modelos de SQLAlchemy.
"""
class Base(DeclarativeBase):
    pass

"""
Modelo de Category:
- category_id: Integer, Primary Key, Autoincrement, Index
- category: String(100), Not Null
- price: Numeric(10, 2), Not Null
- rooms: Relationship with Room
- reservations: Relationship with Reservation
- __table_args__: Restricciones CHECK
"""
class Category(Base):
    __tablename__ = "categories"

    # Atributos propios de la tabla
    # PK autoincremental (SQLAlchemy interpreta Integer + primary_key=True como IDENTITY o SERIAL en PostgreSQL)
    category_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, 
        autoincrement=True, 
        index=True
    )

    # VARCHAR(100) NOT NULL
    category: Mapped[str] = mapped_column(
        String(100), 
        nullable=False
    )

    # NUMERIC(10, 2) NOT NULL
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    # Relaciones ORM
    # Relacion con Room
    rooms: Mapped[List["Room"]] = relationship(
        "Room",
        back_populates="category"
    )

    # Relacion con Reservation
    reservations: Mapped[List["Reservation"]] = relationship(
        "Reservation",
        back_populates="category"
    )

    # Definición de restricciones compuestas / Check constraints
    __table_args__ = (
        CheckConstraint("price > 0", name="chk_categories_price_positive"),
    )