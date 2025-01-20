
from pydantic import ValidationError


def validate_content(object) -> dict:
    """
    Validates the content data 
    : return : true if the content is valid, false otherwise
    """
    from web.controllers.content.validators.content import Content
    errors = {"valid": True, "errors": []}

    try:
        content = Content(**object)
    except ValidationError as e:
        errors["valid"] = False
        errors["errors"] = e.errors()
        return errors
    return errors


def validate_partial_content(object) -> bool:
    """
    Validates the content data
    : return : true if the content is valid for update, false otherwise
    """
    from web.controllers.content.validators.content import PartialContent

    errors = {"valid": True, "errors": []}

    try:
        content = PartialContent(**object)
    except ValidationError as e:
        errors["valid"] = False
        errors["errors"] = e.errors()
        return errors

    return errors
