from pydantic import BaseModel, Field, field_validator, EmailStr
from typing import Optional
from datetime import datetime


class Member(BaseModel):
    """
    Member class to validate the user data
    """

    email: EmailStr = Field(...)
    dni: int = Field(...)
    nombre: str = Field(...)
    apellido: str = Field(...)
    telefono: int = Field(...)
    domicilio: str = Field(...)
    localidad: str = Field(...)
    profesion: str = Field(...)
    puesto_laboral: str = Field(...)
    condicion: str = Field(...)
    activo: bool
    numero_afiliado: int = Field(...)
    numero_emergencia: int = Field(...)
    nombre_emergencia: str = Field(...)
    fecha_inicio: datetime

    @field_validator("email")
    def validate_email(cls, value):
        if not value:
            raise ValueError("Email es requerido")
        return value

    @field_validator("dni")
    def validate_dni(cls, value):
        if not value or value < 0:
            raise ValueError("DNI es requerido")
        return value

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

    @field_validator("profesion")
    def validate_profesion(cls, value):
        if not value:
            raise ValueError("Profesion es requerido")
        return value

    @field_validator("puesto_laboral")
    def validate_puesto_laboral(cls, value):
        if not value:
            raise ValueError("Puesto laboral es requerido")
        return value

    @field_validator("condicion")
    def validate_condicion(cls, value):
        if not value:
            raise ValueError("Condicion es requerido")
        return value

    @field_validator("numero_afiliado")
    def validate_numero_afiliado(cls, value):
        if not value or value < 0:
            raise ValueError("Numero afiliado es requerido")
        return value

    @field_validator("numero_emergencia")
    def validate_numero_emergencia(cls, value):
        if not value or value < 0:
            raise ValueError("Numero emergencia es requerido")
        return value

    @field_validator("nombre_emergencia")
    def validate_nombre_emergencia(cls, value):
        if not value:
            raise ValueError("Nombre emergencia es requerido")
        return value

    @field_validator("activo")
    def validate_activo(cls, value):
        if value == "off":
            return False
        else:
            return True

    @field_validator("localidad")
    def validate_localidad(cls, value):
        if not value:
            raise ValueError("Localidad es requerido")
        return value

    @field_validator("telefono")
    def validate_telefono(cls, value):
        if not value or value < 0:
            raise ValueError("Telefono es requerido")
        return value

    @field_validator("domicilio")
    def validate_domicilio(cls, value):
        if not value:
            raise ValueError("Domicilio es requerido")
        return value


class PartialMember(BaseModel):
    """
    PartialMember class to validate the user data
    """

    nombre: Optional[str]
    apellido: Optional[str]
    profesion: Optional[str]
    condicion: Optional[str]
    puesto_laboral: Optional[str]
    activo: Optional[bool]
    numero_emergencia: Optional[int]
    nombre_emergencia: Optional[str]
