
from pydantic import BaseModel, Field, field_validator
from typing import Optional


class ProvisionalSituation(BaseModel):
    """
    Institution class to validate user data for the Situacion Previsional table
    """

    obra_social: str = Field(...)
    numero_afiliado: int = Field(...)
    tiene_curatela: bool = Field(...)
    observaciones: Optional[str] = Field(None)

    @field_validator("obra_social")
    def validate_obra_social(cls, value):
        if not value:
            raise ValueError("Obra social es requerido")
        return value

    @field_validator("numero_afiliado")
    def validate_numero_afiliado(cls, value):
        if value <= 0:
            raise ValueError("El número de afiliado debe ser positivo")
        return value

    @field_validator("tiene_curatela")
    def validate_tiene_curatela(cls, value):
        if not value:
            raise ValueError("Tiene curatela es requerido")
        return value


class PartialProvisionalSituation(BaseModel):
    """
    PartialMember class to validate the user data
    """

    obra_social: Optional[str] = Field(None)
    numero_afiliado: Optional[int] = Field(None)
    tiene_curatela: Optional[bool] = Field(None)
    observaciones: Optional[str] = Field(None)
