from pydantic import BaseModel, Field, field_validator
from typing import Optional


class Work(BaseModel):
    """
    Institution class to validate user data for the Situacion Previsional table
    """

    tipo_trabajo: str = Field(...)
    condicion: str = Field(...)
    sede: str = Field(...)
    dia: str = Field(...)
    profesor_terapeuta_id: int = Field(...)
    conductor_caballo_id: int = Field(...)
    auxiliar_pista_id: int = Field(...)
    caballo_id: int = Field(...)

    @field_validator("tipo_trabajo")
    def validate_tipo_trabajo(cls, value):
        if not value or not isinstance(value, str):
            raise ValueError(
                "El tipo de trabajo es requerido y debe ser una cadena válida")
        return value

    @field_validator("condicion")
    def validate_condicion(cls, value):
        if not value:
            raise ValueError(
                "La condición es requerida")
        return value

    @field_validator("sede")
    def validate_sede(cls, value):
        if not value:
            raise ValueError(
                "La sede es requerida")
        return value

    @field_validator("dia")
    def validate_dia(cls, value):
        if not value:
            raise ValueError(
                "El día es requerido")
        return value

    @field_validator("profesor_terapeuta_id")
    def validate_profesor_terapeuta_id(cls, value):
        if not value:
            raise ValueError(
                "El profesor terapeuta es requerido")
        return value

    @field_validator("conductor_caballo_id")
    def validate_conductor_caballo_id(cls, value):
        if not value:
            raise ValueError(
                "El conductor de caballo es requerido")
        return value

    @field_validator("auxiliar_pista_id")
    def validate_auxiliar_pista_id(cls, value):
        if not value:
            raise ValueError(
                "El auxiliar de pista es requerido")
        return value

    @field_validator("caballo_id")
    def validate_caballo_id(cls, value):
        if not value:
            raise ValueError(
                "El caballo es requerido")
        return value


class PartialWork(BaseModel):
    """
    PartialMember class to validate the user data
    """
    tipo_trabajo: Optional[str] = None
    condicion: Optional[str] = None
    sede: Optional[str] = None
    # no me está validando que no esté vacío y no sé por qué
    dia:  Optional[str] = None
    profesor_terapeuta_id: Optional[int] = None
    conductor_caballo_id: Optional[int] = None
    auxiliar_pista_id: Optional[int] = None
    caballo_id: Optional[int] = None

    @field_validator("dia")
    def validate_dia(cls, value):
        if not value:
            raise ValueError("Dia es requerido")
        return value
