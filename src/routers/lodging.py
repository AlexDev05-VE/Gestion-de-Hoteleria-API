from datetime import datetime
from typing import Annotated, List
from fastapi import APIRouter, HTTPException, Path, Query, status

# Importamos las clases necesarias del esquema Lodging
from schemas.lodging import (
    LodgingCreate,
    LodgingPatch,
    LodgingResponse,
    LodgingUpdate,
    StayType,
)

# Configuración principal del APIRouter para Hospedajes
router = APIRouter(
    prefix="/api/v1/lodgings",
    tags=["Lodgings"],
)


# ======================================================================
# ENDPOINTS DE LECTURA (GET)
# ======================================================================

@router.get(
    "/",
    response_model=List[LodgingResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar todos los registros de hospedaje con filtros opcionales",
)
def get_all_lodgings(
    room_id: Annotated[
        int | None,
        Query(
            gt=0,
            description="Filtrar por ID de la habitación",
            examples=[1],
        ),
    ] = None,
    user_id: Annotated[
        int | None,
        Query(
            gt=0,
            description="Filtrar por ID del usuario (recepcionista o recepcionista que registró)",
            examples=[1],
        ),
    ] = None,
    stay_type: Annotated[
        StayType | None,
        Query(
            description="Filtrar por modalidad/tipo de estadía (Dropdown en Swagger)",
        ),
    ] = None,
    start_date: Annotated[
        datetime | None,
        Query(
            description="Fecha inicial para buscar hospedajes en un rango de tiempo (ISO 8601)",
            examples=["2026-07-01T00:00:00"],
        ),
    ] = None,
    end_date: Annotated[
        datetime | None,
        Query(
            description="Fecha final para buscar hospedajes en un rango de tiempo (ISO 8601)",
            examples=["2026-07-31T23:59:59"],
        ),
    ] = None,
):
    """
    Obtiene el listado general de hospedajes registrados en el sistema.
    
    Permite aplicar múltiples filtros por parámetros de consulta (`Query Params`):
    - **room_id**: Filtra las estadías asociadas a una habitación específica.
    - **user_id**: Filtra los registros creados por un usuario en particular.
    - **stay_type**: Menú desplegable para filtrar por modalidad de tiempo (ej. `amanecer`, `3 horas`).
    - **start_date / end_date**: Permite consultar hospedajes dentro de una ventana de fechas.
    """
    pass


@router.get(
    "/{lodging_id}",
    response_model=LodgingResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener un hospedaje por su ID",
)
def get_lodging_by_id(
    lodging_id: Annotated[
        int,
        Path(
            gt=0,
            description="Identificador único numérico del registro de hospedaje",
            examples=[1],
        ),
    ],
):
    """
    Busca y retorna la información detallada de una estadía según su `lodging_id`,
    incluyendo sus objetos anidados: `room`, `user`, `payment` y `reservation` (si aplica).
    """
    pass


# ======================================================================
# ENDPOINT DE CREACIÓN (POST)
# ======================================================================

@router.post(
    "/",
    response_model=LodgingResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar una nueva estadía / check-in",
)
def create_lodging(
    lodging_in: LodgingCreate,
):
    """
    Registra un nuevo ingreso / hospedaje en el sistema.
    
    Requiere el cuerpo JSON validado según `LodgingCreate`:
    - **initial_time**: Fecha/hora inicial (check-in)
    - **final_time**: Fecha/hora de salida estipulada (check-out)
    - **stay_type**: Tipo de estadía (`3 horas`, `4 horas`, `amanecer`, etc.)
    - **room_id**: ID de la habitación asignada
    - **user_id**: ID del recepcionista/usuario que registra
    - **payment_id**: ID del método de pago utilizado
    - **reservation_id**: (Opcional) ID de la reserva previa si existiera
    """
    pass


# ======================================================================
# ENDPOINTS DE ACTUALIZACIÓN (PUT / PATCH)
# ======================================================================

@router.put(
    "/{lodging_id}",
    response_model=LodgingResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar completamente un registro de hospedaje (Reemplazo total)",
)
def update_lodging(
    lodging_id: Annotated[
        int,
        Path(
            gt=0,
            description="ID numérico del hospedaje a reemplazar",
            examples=[1],
        ),
    ],
    lodging_in: LodgingUpdate,
):
    """
    Reemplaza todos los datos del registro de hospedaje indicado por su `lodging_id`.
    """
    pass


@router.patch(
    "/{lodging_id}",
    response_model=LodgingResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar parcialmente un registro de hospedaje",
)
def patch_lodging(
    lodging_id: Annotated[
        int,
        Path(
            gt=0,
            description="ID numérico del hospedaje a modificar",
            examples=[1],
        ),
    ],
    lodging_in: LodgingPatch,
):
    """
    Modifica únicamente los campos especificadas en el cuerpo JSON de la petición.
    
    Permite extender o modificar fechas (`initial_time`, `final_time`), cambiar la habitación,
    actualizar comentarios o ajustar la modalidad de estadía (`stay_type`).
    """
    pass


# ======================================================================
# ENDPOINT DE ELIMINACIÓN (DELETE)
# ======================================================================

@router.delete(
    "/{lodging_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar o anular un registro de hospedaje",
)
def delete_lodging(
    lodging_id: Annotated[
        int,
        Path(
            gt=0,
            description="ID numérico del hospedaje a eliminar",
            examples=[1],
        ),
    ],
):
    """
    Elimina o cancela un registro de hospedaje del sistema según su `lodging_id`.
    
    Devuelve una respuesta con código HTTP `204 No Content` sin cuerpo tras completarse con éxito.
    """
    pass