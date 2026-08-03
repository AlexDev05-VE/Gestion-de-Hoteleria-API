from typing import TYPE_CHECKING
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

if TYPE_CHECKING:
    from src.models.user import User

"""
Declarar Modelo de Base de DeclarativeBase
Clase de Herencia para los modelos de SQLAlchemy.
"""
class Base(DeclarativeBase):
    pass

"""
Modelo de Role:
- role_id: Integer, Primary Key, Autoincrement, Index
- role_name: String(100), Not Null, Unique
- users: Relationship with User
"""
class Role(Base):
    __tablename__ = "roles"

    # Atributos Propios de la tabla
    role_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True
    )
    role_name: Mapped[str] = mapped_column(
        String(100), 
        nullable=False, 
        unique=True
    )

    # Relaciones ORM
    users: Mapped[list["User"]] = relationship(back_populates="role")
