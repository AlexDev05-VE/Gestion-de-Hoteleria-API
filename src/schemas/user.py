from pydantic import BaseModel, ConfigDict, Field
from src.schemas.rol import RoleResponse


# ======================================================================
# ESQUEMA BASE DE USUARIO (Atributos compartidos)
# ======================================================================
class UserBase(BaseModel):
    username: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="name de usuario único",
        examples=["carlos_perez"],
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="name real del usuario",
        examples=["Carlos"],
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="last_name del usuario",
        examples=["Pérez"],
    )


# ======================================================================
# ESQUEMAS DE ENTRADA (Creación y Actualizaciones)
# ======================================================================
class UserCreate(UserBase):
    """Esquema para POST /api/v1/users"""

    role_id: int = Field(
        ...,
        gt=0,
        description="ID del rol asignado al usuario",
        examples=[1],
    )


class UserUpdate(UserBase):
    """Esquema para PUT /api/v1/users/{users_id} (Actualización completa)"""

    role_id: int = Field(
        ...,
        gt=0,
        description="ID del rol asignado al usuario",
        examples=[1],
    )


class UserPatch(BaseModel):
    """Esquema para PATCH /api/v1/users/{users_id} (Actualización parcial)"""

    username: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
        description="name de usuario",
        examples=["carlos_updated"],
    )
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
        description="name real",
        examples=["Carlos Antonio"],
    )
    last_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
        description="last_name",
        examples=["Pérez Gómez"],
    )
    role_id: int | None = Field(
        default=None,
        gt=0,
        description="ID del rol",
        examples=[2],
    )


# ======================================================================
# ESQUEMA DE SALIDA (Respuesta completa con serialización de Rol)
# ======================================================================
class UserResponse(UserBase):
    """Esquema devuelto en las respuestas GET, POST, PUT y PATCH"""

    user_id: int = Field(
        ...,
        gt=0,
        description="Identificador único del usuario (entero positivo)",
        examples=[1],
    )
    
    # Se reemplaza la ID simple por la clase / esquema de Rol completo
    role: RoleResponse = Field(
        ...,
        description="Objeto completo del rol asociado al usuario",
    )

    model_config = ConfigDict(from_attributes=True)