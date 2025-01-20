from flask import request
from src.core.models import equestrian
from src.core.models import teams
from web.controllers.equestrian.handlers.validators.horse import Horse, PartialHorse
from src.core.models.equestrian.Horse import Caballo
from pydantic import ValidationError



def validate_horse(object) -> dict:
    """
    Validates the horse data
    : return : true if the user is valid for insert, false otherwise
    """
    errors = {"valid": True, "errors": []}

    try:
        object = object.to_dict()  
        horse = Horse(**object)
    except ValidationError as e:
        errors["valid"] = False
        errors["errors"] = e.errors()

        return errors

    if not teams.search_by_dni(object["dni"]):
        errors["valid"] = False
        errors["errors"].append(
            {"loc": ("dni",), "msg": "DNI no encontrado", "type": "value_error"}
        )

    return errors


def validate_partial_horse(object) -> bool:
    """
    Validates partial horse data \n
    : return : true if the user is valid for update, false otherwise
    """
    errors = {"valid": True, "errors": []}
    
    try:
        horse = PartialHorse(**object)
    except ValidationError as e:
        errors["valid"] = False
        errors["errors"] = e.errors()
        return errors
    
    # Obtener la lista de DNIs como una lista
    empleados = object.get("empleados_dni", "").split(',')  # Cambiado a "empleados_dni"
    
    for dni in empleados:
        dni = dni.strip()  # Eliminar espacios en blanco
        if not dni:
            errors["valid"] = False
            errors["errors"].append(
                {"loc": ("empleados_dni",), "msg": "DNI no puede estar vacío", "type": "value_error"}
            )
        elif not teams.search_by_dni(dni):
            errors["valid"] = False
            errors["errors"].append(
                {"loc": ("empleados_dni",), "msg": f"DNI {dni} no encontrado", "type": "value_error"}
            )
    
    return errors


