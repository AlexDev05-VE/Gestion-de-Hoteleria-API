from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase  
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.lodging import Lodging

"""
Declarar Modelo de Base de DeclarativeBase
Clase de Herencia para los modelos de SQLAlchemy.
"""
class Base(DeclarativeBase):
    pass

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