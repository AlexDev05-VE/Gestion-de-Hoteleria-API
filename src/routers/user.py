from typing import Annotated, List
from fastapi import APIRouter, HTTPException, Path, Query, status

# Importamos todos los esquemas necesarios para los endpoints de Usuario
from schemas.rol import RoleResponse
from schemas.user import (
    UserCreate,
    UserPatch,
    UserResponse,
    UserUpdate,
)

# Configuración principal del APIRouter para Usuarios
router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"],
)


# ======================================================================
# ENDPOINTS DE LECTURA (GET)
# ======================================================================

@router.get(
    "/",
    response_model=List[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar todos los usuarios con filtros opcionales",
)
def get_all_users(
    username: Annotated[
        str | None,
        Query(
            description="Filtrar por coincidencia o nombre de usuario exacto",
            examples=["carlos_perez"],
        ),
    ] = None,
    role_id: Annotated[
        int | None,
        Query(
            gt=0,
            description="Filtrar usuarios asociados a un ID de rol específico",
            examples=[1],
        ),
    ] = None,
):
    """
    Obtiene el listado completo de los usuarios registrados.
    
    Permite aplicar filtros opcionales por parámetro de consulta (`Query Params`)
    para buscar por nombre de usuario (`username`) o por rol asignado (`role_id`).
    """
    pass


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener un usuario específico por su ID",
)
def get_user_by_id(
    user_id: Annotated[
        int,
        Path(
            gt=0,
            description="Identificador único numérico del usuario",
            examples=[1],
        ),
    ],
):
    """
    Busca y retorna los datos detallados de un usuario según su `user_id`, 
    incluyendo la información anidada completa de su rol asignado (`role`).
    """
    pass


# ======================================================================
# ENDPOINT DE CREACIÓN (POST)
# ======================================================================

@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo usuario",
)
def create_user(
    user_in: UserCreate,
):
    """
    Registra un nuevo usuario en la base de datos.
    
    Requiere el cuerpo JSON validado según `UserCreate`:
    - **username**: Nombre de usuario único (1 - 100 caracteres)
    - **name**: Nombre real de la persona
    - **last_name**: Apellido real de la persona
    - **role_id**: ID válido del rol que se le asignará
    """
    pass


# ======================================================================
# ENDPOINTS DE ACTUALIZACIÓN (PUT / PATCH)
# ======================================================================

@router.put(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar completamente un usuario (Reemplazo total)",
)
def update_user(
    user_id: Annotated[
        int,
        Path(
            gt=0,
            description="ID numérico del usuario a reemplazar",
            examples=[1],
        ),
    ],
    user_in: UserUpdate,
):
    """
    Reemplaza la totalidad de la información de un usuario especificado por su `user_id`.
    
    Obliga a redefinir todos los campos obligatorios del esquema `UserUpdate`.
    """
    pass


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar parcialmente los datos de un usuario",
)
def patch_user(
    user_id: Annotated[
        int,
        Path(
            gt=0,
            description="ID numérico del usuario a modificar",
            examples=[1],
        ),
    ],
    user_in: UserPatch,
):
    """
    Modifica únicamente los campos enviados en el cuerpo JSON de la petición.
    
    Utiliza `UserPatch`, donde todos los atributos son opcionales (`None`).
    Permite actualizar de forma independiente el `username`, `name`, `last_name` o el `role_id`.
    """
    pass


# ======================================================================
# ENDPOINT DE ELIMINACIÓN (DELETE)
# ======================================================================

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un usuario",
)
def delete_user(
    user_id: Annotated[
        int,
        Path(
            gt=0,
            description="ID numérico del usuario a eliminar",
            examples=[1],
        ),
    ],
):
    """
    Elimina un usuario del sistema mediante su `user_id`.
    
    Responde con un código HTTP `204 No Content` sin cuerpo de respuesta tras completarse correctamente.
    """
    pass