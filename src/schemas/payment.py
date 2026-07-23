from typing import Annotated, Optional
from pydantic import BaseModel, ConfigDict, Field

# ==========================================
# TIPOS REUTILIZABLES CON ANNOTATED
# ==========================================

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


# ==========================================
# ESQUEMAS PRINCIPALES DE PAYMENT METHOD
# ==========================================

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