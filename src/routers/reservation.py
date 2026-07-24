from datetime import datetime
from typing import Annotated, List
from fastapi import APIRouter, HTTPException, Path, Query, status

# Importamos los esquemas necesarios para la entidad Reservation
from schemas.category import CategoryResponse
from schemas.reservations import (
    ReservationCreate,
    ReservationPatch,
    ReservationResponse,
    ReservationUpdate,
)

# Configuración principal del APIRouter para Reservaciones
router = APIRouter(
    prefix="/api/v1/reservations",
    tags=["Reservations"],
)


# ======================================================================
# ENDPOINTS DE LECTURA (GET)
# ======================================================================

@router.get(
    "/",
    response_model=List[ReservationResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar todas las reservaciones con filtros opcionales",
)
def get_all_reservations(
    category_id: Annotated[
        int | None,
        Query(
            gt=0,
            description="Filtrar reservaciones asociadas a una categoría específica",
            examples=[1],
        ),
    ] = None,
    is_paid: Annotated[
        bool | None,
        Query(
            description="Filtrar por estado de pago (True para pagadas, False para pendientes)",
        ),
    ] = None,
    client_name: Annotated[
        str | None,
        Query(
            description="Filtrar por nombre o apellido del cliente",
            examples=["María"],
        ),
    ] = None,
):
    """
    Obtiene la lista completa de reservaciones registradas en el sistema.
    
    Permite aplicar múltiples filtros opcionales mediante parámetros de consulta (`Query Params`)
    para buscar por categoría asignada (`category_id`), estado de pago (`is_paid`) o cliente (`client_name`).
    """
    pass


@router.get(
    "/{reservation_id}",
    response_model=ReservationResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener una reservación específica por su ID",
)
def get_reservation_by_id(
    reservation_id: Annotated[
        int,
        Path(
            gt=0,
            description="Identificador único numérico de la reservación",
            examples=[1],
        ),
    ],
):
    """
    Busca y retorna los detalles de una reservación según su `reservation_id`,
    incluyendo la información anidada de la categoría asignada (`category`).
    """
    pass


# ======================================================================
# ENDPOINT DE CREACIÓN (POST)
# ======================================================================

@router.post(
    "/",
    response_model=ReservationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva reservación",
)
def create_reservation(
    reservation_in: ReservationCreate,
):
    """
    Registra una nueva reservación en el sistema.
    
    Requiere el cuerpo JSON validado según `ReservationCreate`:
    - **client_first_name**: Nombre del cliente (1 - 100 caracteres)
    - **client_last_name**: Apellido del cliente (1 - 100 caracteres)
    - **reservation_date**: Fecha y hora en formato ISO 8601 (ej. "2026-07-25T14:30:00")
    - **is_paid**: Estado del pago (Por defecto False)
    - **category_id**: ID válido de la categoría asignada
    """
    pass


# ======================================================================
# ENDPOINTS DE ACTUALIZACIÓN (PUT / PATCH)
# ======================================================================

@router.put(
    "/{reservation_id}",
    response_model=ReservationResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar completamente una reservación (Reemplazo total)",
)
def update_reservation(
    reservation_id: Annotated[
        int,
        Path(
            gt=0,
            description="ID numérico de la reservación a reemplazar",
            examples=[1],
        ),
    ],
    reservation_in: ReservationUpdate,
):
    """
    Reemplaza la totalidad de los datos de la reservación especificada por su `reservation_id`.
    
    Obliga a redefinir todos los campos expuestos en `ReservationUpdate`.
    """
    pass


@router.patch(
    "/{reservation_id}",
    response_model=ReservationResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar parcialmente una reservación",
)
def patch_reservation(
    reservation_id: Annotated[
        int,
        Path(
            gt=0,
            description="ID numérico de la reservación a modificar",
            examples=[1],
        ),
    ],
    reservation_in: ReservationPatch,
):
    """
    Modifica únicamente los campos enviados en el cuerpo JSON de la petición.
    
    Usa el esquema `ReservationPatch`, donde todos los atributos son opcionales (`None`).
    Permite actualizar de forma independiente el nombre/apellido del cliente, la fecha, el estado de pago o la categoría.
    """
    pass


# ======================================================================
# ENDPOINT DE ELIMINACIÓN (DELETE)
# ======================================================================

@router.delete(
    "/{reservation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar una reservación",
)
def delete_reservation(
    reservation_id: Annotated[
        int,
        Path(
            gt=0,
            description="ID numérico de la reservación a eliminar",
            examples=[1],
        ),
    ],
):
    """
    Elimina un registro de reservación del sistema según su `reservation_id`.
    
    Responde con un código HTTP `204 No Content` sin cuerpo de respuesta tras completarse correctamente.
    """
    pass