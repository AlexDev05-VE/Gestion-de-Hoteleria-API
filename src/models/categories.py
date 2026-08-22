"""Módulo del modelo ORM para la entidad Categoría.

Define la clase `Category` mapeada a la tabla `categories` mediante el sistema
Declarative de SQLAlchemy (v2.0+), incluyendo sus restricciones de integridad,
tipado con `Mapped` y relaciones con otros recursos del sistema.
"""

from typing import TYPE_CHECKING, List
from sqlalchemy import CheckConstraint, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base

if TYPE_CHECKING:
    from models.reservation import Reservation
    from models.room import Room


class Category(Base):
    """Modelo de datos SQLAlchemy que representa la tabla 'categories'.

    Almacena las clasificaciones de habitaciones disponibles en el hotel
    y define sus tarifas base, restricciones e interacciones ORM con otras tablas.

    Attributes:
        category_id (int): Identificador único y clave primaria autoincremental.
        category (str): Nombre o etiqueta de la categoría (ej. Suite, Doble). Único.
        price (float): Precio o tarifa base asignada a la categoría.
        rooms (List[Room]): Colección de habitaciones pertenecientes a esta categoría.
        reservations (List[Reservation]): Historial de reservas asociadas.
    """

    __tablename__ = "categories"

    # Clave primaria autoincremental e indexada
    category_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
        doc="Clave primaria única autoincremental de la categoría.",
    )

    # Nombre de la categoría
    category: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        doc="Nombre descriptivo único de la categoría (máx. 100 caracteres).",
    )

    # Precio base por noche
    price: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False,
        doc="Precio base por noche de la categoría con precisión de 2 decimales.",
    )

    # Relaciones ORM
    rooms: Mapped[List["Room"]] = relationship(
        "Room",
        back_populates="category",
        doc="Relación un-a-muchos con el modelo Room.",
    )

    reservations: Mapped[List["Reservation"]] = relationship(
        "Reservation",
        back_populates="category",
        doc="Relación un-a-muchos con el modelo Reservation.",
    )

    # Restricciones de tabla e integridad de BD
    __table_args__ = (
        CheckConstraint("price > 0", name="chk_categories_price_positive"),
    )