from src.core.models.users_module.user import Usuario
from src.web.controllers.users_module.handlers.validators.user import User, PartialUser
from pydantic import ValidationError

def validate_user(object) -> dict:
    """
    Validates the user data \n
    : return : true if the user is valid for insert, false otherwise
    """
    errors = {"valid": True, "errors": []}
    try:
        user = User(**object)
    except ValidationError as e:
        errors["valid"] = False
        errors["errors"] = e.errors()

        return errors
    
    if Usuario.query.filter(Usuario.email == object["email"]).first():
        errors["valid"] = False
        errors["errors"].append(
            {"loc": ("email",), "msg": "El email ingresado ya existe en el sistema. Debe ser único",
             "type": "value_error"}
        )
        
    return errors


def validate_partial_user(object) -> dict:
    """
    Validates the partial user data to update it \n
    return true if the data is valid for update, false otherwise
    """
    from web.controllers.contact_module.handlers.validators.contact import PartialContact
    errors = {"valid": True, "errors": []}
    
    try:
        query = PartialUser(**object)
    except ValidationError as e:
        errors["valid"] = False
        errors["errors"] = e.errors()
        return errors
    
    return errors
