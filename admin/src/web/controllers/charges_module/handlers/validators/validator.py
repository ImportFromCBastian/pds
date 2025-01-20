from src.core.models.charges_module.charge import Cobro
from src.core.models.riders import exists_rider
from src.core.models.teams import search_by_dni
from src.core.models.teams.employee import Empleado
from src.web.controllers.charges_module.handlers.validators.charge import Charge, PartialCharge
from pydantic import ValidationError


def validate_charge(object):
    """
    Validates the charge data. \n
    Return true if the charge data is valid for insert, false otherwise
    """
    errors = {"valid": True, "errors": []}
    
    try:
        charge = Charge(**object)
    except ValidationError as e:
        errors["valid"] = False
        errors["errors"] = e.errors()

        return errors
    
    
    if not exists_rider(object["dni_equitador"]):
        errors["valid"] = False
        errors["errors"].append(
            {"loc": ("dni_equitador",), "msg": "El J&A ingresado no existe",
             "type": "value_error"}
        )
    
    if not search_by_dni(object["dni_empleado"]):
        errors["valid"] = False
        errors["errors"].append(
            {"loc": ("dni_empleado",), "msg": "El Empleado ingresado no existe",
             "type": "value_error"}
        )

    return errors


def validate_partial_charge(object):
    """
    Validates the charge data. \n
    Return true if the charge data is valid for insert, false otherwise
    """
    errors = {"valid": True, "errors": []}
    
    try:
        charge = PartialCharge(**object)
    except ValidationError as e:
        errors["valid"] = False
        errors["errors"] = e.errors()

        return errors
    
    
    if not exists_rider(object["dni_equitador"]):
        errors["valid"] = False
        errors["errors"].append(
            {"loc": ("dni_equitador",), "msg": "El J&A ingresado no existe",
             "type": "value_error"}
        )
    
    if not search_by_dni(object["dni_empleado"]):
        errors["valid"] = False
        errors["errors"].append(
            {"loc": ("dni_empleado",), "msg": "El Empleado ingresado no existe",
             "type": "value_error"}
        )

    return errors