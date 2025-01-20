from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional


class PaymentModel(BaseModel):
    """
    Payment class to validate payment data.
    """

    beneficiario: int = Field(..., description="ID del beneficiario")
    tipo_pago: str = Field(..., description="Tipo de pago")
    monto: float = Field(..., description="Monto del pago")
    fecha_pago: datetime = Field(..., description="Fecha del pago")
    descripcion: Optional[str] = Field(description="Descripción del pago")

    @field_validator("beneficiario", mode="before")
    def validate_beneficiary(cls, value):
        if isinstance(value, str):
            try:
                value = int(value)
            except ValueError:
                raise ValueError("El beneficiario debe ser uno valido.")
        if value <= 0:
            raise ValueError("El beneficiario debe ser un ID válido.")
        return value

    @field_validator("tipo_pago", mode="before")
    def validate_payment_type(cls, value):
        if not value:
            raise ValueError("El tipo de pago es requerido.")
        return value

    @field_validator("monto", mode="before")
    def validate_amount(cls, value):
        if isinstance(value, str):
            try:
                value = float(value)
            except ValueError:
                raise ValueError("El monto debe ser un número válido.")
        if value <= 0:
            raise ValueError("El monto debe ser mayor a 0.")
        return value

    @field_validator("fecha_pago", mode="before")
    def validate_date(cls, value):
        if isinstance(value, str):
            try:
                value = datetime.fromisoformat(value)
            except ValueError:
                raise ValueError("Formato de fecha incorrecto.")
        return value


class PartialPaymentModel(BaseModel):
    """
    Partial payment class to validate partial payment data.
    """

    monto: Optional[float] = Field(None, description="Monto del pago")
    descripcion: Optional[str] = Field(
        None, description="Descripción del pago")
    tipo_pago: Optional[str] = Field(None, description="Tipo de pago")
    fecha_pago: Optional[datetime] = Field(None, description="Fecha del pago")
