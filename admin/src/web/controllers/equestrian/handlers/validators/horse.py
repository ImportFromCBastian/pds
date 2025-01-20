from pydantic import BaseModel, Field, field_validator, EmailStr
from typing import Optional
from datetime import datetime


class Horse(BaseModel):
    """
    Horse class to validate the user data
    """

    nombre: str = Field(...)
    fecha_nacimiento: datetime
    sexo: str = Field(...)
    raza: str = Field(...)
    pelaje: str = Field(...)
    compra_donacion: str = Field(...)
    fecha_ingreso: datetime
    tipo_de_JyA_asignado: str = Field(...)
    sede_asignada: str = Field(...)

    @field_validator("nombre")
    def validate_nombre(cls, value):
        if not value:
            raise ValueError("Nombre es requerido")
        return value

    @field_validator("fecha_nacimiento")
    def validate_fecha_nacimiento(cls, value):
        if not value:
            raise ValueError("Fecha de nacimiento es requerido")
        return value

    @field_validator("sexo")
    def validate_sexo(cls, value):
        if not value:
            raise ValueError("Sexo es requerido")
        return value

    @field_validator("raza")
    def validate_raza(cls, value):
        if not value:
            raise ValueError("Raza es requerido")
        return value
    
    @field_validator("pelaje")
    def validate_pelaje(cls, value):
        if not value:
            raise ValueError("Pelaje es requerido")
        return value

    @field_validator("compra_donacion")
    def validate_compra_donacion(cls, value):
        if not value:
            raise ValueError("Compra o donacion es requerido")
        return value

    @field_validator("fecha_ingreso")
    def validate_fecha_ingreso(cls, value):
        if not value:
            raise ValueError("Fecha de ingreso es requerido")
        return value
    
    @field_validator("tipo_de_JyA_asignado")
    def validate_tipo_de_JyA_asignado(cls, value):
        if not value:
            raise ValueError("Tipo de JyA asignado es requerido")
        return

    @field_validator("sede_asignada")
    def validate_sede_asignada(cls, value):
        if not value:
            raise ValueError("Sede asignada es requerido")
        return value


class PartialHorse(BaseModel):
    """
    PartialHorse class to validate
    """
    
    nombre: Optional[str]
    fecha_nacimiento: Optional[datetime]
    sexo: Optional[str]
    raza: Optional[str]
    compra_donacion: Optional[str]
    fecha_ingreso: Optional[datetime]
    sede_asignada: Optional[str]
