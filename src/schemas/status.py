from enum import Enum
from typing import Annotated, Optional
from pydantic import BaseModel, Field, ConfigDict

# ==========================================
# ENUMERACIÓN DE ESTADOS PERMITIDOS
# ==========================================

class RoomStatusEnum(str, Enum):
    """Conjunto cerrado de estados permitidos para las habitaciones."""
    DISPONIBLE = "Disponible"
    OCUPADO = "Ocupado"
    MANTENIMIENTO = "Mantenimiento"
    FUERA_DE_SERVICIO = "Fuera de Servicio"
    RESERVADO = "Reservado"


# ==========================================
# TIPOS REUTILIZABLES CON ANNOTATED
# ==========================================

StatusIDType = Annotated[
    int, 
    Field(gt=0, description="Identificador único del estado (entero positivo)")
]

StatusNameType = Annotated[
    RoomStatusEnum, 
    Field(description="Nombre del estado de la habitación (Valor restringido)")
]

# ==========================================
# ESQUEMAS PRINCIPALES DE STATUS (READ-ONLY)
# ==========================================

class StatusBase(BaseModel):
    """Atributos base para la entidad Status."""
    name: StatusNameType


class StatusResponse(StatusBase):
    """Esquema de salida/serialización para lecturas (GET /status)."""
    id: StatusIDType

    model_config = ConfigDict(
        from_attributes=True,
        # Permite que el Enum se serialice como string directo ("Disponible") en el JSON
        use_enum_values=True 
    )