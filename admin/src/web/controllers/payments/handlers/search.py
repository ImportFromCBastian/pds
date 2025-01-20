from datetime import datetime
from src.core.models.payments.payment import PaymentType
from math import ceil


from datetime import datetime
from src.core.models.payments.payment import PaymentType


def filter_payments(payments, filters, page=1, per_page=5):
    """
    Filter a list of payments based on filters for employee DNI, payment date range, and payment type.

    :param payments: List of payments
    :param filters: Dictionary with filter parameters
    :return: Filtered list of payments.
    """

    def apply_filter(payment, key, value):
        """
        Apply a single filter to a payment.
        """
        if key == "beneficiario" and value:
            try:
                return payment.employee.dni == int(value)
            except ValueError:
                return False

        # Handle date range filter
        if key == "fecha_pago_desde" and value:
            return payment.fecha_pago >= datetime.strptime(value, "%Y-%m-%d")
        if key == "fecha_pago_hasta" and value:
            return payment.fecha_pago <= datetime.strptime(value, "%Y-%m-%d")

        if key == "tipo_pago" and value:
            return payment.tipo_pago == PaymentType[value]

        return True

    filtered_payments = [
        payment
        for payment in payments
        if all(apply_filter(payment, key, value) for key, value in filters.items())
    ]

    total_items = len(filtered_payments)
    total_pages = ceil(total_items / per_page)
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    paginated_payments = filtered_payments[start_index:end_index]

    pagination_metadata = {
        "pages": page,
        "per_page": per_page,
        "total_items": total_items,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1,
        "next_num": page + 1 if page < total_pages else None,
        "prev_num": page - 1 if page > 1 else None,
        "item": len(paginated_payments),
    }

    return {
        "payments": paginated_payments,
        "pagination": pagination_metadata,
    }


def apply_order(payments, order):
    """
    Apply an order to a list of payments based on the payment date.

    :param payments: List of payments
    :param order: Order direction
    :return: Ordered list of payments.
    """
    if order == "asc":
        payments.sort(key=lambda x: x.fecha_pago)
    else:
        payments.sort(key=lambda x: x.fecha_pago, reverse=True)

    return payments
