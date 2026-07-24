from typing import Annotated, List
from fastapi import APIRouter, HTTPException, Path, Query, status

# Importamos tu esquema de respuesta
from schemas.status import RoomStatusEnum, StatusResponse

# 1. Instanciamos el APIRouter con su prefijo y tag para la documentación
router = APIRouter(
    prefix="/api/v1/statuses",
    tags=["Room Statuses"],
)

# ----------------------------------------------------------------------
# MOCK DE DATOS LOCAL (Simulación de la base de datos)
# ----------------------------------------------------------------------
FAKE_STATUSES_DB = [
    {"id": 1, "name": RoomStatusEnum.DISPONIBLE},
    {"id": 2, "name": RoomStatusEnum.OCUPADO},
    {"id": 3, "name": RoomStatusEnum.MANTENIMIENTO},
    {"id": 4, "name": RoomStatusEnum.FUERA_DE_SERVICIO},
    {"id": 5, "name": RoomStatusEnum.RESERVADO},
]


# ----------------------------------------------------------------------
# ENDPOINTS
# ----------------------------------------------------------------------

@router.get(
    "/",
    response_model=List[StatusResponse],
    status_code=status.HTTP_200_OK,
    responses={200: {"description": "Estados obtenidos correctamente"}},
    summary="Obtener el catálogo completo de estados de habitación",
)
def get_all_statuses(
    name_filter: Annotated[
        RoomStatusEnum | None,
        Query(
            description="Filtrar por un estado en específico",
            alias="name",
        ),
    ] = None,
):
    pass


@router.get(
    "/{status_id}",
    response_model=StatusResponse,
    status_code=status.HTTP_200_OK,
    responses={200: {"description": "Estado obtenido correctamente"}},
    summary="Obtener un estado de habitación por su ID",
)
def get_status_by_id(
    status_id: Annotated[
        int,
        Path(
            gt=0,
            description="Identificador único numérico del estado",
            examples=[1],
        ),
    ],
):
    pass