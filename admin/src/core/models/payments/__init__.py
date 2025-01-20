from src.core.models.payments.payment import Pago
from src.core.database import commit_db
from src.core.models.payments.handlers.update_payment import update as update_payment
from sqlalchemy import extract


def payment_index():
    """
    List all the payments.
    """
    payments = Pago.query.all()
    return payments


def payment_create(**kwargs):
    """
    Create a new payment.
    """
    new_payment = Pago(**kwargs)
    commit_db(new_payment)
    return new_payment


def payment_update(id: int, params):
    """
    Update a payment.
    """
    payment = search_by_id(id)
    update_payment(payment, params)
    commit_db(payment)
    return payment


def search_by_id(id: int):
    """
    Search a payment by id.
    """
    payment = Pago.query.filter_by(id=id).first()
    return payment


def payments_by_month(year: int):
    """
    Return all payments of the current year grouped by month.
    """
    payments = Pago.query.filter(
        extract('year', Pago.fecha_pago) == year
    ).all()

    payments_by_month = {}
    for payment in payments:
        month = payment.fecha_pago.strftime("%B")
        if month not in payments_by_month:
            payments_by_month[month] = []
        payments_by_month[month].append(payment)

    return payments_by_month
