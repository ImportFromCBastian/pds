from src.core.models import teams
from web.controllers.teams.handlers.validators.member import Member, PartialMember
from src.core.models.users_module.user import Usuario
from pydantic import ValidationError


def validate_user(object) -> dict:
    """
    Validates the user data \n
    : return : true if the user is valid for insert, false otherwise
    """
    errors = {"valid": True, "errors": []}

    try:
        object = object.to_dict()

        if not object.get("activo"):
            object["activo"] = "off"

        if not object.get("fecha_inicio"):
            object["fecha_inicio"] = None

        member = Member(**object)
    except ValidationError as e:
        errors["valid"] = False
        errors["errors"] = e.errors()

        return errors

    # Validar email y dni en base de datos
    if teams.search_by_email(object["email"]) or Usuario.get_user(object["email"]):
        errors["valid"] = False
        errors["errors"].append(
            {"loc": ("email",), "msg": "Email ya existe",
             "type": "value_error"}
        )

    if teams.search_by_dni(object["dni"]):
        errors["valid"] = False
        errors["errors"].append(
            {"loc": ("dni",), "msg": "DNI ya existe", "type": "value_error"}
        )

    if teams.search_by_number(object["numero_afiliado"]):
        errors["valid"] = False
        errors["errors"].append(
            {
                "loc": ("numero_afiliado",),
                "msg": "Numero de afiliado ya existe",
                "type": "value_error",
            }
        )

    return errors


def validate_partial_user(object) -> bool:
    """
    Validates the user data \n
    : return : true if the user is valid for update, false otherwise
    """
    errors = {"valid": True, "errors": []}

    # parsing data that cannot be coersed by pydantic
    object["numero_emergencia"] = (
        int(object.get("numero_emergencia")) if object.get(
            "numero_emergencia") else 0
    )
    object["activo"] = True if object.get("activo") == "on" else False

    try:
        member = PartialMember(**object)
    except ValidationError as e:
        errors["valid"] = False
        errors["errors"] = e.errors()

        return errors

    return errors
