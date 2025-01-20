from pydantic import BaseModel, Field, EmailStr, ValidationError, field_validator
from datetime import datetime
from typing import Optional


class Contact(BaseModel):
    """
    Query class to validate the data to create a new portal query
    """
    title: str = Field(...)
    email: EmailStr = Field(...)
    description: str = Field(...)
    query_state: str = Field(...)
    created_at: str = Field(...)
    closed_at: str = Field(...)

    @field_validator("title")
    def validate_title(cls, value):
        if not value:
            raise ValueError("El título es requerido")
        return value
    
    @field_validator("email")
    def validate_email(cls, value):
        if not value:
            raise ValueError("El email es requerido")
        return value

    @field_validator("description")
    def validate_description(cls, value):
        if not value:
            raise ValueError("La descripción es requerida")
        return value

    @field_validator("query_state")
    def validate_query_state(cls, value):
        if not value:
            raise ValueError("El estado es requerido")
        if value != "Creada":
            raise ValueError("El estado debe ser uno valido")
        return value

    @field_validator("created_at")
    def validate_created_at(cls, value):
        if not value:
            raise ValueError("La fecha de creación es requerida")
        
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("la fecha de creacion debe tener un formato válido")
        return value
    
    @field_validator("closed_at")
    def validate_closed_at(cls, value):
        if not value:
            raise ValueError("La fecha de conclusion es requerida")
        
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("la fecha de conclusion debe tener un formato válido")
        return value


class PartialContact(BaseModel):
    """
    Query class to validate the data to update a portal query
    """
    query_state: Optional[str]
    query_coment: Optional[str]
    
    @field_validator("query_state")
    def validate_query_state_update(cls, value):
        if value and value not in ["Creada", "Atendida", "Pendiente"]:
            raise ValueError("El estado debe ser uno válido")
        return value
