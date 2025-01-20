from src.core.database import db
from src.core.models.riders import Equitador
from src.core.models.teams import Empleado
from datetime import datetime
from sqlalchemy import func
import enum


class PayMethod(enum.Enum):
    """Enumerate pay methods"""
    TarjetaDeCredito = "Tarjeta de Credito"
    TarjetaDeDebito = "Tarjeta de Debito"
    Efectivo = "Efectivo"
    Honorarios = "Honorarios"
    Proveedor = "Proveedor"
    GastosVarios = "Gastos Varios"


class Cobro(db.Model):
    """A charge that represents a payment from a rider to an employee."""
    __tablename__ = "Cobro"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dni_equitador = db.Column(db.BigInteger, db.ForeignKey(
        "Equitador.dni"), nullable=False)
    equitador = db.relationship("Equitador", back_populates="cobros")
    fecha_pago = db.Column(db.DateTime, default=datetime.now())
    medio_de_pago = db.Column(db.Enum(PayMethod), nullable=False)
    monto = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    dni_empleado = db.Column(db.BigInteger, db.ForeignKey(
        "Empleado.dni"), nullable=False)
    empleado = db.relationship("Empleado", back_populates="cobros")
    observaciones = db.Column(db.String, nullable=True)
    inserted_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(
        db.DateTime, default=datetime.now(), onupdate=datetime.now())
    borrado = db.Column(db.Boolean, nullable=True, default=False)

    @classmethod
    def create_charge(cls, **kwargs):
        """
        Add a charge by sending the parameters and types below:
            dni_equitador: Integer
            fecha_pago: Date
            medio_de_pago: String
            monto: Real
            dni_empleado: Integer
            observaciones: String
        Finally, returns the charge.
        """
        charge = cls(**kwargs)
        db.session.add(charge)
        db.session.commit()
        return charge

    @classmethod
    def get_charge(cls, id: int):
        """Search the charge for the id sended"""
        return cls.query.filter_by(borrado=False).filter(cls.id == id).first()

    @classmethod
    def delete_charge(cls, id: int) -> bool:
        """Deletes the charge for the id sended, and returns if it was deleted or not"""
        charge = cls.get_charge(id)

        if charge:
            charge.borrado = True
            db.session.commit()
            return True
        else:
            return False

    def update_charge(self, **kwargs):
        """Updates the charge with the given data. Returns a dictionary with the data
        changed and a report of errors if they existed"""
        changed = {}
        for attribute, value in kwargs.items():
            match attribute:
                case "dni_equitador":
                    self.dni_equitador = value
                    changed[attribute] = value

                case "dni_empleado":
                    self.dni_empleado = value
                    changed[attribute] = value

                case "fecha_pago":
                    if value != "":
                        self.fecha_pago = value
                        changed[attribute] = value

                case "medio_de_pago":
                    self.medio_de_pago = value
                    changed[attribute] = value

                case "monto":
                    self.monto = value
                    changed[attribute] = value

                case "observaciones":
                    if value != self.observaciones:
                        self.observaciones = value
                        changed[attribute] = value
                        
        db.session.commit()
        return changed

    @classmethod
    def pay_charge(cls, id: int):
        """Pays the charge for the id sended"""
        charge = cls.get_charge(id)
        charge.monto = charge.monto * -1
        db.session.commit()
        return charge

    @classmethod
    def get_loans(cls):
        """Retrieve grouped charges with equitador information and total amounts."""
        charges = (
            cls.query
            .with_entities(
                cls.dni_equitador,
                Equitador.nombre,
                Equitador.apellido,
                func.sum(cls.monto).label('total_monto')
            )
            .join(Equitador, Equitador.dni == cls.dni_equitador)
            .filter(cls.borrado == False, Equitador.borrado == False, cls.monto < 0)
            .group_by(
                cls.dni_equitador,
                Equitador.nombre,
                Equitador.apellido
            )
            .all()
        )
        return charges
