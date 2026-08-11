from pydantic import BaseModel, ConfigDict, Field


"""
ESQUEMA BASE (Atributos compartidos) Utilizamos Pydactic para serializar y tipar tanto las respuestas como los inputs

- CategoryBase: Clase que hereda de BaseModel y define los atributos compartidos de la categoria
- 
"""
class CategoryBase(BaseModel):
    category: str = Field(
        ...,
        min_length=1, # -- Longitud minima es de 1 caracter
        max_length=100, # -- Longitud maxima es de 100 caracteres
        description="Nombre de la categoría (ej. Suite, Individual, Doble)", # -- Descripcion del campo
        examples=["Suite Presidencial"], # -- Ejemplos de uso
    )
    price: float = Field(
        ...,
        gt=0,  # -- 'gt=0' garantiza que el price sea estrictamente positivo (> 0)
        description="price de la categoría por noche (debe ser mayor a 0)", # -- Descripcion del campo
        examples=[150.50], # -- Ejemplos de uso
    )


"""
ESQUEMAS DE ENTRADA (Creación y Actualizaciones)

- CategoryCreate: Clase que hereda de CategoryBase y define los atributos de la categoria para crear una nueva

- CategoryUpdate: Clase que hereda de CategoryBase y define los atributos de la categoria para actualizar una existente (Reemplazo completo)

- CategoryPatch: Clase que hereda de BaseModel y define los atributos de la categoria para actualizar una existente (Actualización parcial)
"""

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
        min_length=1, # -- Longitud minima es de 1 caracter
        max_length=100, # -- Longitud maxima es de 100 caracteres
        description="Nombre de la categoría", # -- Descripcion del campo
        examples=["Doble Superior"], # -- Ejemplos de uso
    )
    price: float | None = Field(
        default=None,
        gt=0, # -- 'gt=0' garantiza que el price sea estrictamente positivo (> 0)
        description="price de la categoría por noche (debe ser mayor a 0)", # -- Descripcion del campo
        examples=[180.00], # -- Ejemplos de uso
    )


"""
ESQUEMA DE SALIDA (Respuesta)
- CategoryResponse: Clase que hereda de CategoryBase y define los atributos de la categoria para respuesta
"""
class CategoryResponse(CategoryBase):
    """Esquema devuelto por los endpoints GET, POST, PUT y PATCH"""
    category_id: int = Field(
        ..., # -- Se requiere un valor
        description="Identificador único de la categoría", # -- Descripcion del campo
        examples=[1], # -- Ejemplos de uso
    )

    # Configuración para compatibilidad con ORMs como SQLAlchemy - Permite que el schema pueda ser creado a partir de instancias de modelos SQLAlchemy
    model_config = ConfigDict(from_attributes=True)