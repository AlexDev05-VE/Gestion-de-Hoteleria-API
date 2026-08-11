from typing import Annotated, Optional
from pydantic import BaseModel, Field, ConfigDict
from schemas.status import StatusResponse
from schemas.category import CategoryResponse


"""TIPOS REUTILIZABLES CON ANNOTATED

- RoomNumberType: Alias para RoomNumber con validación de entero positivo entre 1 y 9999
- FloorType: Alias para Floor con validación de entero positivo entre 1 y 10
- CommentType: Alias para Comment con validación de cadena opcional de hasta 200 caracteres
- IDType: Alias para ID con validación de entero positivo
"""
# Definimos las reglas de validación en alias para no repetir el Field(...) una y otra vez

RoomNumberType = Annotated[
    int, 
    Field(gt=0, ge=1, le=9999, description="Número de habitación (entero positivo)")
]

FloorType = Annotated[
    int, 
    Field(gt=0, ge=1, le=10, description="Piso de la habitación (entero positivo entre 1 y 10)")
]

CommentType = Annotated[
    Optional[str], 
    Field(None, max_length=200, description="Comentario o nota interna para recepción (máx. 200 caracteres)")
]

IDType = Annotated[
    int, 
    Field(gt=0, description="Identificador único (entero positivo)")
]

"""ESQUEMAS PRINCIPALES DE ROOM

- RoomBase: Clase base que define los atributos comunes de la habitación

- RoomCreate: Clase que hereda de RoomBase y define los atributos del usuario para crear uno nuevo

- RoomUpdate: Clase que hereda de BaseModel y define los atributos del usuario para actualizar uno existente (Reemplazo completo)

- RoomPatch: Clase que hereda de BaseModel y define los atributos del usuario para actualizar uno existente (Actualización parcial)
"""

class RoomBase(BaseModel):
    """Atributos comunes compartidos por la entidad Room."""
    room_number: RoomNumberType
    floor: FloorType
    comment: CommentType = None
    status_id: IDType
    category_id: IDType


class RoomCreate(RoomBase):
    """Esquema para la creación de una habitación (POST)."""
    pass  # Hereda todo lo de RoomBase


class RoomUpdate(BaseModel):
    """Esquema para la actualización parcial o completa de una habitación (PUT / PATCH)."""
    room_number: Optional[RoomNumberType] = None
    floor: Optional[FloorType] = None
    comment: CommentType = None
    status_id: Optional[IDType] = None
    category_id: Optional[IDType] = None
    is_active: Annotated[
        Optional[bool], 
        Field(None, description="Estado de borrado lógico")
    ] = None


class RoomResponse(BaseModel):
    """Esquema de salida/serialización para lecturas (GET)."""
    id: IDType
    room_number: int
    floor: int
    comment: Optional[str] = None
    is_active: Annotated[bool, Field(True, description="Indicador de Soft Delete")] = True
    
    # Relaciones anidadas con las otras clases/entidades
    status: StatusResponse
    category: CategoryResponse

    model_config = ConfigDict(from_attributes=True)