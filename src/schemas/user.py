from pydantic import BaseModel, ConfigDict, Field
from schemas.rol import RoleResponse


"""ESQUEMA BASE DE USUARIO (Atributos compartidos)

- UserBase: Clase que hereda de BaseModel y define los atributos compartidos del usuario
"""
class UserBase(BaseModel):
    username: str = Field(
        ...,
        min_length=1, # -- Longitud minima es de 1 caracter
        max_length=100, # -- Longitud maxima es de 100 caracteres
        description="name de usuario único", # -- Descripcion del campo
        examples=["carlos_perez"], # -- Ejemplos de uso
    )
    name: str = Field(
        ...,
        min_length=1, # -- Longitud minima es de 1 caracter
        max_length=100, # -- Longitud maxima es de 100 caracteres
        description="name real del usuario", # -- Descripcion del campo
        examples=["Carlos"], # -- Ejemplos de uso
    )
    last_name: str = Field(
        ...,
        min_length=1, # -- Longitud minima es de 1 caracter
        max_length=100, # -- Longitud maxima es de 100 caracteres
        description="last_name del usuario", # -- Descripcion del campo
        examples=["Pérez"], # -- Ejemplos de uso
    )


"""ESQUEMAS DE ENTRADA (Creación y Actualizaciones)

- UserCreate: Clase que hereda de UserBase y define los atributos del usuario para crear uno nuevo
- UserUpdate: Clase que hereda de UserBase y define los atributos del usuario para actualizar uno existente (Reemplazo completo)
- UserPatch: Clase que hereda de BaseModel y define los atributos del usuario para actualizar uno existente (Actualización parcial)
"""

class UserCreate(UserBase):
    """Esquema para POST /api/v1/users"""

    role_id: int = Field(
        ...,
        gt=0, # -- 'gt=0' garantiza que el role_id sea mayor a 0
        description="ID del rol asignado al usuario", # -- Descripcion del campo
        examples=[1], # -- Ejemplos de uso
    )


class UserUpdate(UserBase):
    """Esquema para PUT /api/v1/users/{users_id} (Actualización completa)"""

    role_id: int = Field(
        ...,
        gt=0, # -- 'gt=0' garantiza que el role_id sea mayor a 0
        description="ID del rol asignado al usuario", # -- Descripcion del campo
        examples=[1], # -- Ejemplos de uso
    )


class UserPatch(BaseModel):
    """Esquema para PATCH /api/v1/users/{users_id} (Actualización parcial)"""

    username: str | None = Field(
        default=None,
        min_length=1, # -- Longitud minima es de 1 caracter
        max_length=100, # -- Longitud maxima es de 100 caracteres
        description="name de usuario", # -- Descripcion del campo
        examples=["carlos_updated"], # -- Ejemplos de uso
    )
    name: str | None = Field(
        default=None,
        min_length=1, # -- Longitud minima es de 1 caracter
        max_length=100, # -- Longitud maxima es de 100 caracteres
        description="name real", # -- Descripcion del campo
        examples=["Carlos Antonio"], # -- Ejemplos de uso
    )
    last_name: str | None = Field(
        default=None,
        min_length=1, # -- Longitud minima es de 1 caracter
        max_length=100, # -- Longitud maxima es de 100 caracteres
        description="last_name", # -- Descripcion del campo
        examples=["Pérez Gómez"], # -- Ejemplos de uso
    )
    role_id: int | None = Field(
        default=None,
        gt=0, # -- 'gt=0' garantiza que el role_id sea mayor a 0
        description="ID del rol", # -- Descripcion del campo
        examples=[2], # -- Ejemplos de uso
    )


"""ESQUEMA DE SALIDA (Respuesta completa con serialización de Rol)

- UserResponse: Clase que hereda de UserBase y define los atributos del usuario para devolverlo como respuesta
"""
class UserResponse(UserBase):
    """Esquema devuelto en las respuestas GET, POST, PUT y PATCH"""

    user_id: int = Field(
        ...,
        gt=0, # -- 'gt=0' garantiza que el user_id sea mayor a 0
        description="Identificador único del usuario (entero positivo)", # -- Descripcion del campo
        examples=[1], # -- Ejemplos de uso
    )
    
    # Se reemplaza la ID simple por la clase / esquema de Rol completo
    role: RoleResponse = Field(
        ...,
        description="Objeto completo del rol asociado al usuario", # -- Descripcion del campo
    )

    # Configuración para compatibilidad con ORMs como SQLAlchemy - Permite que el schema pueda ser creado a partir de instancias de modelos SQLAlchemy
    model_config = ConfigDict(from_attributes=True)