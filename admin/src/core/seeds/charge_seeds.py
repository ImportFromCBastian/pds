from src.core.models.charges_module.charge import Cobro
from src.core.models.charges_module.charge import PayMethod
from datetime import datetime


def create_charges():
    cobro1 = Cobro.create_charge(
        dni_equitador=12345678,
        fecha_pago=datetime.now(),
        medio_de_pago=PayMethod.TarjetaDeCredito,
        monto=5000,
        dni_empleado=96186620,
        observaciones=" "
    )

    return cobro1
