from src.core.models import payments


def create_payments():
    """
    Create a new payment for the employees.
    """
    payment1 = payments.payment_create(
        beneficiario=96186620,
        monto=10000,
        fecha_pago="2021-01-01",
        tipo_pago="honorario",
        descripcion="Pago de honorarios",
    )

    payment2 = payments.payment_create(
        beneficiario=2,
        monto=5000,
        fecha_pago="2021-01-01",
        tipo_pago="proveedor",
        descripcion="Pago a proveedor",
    )
