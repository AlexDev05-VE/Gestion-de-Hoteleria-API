from pydantic import BaseModel, ConfigDict, Field


# ----------------------------------------------------------------------
# ESQUEMA BASE (Atributos compartidos)
# ----------------------------------------------------------------------
class CategoryBase(BaseModel):
    category: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Nombre de la categoría (ej. Suite, Individual, Doble)",
        examples=["Suite Presidencial"],
    )
    price: float = Field(
        ...,
        gt=0,  # 'gt=0' garantiza que el price sea estrictamente positivo (> 0)
        description="price de la categoría por noche (debe ser mayor a 0)",
        examples=[150.50],
    )


# ----------------------------------------------------------------------
# ESQUEMAS DE ENTRADA (Creación y Actualizaciones)
# ----------------------------------------------------------------------
class CategoryCreate(CategoryBase):
    """Esquema utilizado para el POST /api/v1/category"""

    pass


class CategoryUpdate(CategoryBase):
    """Esquema utilizado para el PUT /api/v1/category/{category_id} (Reemplazo completo)"""

    pass


class CategoryPatch(BaseModel):
    """Esquema utilizado para el PATCH /api/v1/category/{category_id} (Actualización parcial)"""

    category: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
        description="Nombre de la categoría",
        examples=["Doble Superior"],
    )
    price: float | None = Field(
        default=None,
        gt=0,
        description="price de la categoría por noche (debe ser mayor a 0)",
        examples=[180.00],
    )


# ----------------------------------------------------------------------
# ESQUEMA DE SALIDA (Respuesta)
# ----------------------------------------------------------------------
class CategoryResponse(CategoryBase):
    """Esquema devuelto por los endpoints GET, POST, PUT y PATCH"""

    category_id: int = Field(
        ...,
        description="Identificador único de la categoría",
        examples=[1],
    )

    # Configuración para compatibilidad con ORMs como SQLAlchemy
    model_config = ConfigDict(from_attributes=True)