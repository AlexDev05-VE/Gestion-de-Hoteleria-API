from typing import Annotated, List
from fastapi import APIRouter, HTTPException, Path, Query, status

# Importamos los esquemas correspondientes a PaymentMethod
from schemas.payment import (
    PaymentMethodCreate,
    PaymentMethodPatch,
    PaymentMethodResponse,
    PaymentMethodUpdate,
)

# Configuración principal del APIRouter para Métodos de Pago
router = APIRouter(
    prefix="/api/v1/payment-methods",
    tags=["Payment Methods"],
)


# ======================================================================
# ENDPOINTS DE LECTURA (GET)
# ======================================================================

@router.get(
    "/",
    response_model=List[PaymentMethodResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar todos los métodos de pago",
)
def get_all_payment_methods(
    payment_name: Annotated[
        str | None,
        Query(
            description="Filtrar por coincidencia o nombre del método de pago",
            examples=["Zelle"],
            alias="payment",
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
    Obtiene la lista completa de métods de pago registrados en el sistema (Efectivo, Zelle, Punto de Venta, etc.).
    
    Permite aplicar filtros opcionales por parámetro de consulta (`Query Params`) 
    para buscar por nombre (`payment`) o estado de activación (`is_active`).
    """
    pass


@router.get(
    "/{payment_id}",
    response_model=PaymentMethodResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener un método de pago por su ID",
)
def get_payment_method_by_id(
    payment_id: Annotated[
        int,
        Path(
            gt=0,
            description="Identificador único numérico del método de pago",
            examples=[1],
        ),
    ],
):
    """
    Busca y retorna los datos detallados de un método de pago según su `payment_id`.
    """
    pass


# ======================================================================
# ENDPOINT DE CREACIÓN (POST)
# ======================================================================

@router.post(
    "/",
    response_model=PaymentMethodResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un nuevo método de pago",
)
def create_payment_method(
    payment_in: PaymentMethodCreate,
):
    """
    Crea un nuevo método de pago en el sistema.
    
    Requiere el cuerpo JSON validado por `PaymentMethodCreate`:
    - **payment**: Nombre del método de pago (1 - 200 caracteres, ej. "Punto de Venta").
    """
    pass


# ======================================================================
# ENDPOINTS DE ACTUALIZACIÓN (PUT / PATCH)
# ======================================================================

@router.put(
    "/{payment_id}",
    response_model=PaymentMethodResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar completamente un método de pago (Reemplazo total)",
)
def update_payment_method(
    payment_id: Annotated[
        int,
        Path(
            gt=0,
            description="ID numérico del método de pago a reemplazar",
            examples=[1],
        ),
    ],
    payment_in: PaymentMethodUpdate,
):
    """
    Reemplaza todos los datos del método de pago especificado por su `payment_id`.
    
    Obliga a redefinir el atributo obligatorio `payment`.
    """
    pass


@router.patch(
    "/{payment_id}",
    response_model=PaymentMethodResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar parcialmente un método de pago",
)
def patch_payment_method(
    payment_id: Annotated[
        int,
        Path(
            gt=0,
            description="ID numérico del método de pago a modificar",
            examples=[1],
        ),
    ],
    payment_in: PaymentMethodPatch,
):
    """
    Modifica únicamente los campos enviados en el cuerpo JSON de la petición.
    
    Utiliza `PaymentMethodPatch`, donde los atributos son opcionales (`None`).
    Permite modificar de forma independiente el nombre (`payment`) o cambiar su estado de activación (`is_active`).
    """
    pass


# ======================================================================
# ENDPOINT DE ELIMINACIÓN (DELETE / SOFT DELETE)
# ======================================================================

@router.delete(
    "/{payment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar o desactivar un método de pago (Soft Delete)",
)
def delete_payment_method(
    payment_id: Annotated[
        int,
        Path(
            gt=0,
            description="ID numérico del método de pago a eliminar o desactivar",
            examples=[1],
        ),
    ],
):
    """
    Aplica el borrado lógico (`is_active = False`) o borrado físico del método de pago mediante su `payment_id`.
    
    Responde con un código HTTP `204 No Content` sin cuerpo tras completarse la operación.
    """
    pass