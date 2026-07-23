from enum import Enum
from pydantic import BaseModel, ConfigDict, Field

class RoleName(str, Enum):
    """
    Enum para restringir los nombres de roles permitidos en el sistema.
    Heredar de 'str' facilita la serialización automática a JSON.
    """
    ADMINISTRADOR = "Administrador"
    RECEPCIONISTA = "Recepcionista"



# ======================================================================
# ESQUEMA DE SALIDA PARA ROL (Solo GET)
# ======================================================================
class RoleResponse(BaseModel):
    """
    Esquema utilizado únicamente para la lectura y serialización de Roles.
    """

    role_id: int = Field(
        ...,
        gt=0,  # Entero estrictamente positivo
        description="Identificador único del rol",
        examples=[1],
    )
    role_name: RoleName = Field(
        ...,
        description="Nombre del rol asignado (restringido a los valores del Enum)",
        examples=[RoleName.ADMINISTRADOR],
    )

    # Habilita la serialización transparente desde modelos ORM (SQLAlchemy, SQLModel, etc.)
    model_config = ConfigDict(from_attributes=True)