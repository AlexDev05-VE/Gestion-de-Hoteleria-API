from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from src.models.role import Role
    from src.models.lodging import Lodging

"""
Declarar Modelo de Base de DeclarativeBase
Clase de Herencia para los modelos de SQLAlchemy.
"""
class Base(DeclarativeBase):
    pass

"""
Modelo de User:
- user_id: Integer, Primary Key, Autoincrement, Index
- username: String(100), Not Null, Unique
- name: String(100), Not Null
- last_name: String(100), Not Null
- role_id: Integer, Not Null, Foreign Key to roles.role_id
- role: Relationship with Role
- lodgings: Relationship with Lodging
"""
class User(Base):
    __tablename__ = "users"

    # Atributos Propios de la tabla
    user_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, index=True
    )
    username: Mapped[str] = mapped_column(
        String(100), 
        nullable=False, 
        unique=True
    )
    name: Mapped[str] = mapped_column(
        String(100), 
        nullable=False
    )
    last_name: Mapped[str] = mapped_column(
        String(100), 
        nullable=False
    )

    # Llaves Foraneas
    # Relación con Role
    role_id: Mapped[int] = mapped_column(
        ForeignKey(
            "roles.role_id",
            ondelete="RESTRICT",
            onupdate="CASCADE"
        ),
        nullable=False
    )

    # Relaciones ORM
    # Relación con Role
    role: Mapped["Role"] = relationship(
        "Role",
        back_populates="users"
    )

    lodgings: Mapped[list["Lodging"]] = relationship(
        "Lodging",
        back_populates="user",
    )