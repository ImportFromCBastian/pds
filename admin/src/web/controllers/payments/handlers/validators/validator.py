from pydantic import ValidationError
from web.controllers.payments.handlers.validators.payment_service import (
    PaymentModel,
    PartialPaymentModel,
)


def validate_payment(object) -> dict:
    """
    Validates the payment data \n
    : return : true if the payment is valid for insert, false otherwise
    """

    errors = {"valid": True, "errors": []}

    try:
        object = object.to_dict()

        if not object.get("fecha_pago"):
            object["fecha_pago"] = None

        member = PaymentModel(**object)
    except ValidationError as e:
        errors["valid"] = False
        errors["errors"] = e.errors()

        return errors

    return errors


def validate_partial_payment(object) -> dict:
    """
    Validates the payment data \n
    : return : dict['valid']=true if the payment is valid for update, false otherwise
    """
    errors = {"valid": True, "errors": []}

    # parsing data that cannot be coersed by pydantic
    object["monto"] = int(object.get("monto")) if object.get("monto") else 0

    if not object.get("fecha_pago"):
        object["fecha_pago"] = None

    try:

        member = PartialPaymentModel(**object)
    except ValidationError as e:
        errors["valid"] = False
        errors["errors"] = e.errors()

        return errors

    return errors
