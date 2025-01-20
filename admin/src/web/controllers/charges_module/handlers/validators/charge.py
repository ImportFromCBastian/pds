from pydantic import BaseModel, Field, EmailStr, ValidationError, field_validator
from datetime import datetime
from typing import Optional
from src.core.models.charges_module.charge import PayMethod


class Charge(BaseModel):
    """
    Charge class to validate the data to create a new charge
    """
    dni_equitador: int = Field(...)
    fecha_pago: str = Field(...)
    medio_de_pago: str = Field(...)
    monto: float = Field(...)
    dni_empleado: int = Field(...)
    observaciones: str
    
    @field_validator("dni_equitador")
    def validate_dni_equitador(cls, value):
        if not value or value < 0:
            raise ValueError("El DNI del J&A del cobro es requerido")
        return value
    
    @field_validator("fecha_pago")
    def validate_fecha_pago(cls, value):
        if not value:
            raise ValueError("La fecha de pago del cobro es requerida")
        
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("la fecha de pago del cobro debe tener un formato válido")
        return value
    
    @field_validator("medio_de_pago")
    def validate_medio_de_pago(cls, value):
        if not value:
            raise ValueError("El medio de pago del cobro es requerido")
        pay_methods = [pay_method.name for pay_method in PayMethod ]
        if value not in pay_methods:
            raise ValueError("El medio de pago del cobro debe ser uno valido")
        return value
    
    @field_validator("monto")
    def validate_monto(cls, value):
        if not value:
            raise ValueError("El monto del cobro es requerido")
        
        if len(str(abs(value))) > 10:
            raise ValueError("El monto no debe tener más de 10 dígitos")
        
        return value
    
    @field_validator("dni_empleado")
    def validate_dni_empleado(cls, value):
        if not value or value < 0:
            raise ValueError("El DNI del Empleado del cobro es requerido")
        return value
    

class PartialCharge(BaseModel):
    """
    Charge class to validate the data to update a charge
    """
    dni_equitador: Optional[int]
    fecha_pago: Optional[str]
    medio_de_pago: Optional[str]
    monto: Optional[float]
    dni_empleado: Optional[int]
    observaciones: Optional[str]
    
    @field_validator("dni_equitador")
    def validate_dni_equitador(cls, value):
        if not value or value < 0:
            raise ValueError("El DNI del J&A del cobro es requerido")
        return value
    
    @field_validator("fecha_pago")
    def validate_fecha_pago(cls, value):
        if value:
            try:
                datetime.strptime(value, "%Y-%m-%d")
            except ValueError:
                raise ValueError("la fecha de pago del cobro debe tener un formato válido")
            return value
    
    @field_validator("medio_de_pago")
    def validate_medio_de_pago(cls, value):
        if not value:
            raise ValueError("El medio de pago del cobro es requerido")
        pay_methods = [pay_method.name for pay_method in PayMethod ]
        if value not in pay_methods:
            raise ValueError("El medio de pago del cobro debe ser uno valido")
        return value
    
    @field_validator("monto")
    def validate_monto(cls, value):
        if not value:
            raise ValueError("El monto del cobro es requerido")
        
        if len(str(abs(value))) > 10:
            raise ValueError("El monto no debe tener más de 10 dígitos")
        
        return value
    
    @field_validator("dni_empleado")
    def validate_dni_empleado(cls, value):
        if not value or value < 0:
            raise ValueError("El DNI del Empleado del cobro es requerido")
        return value