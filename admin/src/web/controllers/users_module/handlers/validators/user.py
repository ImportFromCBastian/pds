from pydantic import BaseModel, Field, EmailStr, ValidationError, field_validator
from datetime import datetime
from typing import Optional


class User(BaseModel):
    """
    User class to validate the data to create a new user
    """
    email: EmailStr = Field(...)
    password: str = Field(...)
    alias: str = Field(...)
    bloqueado: bool = Field(...)
    system_admin: bool = Field(...)
    rol_id: int = Field(...)
    
    @field_validator("email")
    def validate_email(cls, value):
        if not value:
            raise ValueError("Email es requerido")
        return value
    
    @field_validator("password")
    def validate_contrasenia(cls, value):
        if not value:
            raise ValueError("Contrasenia es requerido")
        return value
    
    @field_validator("alias")
    def validate_alias(cls, value):
        if not value:
            raise ValueError("Alias es requerido")
        return value
    
    @field_validator("bloqueado")
    def validate_bloqueado(cls, value):
        if value == "False":
            return False
        else:
            return True
        
    @field_validator("system_admin")
    def validate_system_admin(cls, value):
        if value == "False":
            return False
        else:
            return True
        
    @field_validator("rol_id")
    def validate_rol_id(cls, value):
        if not value:
            raise ValueError("Rol es requerido")
        value = int(value)
        if value not in [1, 2, 3, 4]:
            raise ValueError("El Rol debe ser uno válido")
        return int(value)
    
    
class PartialUser(BaseModel):
    alias: Optional[str]
    rol_id: Optional[int]
    
    @field_validator("rol_id")
    def validate_rol_id(cls, value):
        if not value:
            raise ValueError("Rol es requerido")
        value = int(value)
        if value not in [1, 2, 3, 4]:
            raise ValueError("El Rol debe ser uno válido")
        return int(value)