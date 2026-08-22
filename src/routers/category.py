"""Módulo de rutas/endpoints para la gestión del recurso Categorías.

Define los endpoints HTTP para realizar operaciones CRUD sobre las categorías
del sistema de gestión hotelera, incluyendo filtrado dinámico, validaciones
de entrada con Pydantic y documentación OpenAPI estructurada.
"""

from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.orm import Session

from config.db import get_db
from crud.categories import CategoriesModel
from models.categories import Category
from schemas.category import (
    CategoryCreate,
    CategoryPatch,
    CategoryResponse,
    CategoryUpdate,
)
from validators.validation import Validator

# Configuración del enrutador de FastAPI para el recurso 'Categories'
router = APIRouter(
    prefix="/api/v1/categories",
    tags=["Categories"],
)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Obtener todas las categorías o filtrar por parámetros",
    response_model=List[CategoryResponse],
)
def get_all_categories(
    db: Annotated[Session, Depends(get_db)],
    category: Annotated[
        str | None,
        Query(
            min_length=2,
            max_length=50,
            description="Filtro opcional por nombre parcial o exacto de la categoría.",
            examples=["Suite"],
        ),
    ] = None,
    price: Annotated[
        float | None,
        Query(
            ge=0,
            description="Filtro opcional por precio de la categoría.",
            examples=[100.0],
        ),
    ] = None,
):
    """Consulta la lista general de categorías registradas en la Base de Datos.

    Soporta filtrado opcional mediante Query Parameters (?category=...&price=...).
    Si no se proveen parámetros de consulta, retorna el listado completo.

    Args:
        db (Session): Sesión de la base de datos inyectada vía FastAPI Depends.
        category (str | None): Nombre de la categoría a filtrar.
        price (float | None): Precio de la categoría a filtrar.

    Returns:
        List[CategoryResponse]: Lista de categorías devueltas por el servidor.
    """
    # Si se envía al menos un parámetro de filtro por URL
    if category is not None or price is not None:
        fields = {
            "category": category,
            "price": float(price) if price is not None else None,
        }
        # Depurar el diccionario removiendo campos nulos
        fields = Validator.depuration_fields_none(fields=fields)

        return CategoriesModel.get_all(db=db, fields=fields)

    # Retorno sin filtros
    return CategoriesModel.get_all(db=db)


@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener una categoría por su ID único",
)
def get_category_by_id(
    db: Annotated[Session, Depends(get_db)],
    category_id: Annotated[
        int,
        Path(
            gt=0,
            description="Identificador único numérico del registro.",
            examples=[1],
        ),
    ],
):
    """Busca y retorna un recurso específico de categoría a través de su clave primaria.

    Args:
        db (Session): Sesión activa de la base de datos.
        category_id (int): ID numérico de la categoría recibido en la URL (Path Parameter).

    Returns:
        CategoryResponse: Objeto de la categoría encontrada.

    Raises:
        HTTPException (404): Si el ID buscado no existe en la BD.
    """
    return CategoriesModel.get_by_id(db=db, id=category_id)


@router.post(
    "/",
    response_model=CategoryResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo recurso de categoría",
)
def create_category(
    db: Annotated[Session, Depends(get_db)],
    category_body: CategoryCreate,
):
    """Crea un nuevo registro de categoría validando la existencia de duplicados.

    Args:
        db (Session): Sesión activa de la base de datos.
        category_body (CategoryCreate): Esquema Pydantic que valida el Payload recibido.

    Returns:
        CategoryResponse: Objeto recién creado con sus datos persistidos e ID asignado.

    Raises:
        HTTPException (400): Si violas restricciones de campos o valores únicos duplicados.
    """
    # Conversión del modelo Pydantic v2 a diccionario Python
    data_dict = category_body.model_dump()

    return CategoriesModel.create(db=db, data=data_dict)


@router.put(
    "/{category_id}",
    response_model=CategoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar completamente una categoría (Reemplazo total)",
)
def update_category(
    db: Annotated[Session, Depends(get_db)],
    category_id: Annotated[
        int,
        Path(
            gt=0,
            description="Identificador único numérico de la categoría a actualizar.",
            examples=[1],
        ),
    ],
    category_body: CategoryUpdate,
):
    """Realiza un reemplazo completo (PUT) de los datos de una categoría existente.

    Args:
        db (Session): Sesión activa de la base de datos.
        category_id (int): ID de la categoría a actualizar.
        category_body (CategoryUpdate): Esquema con la totalidad de los datos requeridos.

    Returns:
        CategoryResponse: Objeto actualizado.
    """
    data_dict = category_body.model_dump()
    return CategoriesModel.update(db=db, id=category_id, data=data_dict)


@router.patch(
    "/{category_id}",
    response_model=CategoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar parcialmente una categoría",
)
def patch_category(
    db: Annotated[Session, Depends(get_db)],
    category_id: Annotated[
        int,
        Path(
            gt=0,
            description="Identificador único numérico de la categoría a modificar.",
            examples=[1],
        ),
    ],
    category_body: CategoryPatch,
):
    """Aplica modificaciones parciales (PATCH) sobre los atributos enviados en el cuerpo.

    Args:
        db (Session): Sesión activa de la base de datos.
        category_id (int): ID de la categoría a modificar.
        category_body (CategoryPatch): Esquema con campos opcionales para la actualización.

    Returns:
        CategoryResponse: Objeto modificado con los campos aplicados.
    """
    # exclude_unset=True evita actualizar campos que no fueron explícitamente enviados en la petición
    data_dict = category_body.model_dump(exclude_unset=True)
    return CategoriesModel.patch(db=db, id=category_id, data=data_dict)


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar una categoría",
)
def delete_category(
    db: Annotated[Session, Depends(get_db)],
    category_id: Annotated[
        int,
        Path(
            gt=0,
            description="Identificador único numérico de la categoría a eliminar.",
            examples=[1],
        ),
    ],
):
    """Elimina físicamente un registro de categoría por su identificador único.

    Args:
        db (Session): Sesión activa de la base de datos.
        category_id (int): ID de la categoría a remover.

    Returns:
        None: Retorna un estado 204 No Content en caso de éxito.
    """
    CategoriesModel.delete(db=db, id=category_id)
    return None