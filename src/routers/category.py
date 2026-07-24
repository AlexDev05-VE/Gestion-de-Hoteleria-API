from typing import Annotated, List
from fastapi import APIRouter, HTTPException, Path, Query, status

# Importamos todos los esquemas de categoría
from schemas.category import (
    CategoryCreate,
    CategoryPatch,
    CategoryResponse,
    CategoryUpdate,
)

# 1. Configuración del Router
router = APIRouter(
    prefix="/api/v1/categories",
    tags=["Categories"],
)

# ----------------------------------------------------------------------
# MOCK DE DATOS LOCAL (Simulación de Base de Datos)
# ----------------------------------------------------------------------
FAKE_CATEGORIES_DB = [
    {"category_id": 1, "category": "Simple", "price": 45.00},
    {"category_id": 2, "category": "Doble", "price": 75.50},
    {"category_id": 3, "category": "Suite Presidencial", "price": 180.00},
]


# ----------------------------------------------------------------------
# ENDPOINTS
# ----------------------------------------------------------------------

# --- 1. LISTAR TODAS / FILTRAR ---
@router.get(
    "/",
    response_model=List[CategoryResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar categorías con filtro opcional de precio",
)
def get_all_categories(
    max_price: Annotated[
        float | None,
        Query(
            gt=0,
            description="Filtrar categorías con un precio menor o igual al valor ingresado",
            alias="max_price",
        ),
    ] = None,
):
    pass


# --- 2. OBTENER POR ID ---
@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener una categoría por su ID",
)
def get_category_by_id(
    category_id: Annotated[
        int,
        Path(
            gt=0,
            description="Identificador único numérico de la categoría",
            examples=[1],
        ),
    ],
):
    pass


# --- 3. CREAR NUEVA CATEGORÍA ---
@router.post(
    "/",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear una nueva categoría de habitación",
)
def create_category(category_in: CategoryCreate):
    pass


# --- 4. REEMPLAZO COMPLETO (PUT) ---
@router.put(
    "/{category_id}",
    response_model=CategoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar completamente una categoría (Reemplazo total)",
)
def update_category(
    category_id: Annotated[
        int,
        Path(gt=0, description="ID de la categoría a actualizar"),
    ],
    category_in: CategoryUpdate,
):
    pass

# --- 5. ACTUALIZACIÓN PARCIAL (PATCH) ---
@router.patch(
    "/{category_id}",
    response_model=CategoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar parcialmente una categoría",
)
def patch_category(
    category_id: Annotated[
        int,
        Path(gt=0, description="ID de la categoría a modificar"),
    ],
    category_in: CategoryPatch,
):
    pass


# --- 6. ELIMINAR CATEGORÍA ---
@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar una categoría",
)
def delete_category(
    category_id: Annotated[
        int,
        Path(gt=0, description="ID de la categoría a eliminar"),
    ],
):
    pass