from typing import Annotated, List
from fastapi import APIRouter, HTTPException, Path, Query, status

# Importamos el esquema de respuesta y el Enum de Rol
from schemas.rol import RoleName, RoleResponse

# Configuración principal del APIRouter para Roles
router = APIRouter(
    prefix="/api/v1/roles",
    tags=["Roles"],
)


# ======================================================================
# ENDPOINTS DE LECTURA (GET) - CATÁLOGO DE ROLES
# ======================================================================

@router.get(
    "/",
    response_model=List[RoleResponse],
    status_code=status.HTTP_200_OK,
    summary="Obtener el catálogo completo de roles del sistema",
)
def get_all_roles(
    role_name: Annotated[
        RoleName | None,
        Query(
            description="Filtrar por un rol específico usando los valores permitidos en el Enum",
            alias="role_name",
        ),
    ] = None,
):
    """
    Retorna el catálogo completo de roles disponibles en el sistema (`Administrador`, `Recepcionista`).
    
    Permite aplicar un filtro opcional por nombre de rol mediante el parámetro de consulta (`Query Param`).
    En la documentación interactiva de Swagger, este campo aparecerá como un menú desplegable (dropdown).
    """
    pass


@router.get(
    "/{role_id}",
    response_model=RoleResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener un rol específico por su ID",
)
def get_role_by_id(
    role_id: Annotated[
        int,
        Path(
            gt=0,
            description="Identificador único numérico del rol",
            examples=[1],
        ),
    ],
):
    """
    Busca y retorna los detalles de un rol de usuario según su `role_id`.
    """
    pass