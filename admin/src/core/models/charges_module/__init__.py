from src.core.models.charges_module.charge import Cobro
from src.core.models.teams import Empleado
from src.core.models.riders import Equitador
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import aliased
from datetime import datetime


def get_charges_filtered(
    page: int = 1,
    per_page: int = 5,
    sort_order: str = "desc",
    start_date: datetime = None,
    end_date: datetime = None,
    pay_method: str = None,
    name_rcp: str = None,
    surname_rcp: str = None
):
    """Returns charges filtered by a range of date (start_date and end_date), pay method, name and 
    surname of the recipient, ordered by pay date and a given order, paginated in "per_page" charges (5 by default).
    Receives the page to render (1 by default), the sort order (descendent by default), and optionally 
    the range of date, the pay method, the name and the surname of the recipient"""

    EmpleadoAlias = aliased(Empleado)
    EquitadorAlias = aliased(Equitador)

    charges = (
        Cobro.query.filter_by(borrado=False)
        .join(Cobro.empleado.of_type(EmpleadoAlias))
        .join(Cobro.equitador.of_type(EquitadorAlias))
    )

    if start_date:
        charges = charges.filter(Cobro.fecha_pago >= start_date)

    if end_date:
        charges = charges.filter(Cobro.fecha_pago <= end_date)

    if pay_method:
        charges = charges.filter(Cobro.medio_de_pago == pay_method)

    if name_rcp:
        charges = charges.filter(EmpleadoAlias.nombre.like(f"%{name_rcp}%"))

    if surname_rcp:
        charges = charges.filter(
            EmpleadoAlias.apellido.like(f"%{surname_rcp}%"))

    if sort_order == "desc":
        charges = charges.order_by(Cobro.fecha_pago.desc())
    else:
        charges = charges.order_by(Cobro.fecha_pago.asc())

    paginated_charges = charges.paginate(page=page, per_page=per_page)

    return paginated_charges
