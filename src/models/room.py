from typing import TYPE_CHECKING
from sqlalchemy import CheckConstraint, ForeignKey, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base

if TYPE_CHECKING:
    from models.status import Status
    from models.categories import Category
    from models.lodging import Lodging


"""
Modelo de Room:
- room_id: Integer, Primary Key, Autoincrement, Index
- room_number: Integer, Not Null, Unique, Index
- floor: Integer, Not Null, Index
- is_active: Boolean, Not Null, Default True
- status_id: Integer, Not Null, Foreign Key to statuses.status_id
- category_id: Integer, Not Null, Foreign Key to categories.category_id
- status: Relationship with Status
- category: Relationship with Category
- lodgings: Relationship with Lodging
- __table_args__: Restricciones CHECK
"""
class Room(Base):
    __tablename__ = "rooms"

    # Atributos Propios de la tabla
    room_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    room_number: Mapped[int] = mapped_column(
        Integer, 
        nullable=False, 
        unique=True, 
        index=True
    )
    floor: Mapped[int] = mapped_column(
        Integer, 
        nullable=False, 
        index=True
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, 
        nullable=False, 
        default=True
    )

    # Llaves Foraneas
    # Relación con Status
    status_id: Mapped[int] = mapped_column(
        ForeignKey(
            "statuses.status_id", 
            ondelete="RESTRICT", 
            onupdate="CASCADE"
        ),
        nullable=False,
        index=True,
    )

    # Relación con Categories
    category_id: Mapped[int] = mapped_column(
        ForeignKey(
            "categories.category_id", 
            ondelete="RESTRICT", 
            onupdate="CASCADE"
        ),
        nullable=False,
        index=True,
    )

    # Relaciones ORM
    # Relacion con Status
    status: Mapped["Status"] = relationship(
        "Status", 
        back_populates="rooms"
    )

    # Relación con Categories
    category: Mapped["Category"] = relationship(
        "Category", 
        back_populates="rooms"
    )
    
    # Relacion con Lodgings
    lodgings: Mapped[list["Lodging"]] = relationship(
        "Lodging",
        back_populates="room",
        cascade="all, delete-orphan",
    )

    # Restricciones CHECK
    __table_args__ = (
        CheckConstraint(
            "floor BETWEEN 1 AND 10", name="chk_rooms_floor_range"
        ),
        CheckConstraint(
            "room_number > 0", name="chk_rooms_number_positive"
        ),
    )