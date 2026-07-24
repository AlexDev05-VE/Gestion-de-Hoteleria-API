from typing import Annotated, List
from fastapi import APIRouter, HTTPException, Path, Query, status

# Importamos todos los esquemas necesarios para los endpoints de Room
from schemas.category import CategoryResponse
from schemas.room import RoomCreate, RoomResponse, RoomUpdate
from schemas.status import StatusResponse

# Configuración principal del APIRouter para Habitaciones
router = APIRouter(
    prefix="/api/v1/rooms",
    tags=["Rooms"],
)


# ======================================================================
# ENDPOINTS DE LECTURA (GET)
# ======================================================================

@router.get(
    "/",
    response_model=List[RoomResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar todas las habitaciones con filtros opcionales",
)
def get_all_rooms(
    floor: Annotated[
        int | None,
        Query(
            ge=1,
            le=10,
            description="Filtrar habitaciones por número de piso (1 al 10)",
        ),
    ] = None,
    status_id: Annotated[
        int | None,
        Query(
            gt=0,
            description="Filtrar habitaciones por su estado (Status ID)",
        ),
    ] = None,
    category_id: Annotated[
        int | None,
        Query(
            gt=0,
            description="Filtrar habitaciones por su categoría (Category ID)",
        ),
    ] = None,
    is_active: Annotated[
        bool,
        Query(
            description="Filtrar por estado de activación/soft delete (Por defecto True)",
        ),
    ] = True,
):
    """
    Obtiene la lista de todas las habitaciones registradas en el sistema.
    
    Permite combinar múltiples parámetros de consulta opcionales (`Query Params`) 
    para filtrar por piso, estado, categoría o registros activos/inactivos.
    """
    pass


@router.get(
    "/{room_id}",
    response_model=RoomResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener una habitación específica por su ID",
)
def get_room_by_id(
    room_id: Annotated[
        int,
        Path(
            gt=0,
            description="Identificador único numérico de la habitación",
            examples=[1],
        ),
    ],
):
    """
    Busca y retorna la información detallada de una habitación según su `room_id`,
    incluyendo sus objetos anidados de estado (`status`) y categoría (`category`).
    """
    pass


# ======================================================================
# ENDPOINT DE CREACIÓN (POST)
# ======================================================================

@router.post(
    "/",
    response_model=RoomResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva habitación",
)
def create_room(
    room_in: RoomCreate,
):
    """
    Crea un nuevo registro de habitación en el sistema.
    
    Requiere los campos validados del cuerpo JSON (`RoomCreate`):
    - **room_number**: Número entero positivo (1 - 9999)
    - **floor**: Piso (1 - 10)
    - **comment**: Nota interna opcional (máx. 200 caracteres)
    - **status_id**: ID válido del estado inicial
    - **category_id**: ID válido de la categoría asignada
    """
    pass


# ======================================================================
# ENDPOINTS DE ACTUALIZACIÓN (PUT / PATCH)
# ======================================================================

@router.put(
    "/{room_id}",
    response_model=RoomResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar completamente una habitación (Reemplazo total)",
)
def update_room(
    room_id: Annotated[
        int,
        Path(
            gt=0,
            description="ID numérico de la habitación a reemplazar",
        ),
    ],
    room_in: RoomCreate,
):
    """
    Reemplaza todos los datos de la habitación especificada por su `room_id`.
    
    Obliga a redefinir la totalidad de las propiedades obligatorias expuestas en `RoomCreate`.
    """
    pass


@router.patch(
    "/{room_id}",
    response_model=RoomResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualización parcial de una habitación",
)
def patch_room(
    room_id: Annotated[
        int,
        Path(
            gt=0,
            description="ID numérico de la habitación a modificar",
        ),
    ],
    room_in: RoomUpdate,
):
    """
    Modifica únicamente los campos enviados en el cuerpo JSON de la petición.
    
    Usa el esquema `RoomUpdate`, donde todos los atributos son opcionales (`None`).
    Permite cambiar individualmente el piso, estado, categoría, comentario o activar/desactivar (`is_active`).
    """
    pass


# ======================================================================
# ENDPOINT DE ELIMINACIÓN (DELETE / SOFT DELETE)
# ======================================================================

@router.delete(
    "/{room_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar una habitación (Soft Delete)",
)
def delete_room(
    room_id: Annotated[
        int,
        Path(
            gt=0,
            description="ID numérico de la habitación a desactivar o borrar",
        ),
    ],
):
    """
    Aplica el borrado lógico (`is_active = False`) o la eliminación física de la habitación por su `room_id`.
    
    Al completar la operación de manera exitosa, retorna un código HTTP `204 No Content` sin cuerpo de respuesta.
    """
    pass