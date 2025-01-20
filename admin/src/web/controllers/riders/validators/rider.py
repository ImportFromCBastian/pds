from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class Rider(BaseModel):
    """
    Rider class to validate user data for the Equitador table
    """

    nombre: str = Field(...)
    apellido: str = Field(...)
    dni: int = Field(...)
    fecha_nacimiento: datetime = Field(...)
    lugar_nacimiento: str = Field(...)
    domicilio_actual: str = Field(...)
    telefono: int = Field(...)
    numero_emergencia: int = Field(...)
    nombre_emergencia: str = Field(...)
    becado: bool = Field(...)
    porcentaje_beca: Optional[int] = Field(None)
    observaciones: Optional[str] = Field(None)
    certificado_discapacidad: bool = Field(...)
    diagnostico_discapacidad: Optional[str] = Field(None)
    otro_diagnostico: Optional[str] = Field(None)
    tipo_discapacidad: str = Field(...)
    recibe_asignacion: bool = Field(...)
    tipo_asignacion: Optional[str] = Field(None)
    recibe_pension: bool = Field(...)
    tipo_pension: Optional[str] = Field(None)
    profesionales: str = Field(...)

    @field_validator("nombre")
    def validate_nombre(cls, value):
        if not value:
            raise ValueError("Nombre es requerido")
        return value

    @field_validator("apellido")
    def validate_apellido(cls, value):
        if not value:
            raise ValueError("Apellido es requerido")
        return value

    @field_validator("dni")
    def validate_dni(cls, value):
        if value <= 0:
            raise ValueError("DNI debe ser un número positivo")
        return value

    @field_validator("fecha_nacimiento")
    def validate_fecha_nacimiento(cls, value):
        if value > datetime.now():
            raise ValueError("Fecha de nacimiento no puede ser futura")
        return value

    @field_validator("domicilio_actual")
    def validate_domicilio_actual(cls, value):
        if not value:
            raise ValueError("Domicilio actual es requerido")
        return value

    @field_validator("telefono", "numero_emergencia")
    def validate_telefono(cls, value):
        if value <= 0:
            raise ValueError("El número de teléfono debe ser positivo")
        return value

    @field_validator("nombre_emergencia")
    def validate_nombre_emergencia(cls, value):
        if not value:
            raise ValueError("Nombre de emergencia es requerido")
        return value

    @field_validator("certificado_discapacidad", "recibe_asignacion", "recibe_pension", "becado")
    def validate_boolean(cls, value):
        if value is None:
            raise ValueError("Elige una opción")
        return value

    @field_validator("tipo_discapacidad")
    def validate_tipo_discapacidad(cls, value):
        if not value:
            raise ValueError("Tipo de discapacidad es requerido")
        return value

    @field_validator("profesionales")
    def validate_profesionales(cls, value):
        if not value:
            raise ValueError("Profesionales es requerido")
        return value


class PartialRider(BaseModel):
    """
    PartialMember class to validate the user data
    """

    nombre: Optional[str] = None
    apellido: Optional[str] = None
    fecha_nacimiento: Optional[datetime] = Field(None)
    lugar_nacimiento: Optional[str] = None
    domicilio_actual: Optional[str] = None
    telefono: Optional[int] = None
    numero_emergencia: Optional[int] = None
    nombre_emergencia: Optional[str] = None
    becado: Optional[bool] = None
    porcentaje_beca: Optional[int] = None
    observaciones: Optional[str] = None
    tiene_certificado: Optional[bool] = None
    diagnostico_discapacidad: Optional[str] = None
    otro_diagnostico: Optional[str] = None
    tipo_discapacidad: Optional[str] = None
    recibe_asignacion: Optional[bool] = None
    tipo_asignacion: Optional[str] = None
    recibe_pension: Optional[bool] = None
    tipo_pension: Optional[str] = None
    profesionales: Optional[str] = None

    @field_validator('fecha_nacimiento')
    def check_fecha_nacimiento(cls, value):
        if value is not None and value > datetime.now():
            raise ValueError(
                'La fecha de nacimiento no puede ser posterior a la fecha actual.')
        return value

    @field_validator("tipo_discapacidad")
    def validate_tipo_discapacidad(cls, value):
        if not value:
            raise ValueError("Tipo de discapacidad es requerido")
        return value
