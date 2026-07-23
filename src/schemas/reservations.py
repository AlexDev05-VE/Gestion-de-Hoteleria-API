from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, ConfigDict, Field

# Importamos el esquema de respuesta de Categoría
from src.schemas.category import CategoryResponse

# ==========================================
# TIPOS REUTILIZABLES CON ANNOTATED
# ==========================================

ReservationIDType = Annotated[
    int,
    Field(
        gt=0,
        description="Identificador único de la reservación (entero positivo)",
        examples=[1],
    ),
]

ClientName = Annotated[
    str,
    Field(
        min_length=1,
        max_length=100,
        description="Nombre del cliente",
        examples=["María"],
    ),
]

ClientName = Annotated[
    str,
    Field(
        min_length=1,
        max_length=100,
        description="Apellido del cliente",
        examples=["Delgado"],
    ),
]

CategoryIDType = Annotated[
    int,
    Field(
        gt=0,
        description="Identificador de la categoría asignada",
        examples=[1],
    ),
]


# ==========================================
# ESQUEMAS PRINCIPALES DE RESERVACIÓN
# ==========================================


class ReservationBase(BaseModel):
    """Atributos comunes compartidos por la entidad Reservation."""

    client_first_name: ClientName
    client_last_name: ClientName
    reservation_date: datetime = Field(
        ...,
        description="Fecha y hora de la reservación (ISO 8601)",
        examples=["2026-07-25T14:30:00"],
    )
    is_paid: bool = Field(
        default=False,
        description="Indicador de si la reserva está pagada (True/False)",
    )


class ReservationCreate(ReservationBase):
    """Esquema para crear una reservación (POST). Recibe el ID de la categoría."""

    category_id: CategoryIDType


class ReservationUpdate(ReservationBase):
    """Esquema para actualización completa de la reservación (PUT)."""

    category_id: CategoryIDType


class ReservationPatch(BaseModel):
    """Esquema para actualización parcial de la reservación (PATCH)."""

    client_first_name: Optional[ClientName] = None
    client_last_name: Optional[ClientName] = None
    reservation_date: Optional[datetime] = None
    is_paid: Optional[bool] = None
    category_id: Optional[CategoryIDType] = None


class ReservationResponse(ReservationBase):
    """Esquema de salida para lecturas (GET). Retorna la reservación con su categoría anidada."""

    reservation_id: ReservationIDType
    category: CategoryResponse

    # Mapeo transparente desde modelos ORM como SQLAlchemy
    model_config = ConfigDict(from_attributes=True)