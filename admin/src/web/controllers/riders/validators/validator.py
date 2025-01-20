from datetime import datetime
from pydantic import ValidationError

from src.core.models import riders

from web.controllers.riders.validators.rider import Rider, PartialRider
from web.controllers.riders.validators.institution import Institution, PartialInstitution
from web.controllers.riders.validators.work import PartialWork, Work
from src.core.models.riders.rider import Equitador
from web.controllers.riders.validators.familyMember import FamilyMember
from web.controllers.riders.validators.provisionalSituation import PartialProvisionalSituation, ProvisionalSituation


def validate_rider(object) -> dict:
    """
    Validates the rider data
    : return : true if the rider is valid for insert, false otherwise
    """
    errors = {"valid": True, "errors": []}

    try:
        object = preprocess_input(object)
        rider = Rider(**object)
    except ValidationError as e:
        errors["errors"] = clean_validation_errors(e.errors())
        errors["valid"] = False
        return errors

    if riders.exists_rider(object["dni"]):
        errors["valid"] = False
        errors["errors"].append(
            {"loc": ("dni",), "msg": "DNI ya existe", "type": "value_error"}
        )
    return errors


def validate_institution(object) -> dict:
    """
    Validates the institution data
    : return : true if the institution is valid for insert, false otherwise
    """
    errors = {"valid": True, "errors": []}

    try:

        institution = Institution(**object)
    except ValidationError as e:
        errors["errors"] = clean_validation_errors(e.errors())
        errors["valid"] = False
        return errors

    return errors


def validate_provisional_situation(object) -> dict:
    """
    Validates the provisional situation data
    : return : true if the provisional situation is valid for insert, false otherwise
    """
    errors = {"valid": True, "errors": []}

    try:

        provisional_situation = ProvisionalSituation(**object)
    except ValidationError as e:
        errors["errors"] = clean_validation_errors(e.errors())
        errors["valid"] = False
        return errors

    return errors


def validate_work(object) -> dict:
    """
    Validates the work data
    : return : true if the work is valid for insert, false otherwise
    """
    errors = {"valid": True, "errors": []}

    try:

        work = Work(**object)
    except ValidationError as e:
        errors["errors"] = clean_validation_errors(e.errors())
        errors["valid"] = False
        return errors
    return errors


def validate_family_member(object) -> bool:
    """
    Validates the family member data
    : return : true if the family member is valid for insert, false otherwise
    """
    errors = {"valid": True, "errors": []}

    try:

        family_member = FamilyMember(**object)
    except ValidationError as e:
        errors["errors"] = clean_validation_errors(e.errors())
        errors["valid"] = False

        return errors

    return errors


def preprocess_input(data):
    """
    Preprocess the input data to match the expected types for the PartialRider model.
    """
    if 'dni' in data:
        data['dni'] = int(data['dni'])

    if 'fecha_nacimiento' in data:
        data['fecha_nacimiento'] = datetime.strptime(
            data['fecha_nacimiento'], '%Y-%m-%d')

    return data


def validate_partial_rider(object) -> bool:
    """
    Validates the rider data for updates
    : return : true if the rider is valid for update, false otherwise
    """

    errors = {"valid": True, "errors": []}
    object = preprocess_input(object)
    try:
        rider = PartialRider(**object)
    except ValidationError as e:
        errors["errors"] = clean_validation_errors(e.errors())
        errors["valid"] = False

        return errors
    except Exception as ex:

        errors["valid"] = False
        errors["errors"].append(
            {"msg": "Unexpected error occurred", "details": str(ex)})
        return errors

    return errors


def validate_partial_institution(object) -> bool:
    """
    Validates the institution data for updates
    : return : true if the institution is valid for update, false otherwise
    """
    errors = {"valid": True, "errors": []}
    try:
        Institution = PartialInstitution(**object)
    except ValidationError as e:
        errors["errors"] = clean_validation_errors(e.errors())
        errors["valid"] = False

        return errors
    except Exception as ex:
        errors["valid"] = False
        errors["errors"].append(
            {"msg": "Unexpected error occurred", "details": str(ex)})
        return errors
    return errors


def validate_partial_provisional_situation(object) -> bool:
    """
    Validates the previtional situation data for updates
    : return : true if the previtional situation is valid for update, false otherwise
    """
    errors = {"valid": True, "errors": []}
    try:
        provisional_situation = PartialProvisionalSituation(**object)
    except ValidationError as e:
        errors["errors"] = clean_validation_errors(e.errors())
        errors["valid"] = False

        return errors
    except Exception as ex:
        errors["valid"] = False
        errors["errors"].append(
            {"msg": "Unexpected error occurred", "details": str(ex)})
        return errors
    return errors


def validate_partial_work(object) -> bool:
    """
    Validates the work data for updates
    : return : true if the work is valid for update, false otherwise
    """
    errors = {"valid": True, "errors": []}
    try:
        work = PartialWork(**object)
    except ValidationError as e:
        errors["errors"] = clean_validation_errors(e.errors())
        errors["valid"] = False

        return errors
    except Exception as ex:
        errors["valid"] = False
        errors["errors"].append(
            {"msg": "Unexpected error occurred", "details": str(ex)})
        return errors
    return errors


def clean_validation_errors(errors):
    """
    Cleans the validation errors by removing unnecessary prefixes.
    :param errors: List of errors returned by Pydantic ValidationError
    :return: List of cleaned errors
    """
    cleaned_errors = []
    for err in errors:
        error_message = err["msg"].replace(
            "Value error, ", "")
        cleaned_errors.append({
            "loc": err["loc"],
            "msg": error_message
        })
    return cleaned_errors
