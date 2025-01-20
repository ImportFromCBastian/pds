from src.core.models.contact_module import PortalQuery
from pydantic import ValidationError


def validate_portal_query(object) -> dict:
    """
    Validates the portal query data \n
    return true if the portal query is valid for insert, false otherwise
    """
    from web.controllers.contact_module.handlers.validators.contact import Contact
    
    errors = {"valid": True, "errors": []}
    
    try:
        query = Contact(**object)
    except ValidationError as e:
        errors["valid"] = False
        errors["errors"] = e.errors()
        return errors
    
    return errors


def validate_partial_portal_query(object) -> dict:
    """
    Validates the partial portal query data to update it \n
    return true if the data is valid for update, false otherwise
    """
    from web.controllers.contact_module.handlers.validators.contact import PartialContact
    errors = {"valid": True, "errors": []}
    
    try:
        query = PartialContact(**object)
    except ValidationError as e:
        errors["valid"] = False
        errors["errors"] = e.errors()
        return errors
    
    return errors
