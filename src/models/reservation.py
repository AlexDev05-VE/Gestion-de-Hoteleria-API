from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base

if TYPE_CHECKING:
    from models.categories import Category
    from models.lodging import Lodging



"""
Modelo de Reservation:
- reservation_id: Integer, Primary Key, Autoincrement, Index
- client_first_name: String(100), Not Null
- client_last_name: String(100), Not Null
- reservation_date: DateTime(timezone=True), Not Null
- is_paid: Boolean, Not Null, Default False
- category_id: Integer, Not Null, Foreign Key to categories.category_id
- category: Relationship with Category
- lodgings: Relationship with Lodging
"""
class Reservation(Base):
    __tablename__ = "reservations"

    # Atributos Propios de la tabla
    reservation_id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True, 
        autoincrement=True
    )
    client_first_name: Mapped[str] = mapped_column(
        String(100), 
        nullable=False
    )
    client_last_name: Mapped[str] = mapped_column(
        String(100), 
        nullable=False
    )

    # TIMESTAMPTZ -> DateTime con timezone=True
    reservation_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        nullable=False
    )
    is_paid: Mapped[bool] = mapped_column(
        Boolean, 
        nullable=False, 
        default=False
    )

    # Clave Foránea
    # Relacion con Categories
    category_id: Mapped[int] = mapped_column(
        ForeignKey(
            "categories.category_id", 
            ondelete="RESTRICT", 
            onupdate="CASCADE"
        ),
        nullable=False,
        index=True,
    )

    # Relación ORM
    # Relacion con Categories
    category: Mapped["Category"] = relationship(
        "Category", 
        back_populates="reservations"
    )

    # Relacion con Lodgings
    lodgings: Mapped[list["Lodging"]] = relationship(
        "Lodging",
        back_populates="reservation",
    )