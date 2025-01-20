from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class FamilyMember(BaseModel):
    """
    FamilyMember class to validate the user data
    """

    nombre: str = Field(...)
    apellido: str = Field(...)
    dni: int = Field(...)
    domicilio_actual: str = Field(...)
    celular_actual: int = Field(...)
    email: str = Field(...)
    nivel_escolaridad: str = Field(...)
    actividad_ocupacion: str = Field(...)
    parentesco: str = Field(...)

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

    @field_validator("parentesco")
    def validate_parentesco(cls, value):
        if not value:
            raise ValueError("Parentesco es requerido")
        return value

    @field_validator("dni")
    def validate_dni(cls, value):
        if value <= 0:
            raise ValueError("DNI debe ser un número positivo")
        return value

    @field_validator("domicilio_actual")
    def validate_domicilio_actual(cls, value):
        if not value:
            raise ValueError("Domicilio actual es requerido")
        return value

    @field_validator("nivel_escolaridad")
    def validate_nivel_escolaridad(cls, value):
        if not value:
            raise ValueError("Nivel de escolaridad es requerido")
        return value

    @field_validator("actividad_ocupacion")
    def validate_actividad_ocupacion(cls, value):
        if not value:
            raise ValueError("Debe ingresar una actividad/ocupación")
        return value

    @field_validator("celular_actual")
    def validate_celular_actual(cls, value):
        if value <= 0:
            raise ValueError("El número de teléfono debe ser positivo")
        return value

    @field_validator("email")
    def validate_email(cls, value):
        if not value:
            raise ValueError("Email es requerido")
        return value
