
from pydantic import BaseModel, Field, field_validator
from typing import Optional


class Institution(BaseModel):
    """
    Institution class to validate user data for the Equitador table
    """

    nombre: str = Field(...)
    direccion: str = Field(...)
    telefono: int = Field(...)
    grado_actual: str = Field(...)
    observaciones: Optional[str] = Field(None)

    @field_validator("nombre")
    def validate_nombre(cls, value):
        if not value:
            raise ValueError("Nombre es requerido")
        return value

    @field_validator("direccion")
    def validate_domicilio_actual(cls, value):
        if not value:
            raise ValueError("Domicilio actual es requerido")
        return value

    @field_validator("telefono")
    def validate_telefono(cls, value):
        if value <= 0:
            raise ValueError("El número de teléfono debe ser positivo")
        return value

    @field_validator("grado_actual")
    def validate_grado_actual(cls, value):
        if not value:
            raise ValueError("Grado actual es requerido")
        return value


class PartialInstitution(BaseModel):
    """
    PartialMember class to validate the user data
    """

    nombre: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[int] = None
    grado_Actual: Optional[str] = None
    observaciones: Optional[str] = None
