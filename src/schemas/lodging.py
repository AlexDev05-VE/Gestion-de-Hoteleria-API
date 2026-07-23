from __future__ import annotations

from datetime import datetime
from typing import Annotated, Optional
from pydantic import BaseModel, ConfigDict, Field, model_validator

from enum import Enum

# Importamos los esquemas de respuesta para las entidades relacionadas
from src.schemas.payment import PaymentMethodResponse
from src.schemas.reservations import ReservationResponse
from src.schemas.room import RoomResponse
from src.schemas.user import UserResponse


class StayType(str, Enum):
    """
    Modalidades o tipos de estadía permitidos en el hotel.
    """
    TRES_HORAS = "3 horas"
    CUATRO_HORAS = "4 horas"
    CINCO_HORAS = "5 horas"
    SEIS_HORAS = "6 horas"
    AMANECER = "amanecer"



# ==========================================
# TIPOS REUTILIZABLES CON ANNOTATED
# ==========================================

LodgingIDType = Annotated[
    int,
    Field(
        gt=0,
        description="Identificador único del hospedaje (entero positivo)",
        examples=[1],
    ),
]

IDType = Annotated[
    int,
    Field(
        gt=0,
        description="Identificador único de entidad referenciada (entero positivo)",
        examples=[1],
    ),
]

CommentsType = Annotated[
    Optional[str],
    Field(
        default=None,
        max_length=250,
        description="Comentarios, notas u observaciones internas sobre la estadía (máx. 250 caracteres)",
        examples=["Cliente solicitó toallas adicionales"],
    ),
]


# ==========================================
# ESQUEMAS PRINCIPALES DE LODGING
# ==========================================


class LodgingBase(BaseModel):
    """Atributos comunes compartidos por la entidad Lodging."""

    initial_time: datetime = Field(
        ...,
        description="Fecha y hora inicial del hospedaje (check-in)",
        examples=["2026-07-22T14:00:00"],
    )
    final_time: datetime = Field(
        ...,
        description="Fecha y hora final del hospedaje (check-out)",
        examples=["2026-07-23T12:00:00"],
    )
    stay_type: StayType = Field(
        ...,
        description="Tipo o modalidad de estadía (Por Horas, Diario, etc.)",
        examples=[StayType.AMANECER],
    )
    comments: CommentsType = None


class LodgingCreate(LodgingBase):
    """Esquema para crear un registro de hospedaje (POST). Recibe los IDs relacionales."""

    room_id: IDType
    user_id: IDType
    payment_id: IDType
    reservation_id: Optional[IDType] = Field(
        default=None,
        description="ID de la reservación (opcional si el cliente llegó sin reserva previa)",
    )

    @model_validator(mode="after")
    def validate_final_after_initial(self) -> LodgingCreate:
        """Valida que la fecha/hora final sea posterior a la inicial."""
        if self.final_time <= self.initial_time:
            raise ValueError(
                "La fecha y hora final (final_time) debe ser posterior a la inicial (initial_time)"
            )
        return self


class LodgingUpdate(LodgingBase):
    """Esquema para la actualización completa del hospedaje (PUT)."""

    room_id: IDType
    user_id: IDType
    payment_id: IDType
    reservation_id: Optional[IDType] = None

    @model_validator(mode="after")
    def validate_final_after_initial(self) -> LodgingUpdate:
        if self.final_time <= self.initial_time:
            raise ValueError(
                "La fecha y hora final (final_time) debe ser posterior a la inicial (initial_time)"
            )
        return self


class LodgingPatch(BaseModel):
    """Esquema para la actualización parcial del hospedaje (PATCH)."""

    initial_time: Optional[datetime] = None
    final_time: Optional[datetime] = None
    stay_type: Optional[StayType] = None
    comments: CommentsType = None
    room_id: Optional[IDType] = None
    user_id: Optional[IDType] = None
    payment_id: Optional[IDType] = None
    reservation_id: Optional[IDType] = None

    @model_validator(mode="after")
    def validate_dates_if_both_present(self) -> LodgingPatch:
        """Valida el orden cronológico solo si ambas fechas son enviadas en el PATCH."""
        if self.initial_time and self.final_time:
            if self.final_time <= self.initial_time:
                raise ValueError(
                    "La fecha y hora final (final_time) debe ser posterior a la inicial (initial_time)"
                )
        return self


class LodgingResponse(LodgingBase):
    """Esquema de salida devuelto en las consultas (GET) con las entidades anidadas."""

    lodging_id: LodgingIDType

    # Relaciones anidadas con las entidades completas
    room: RoomResponse
    user: UserResponse
    payment: PaymentMethodResponse
    reservation: Optional[ReservationResponse] = None

    model_config = ConfigDict(from_attributes=True)