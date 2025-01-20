from src.core.database import db
from datetime import datetime
import enum


class PaymentType(enum.Enum):
    """
    Enum for the type of  a payment.
    """

    honorario = "Honorarios"
    proveedor = "Proveedor"
    gastos_varios = "Gastos varios"


class Pago(db.Model):
    """
    A payment made to a beneficiary.
    """

    __tablename__ = "Pago"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    beneficiario = db.Column(
        db.BigInteger(), db.ForeignKey("Empleado.dni"), nullable=False
    )
    employee = db.relationship(
        "Empleado"
    )
    monto = db.Column(db.Float, nullable=False)
    fecha_pago = db.Column(db.DateTime, nullable=False)
    tipo_pago = db.Column(db.Enum(PaymentType), nullable=False)
    descripcion = db.Column(db.String(100), default="")
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(
        db.DateTime, default=datetime.now(), onupdate=datetime.now())

    def __repr__(self):
        return (
            f"<Pago id='{self.id}', "
            f"beneficiario='{self.beneficiario}', "
            f"monto='{self.monto}', "
            f"fecha_pago='{self.fecha_pago}', "
            f"tipo_pago='{self.tipo_pago}', "
            f"descripcion='{self.descripcion}', "
            f"created_at='{self.created_at}', "
            f"updated_at='{self.updated_at}'>"
        )
