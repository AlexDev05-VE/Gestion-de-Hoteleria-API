from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship  
from typing import TYPE_CHECKING
from models.base import Base

if TYPE_CHECKING:
    from models.lodging import Lodging


"""
Modelo de PaymentMethod:
- payment_id: Integer, Primary Key, Autoincrement, Index
- payment: String(200), Not Null
- is_active: Boolean, Not Null, Default True
- lodgings: Relationship with Lodging
"""
class PaymentMethod(Base):
    __tablename__ = "payment_methods"

    # Atributos Propios de la tabla
    payment_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True
    )
    payment: Mapped[str] = mapped_column(
        String(200), 
        nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, 
        nullable=False, 
        default=True
    )
    
    # Relaciones ORM
    # Relacion con Lodging
    lodgings: Mapped[list["Lodging"]] = relationship(
        "Lodging",
        back_populates="payment_method"
    )