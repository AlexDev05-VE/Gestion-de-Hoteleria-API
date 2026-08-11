from typing import Annotated, Optional
from pydantic import BaseModel, ConfigDict, Field


"""TIPOS REUTILIZABLES CON ANNOTATED

- PaymentIDType: Alias para PaymentID con validación de entero positivo
- PaymentNameType: Alias para PaymentName con validación de cadena opcional de hasta 200 caracteres
"""
PaymentIDType = Annotated[
    int, 
    Field(gt=0, description="Identificador único del método de pago (entero positivo)", examples=[1])
]

PaymentNameType = Annotated[
    str, 
    Field(
        min_length=1, 
        max_length=200, 
        description="Nombre del método de pago (ej. Efectivo, Transferencia, Punto de Venta, Zelle)", 
        examples=["Zelle"]
    )
]


"""ESQUEMAS PRINCIPALES DE PAYMENT METHOD

- PaymentMethodBase: Clase base que define los atributos comunes de la forma de pago

- PaymentMethodCreate: Clase que hereda de PaymentMethodBase y define los atributos de la forma de pago para crear una nueva

- PaymentMethodUpdate: Clase que hereda de BaseModel y define los atributos de la forma de pago para actualizar una existente (Reemplazo completo)

- PaymentMethodPatch: Clase que hereda de BaseModel y define los atributos de la forma de pago para actualizar una existente (Actualización parcial)

- PaymentMethodResponse: Clase que hereda de PaymentMethodBase y define los atributos de la forma de pago para devolverlo como respuesta
"""
class PaymentMethodBase(BaseModel):
    """Atributos comunes compartidos por la entidad PaymentMethod."""
    payment: PaymentNameType


class PaymentMethodCreate(PaymentMethodBase):
    """Esquema utilizado para registrar un nuevo método de pago (POST)."""
    pass


class PaymentMethodUpdate(PaymentMethodBase):
    """Esquema para la actualización completa del método de pago (PUT)."""
    pass


class PaymentMethodPatch(BaseModel):
    """Esquema para la actualización parcial del método de pago (PATCH)."""
    payment: Optional[PaymentNameType] = None
    is_active: Annotated[
        Optional[bool], 
        Field(None, description="Estado de borrado lógico")
    ] = None


class PaymentMethodResponse(PaymentMethodBase):
    """Esquema de salida devuelto en las lecturas y respuestas del sistema (GET, POST, PUT, PATCH)."""
    payment_id: PaymentIDType
    is_active: Annotated[
        bool, 
        Field(True, description="Indicador de estado / Soft Delete")
    ] = True

    # Permite mapear automáticamente desde modelos de ORM como SQLAlchemy
    model_config = ConfigDict(from_attributes=True)