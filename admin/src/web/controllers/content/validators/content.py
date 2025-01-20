from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional
from datetime import datetime
from enum import Enum


class EstadoType(str, Enum):
    borrador = "Borrador"
    publicado = "Publicado"
    archivado = "Archivado"


class Content(BaseModel):
    """
    Content class to validate the data for content creation.
    """
    titulo: str = Field(min_length=1, max_length=100)
    copete: str = Field(min_length=1, max_length=200)
    contenido: str = Field(min_length=1)
    estado: str = Field()
    fecha_publicacion: Optional[datetime] = Field(None)
    autor_email: str = Field()

    @field_validator("titulo")
    def validate_titulo(cls, value):
        if not value:
            raise ValueError("El título es requerido y no puede estar vacío.")
        return value

    @field_validator("copete")
    def validate_copete(cls, value):
        if not value:
            raise ValueError("El copete es requerido y no puede estar vacío.")
        return value

    @field_validator("contenido")
    def validate_contenido(cls, value):
        if not value:
            raise ValueError(
                "El contenido es requerido y no puede estar vacío.")
        return value

    @field_validator("estado")
    def validate_estado(cls, value):
        if value not in EstadoType:
            raise ValueError(f"Estado '{
                             value}' no es válido. Debe ser 'Borrador', 'Publicado' o 'Archivado'.")
        return value


class PartialContent(BaseModel):
    """
    PartialContent class to validate partial updates to content.
    """

    titulo: Optional[str] = Field(None, min_length=1, max_length=100)
    copete: Optional[str] = Field(None, min_length=1, max_length=200)
    contenido: Optional[str] = Field(None, min_length=1)
    estado: Optional[str] = Field(None)
    fecha_publicacion: Optional[datetime] = Field(None)
    autor_email: Optional[EmailStr] = Field(None)

    @field_validator("estado")
    def validate_estado(cls, value):
        if not value:
            raise ValueError("Estado es requerido")
        elif value not in EstadoType:
            raise ValueError(f"Estado '{
                             value}' no es válido. Debe ser 'Borrador', 'Publicado' o 'Archivado'.")
        return value
