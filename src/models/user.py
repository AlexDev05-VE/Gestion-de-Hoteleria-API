from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from models.base import Base


if TYPE_CHECKING:
    from models.role import Role
    from models.lodging import Lodging


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