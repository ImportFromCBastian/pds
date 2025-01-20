from flask import render_template, request, redirect, url_for, flash, Blueprint
from src.web.handlers.auth import login_and_permission_required
from src.core.models.charges_module import get_charges_filtered
from src.core.models.charges_module.charge import Cobro
from src.core.models.charges_module.charge import PayMethod
from src.core.models.riders import Equitador
from src.core.models.riders import riders_index
from src.core.models.teams import team_index
from datetime import datetime
from src.web.controllers.charges_module.handlers.validators.validator import validate_charge, validate_partial_charge

bp = Blueprint("modulo_cobros", __name__, url_prefix="/modulo_cobros")


@bp.route("/listado", methods=["GET", "POST"])
@login_and_permission_required("charge_index")
def listado():
    """Shows all the charges in pages"""

    sort_order = request.args.get("sort_order", "desc")
    page = request.args.get('page_receive', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    start_date = request.args.get("start_date", None)
    end_date = request.args.get("end_date", None)
    pay_method = request.args.get("pay_method", None)
    name_rcp = request.args.get("name_rcp", None)
    surname_rcp = request.args.get("surname_rcp", None)

    if start_date:
        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        except ValueError as e:
            flash(f'Ingrese una fecha en un formato válido para filtrar por la misma', "error")
            start_date = None

    if end_date:
        try:
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError as e:
            flash(f'Ingrese una fecha en un formato válido para filtrar por la misma', "error")
            end_date = None

    if pay_method == "None":
        pay_method = None

    charges = get_charges_filtered(
        page=page,
        per_page=per_page,
        sort_order=sort_order,
        start_date=start_date,
        end_date=end_date,
        pay_method=pay_method,
        name_rcp=name_rcp,
        surname_rcp=surname_rcp,
    )

    return render_template(
        "charges_module/index.html",
        page=page,
        charges=charges,
        current_sort_column="fecha_de_pago",
        current_sort_order=sort_order,
        pay_methods=PayMethod,
    )


@bp.route("/registrar_cobro", methods=["GET", "POST"])
@login_and_permission_required("charge_create")
def registrar_cobro():
    """Register a charge"""

    if request.method == "GET":
        riders = riders_index()
        employees = team_index()
        return render_template("charges_module/register.html", pay_methods=PayMethod, riders=riders, employees=employees)

    else:

        data = request.form.to_dict()
        is_valid = validate_charge(data)

        if not is_valid["valid"]:
            for error in is_valid["errors"]:
                flash(f'{error["msg"]}', "error")
        
        else:
            created_charge = Cobro.create_charge(
                dni_equitador=data.get("dni_equitador"),
                fecha_pago=data.get("fecha_de_pago"),
                medio_de_pago=data.get("medio_de_pago"),
                monto=data.get("monto"),
                dni_empleado=data.get("dni_empleado"),
                observaciones=data.get("observaciones") or " ",
            )

            if created_charge:
                flash(f"El Cobro ha sido registrado con exito", "success")
            else:
                flash(f"El Cobro no ha sido registrado debido a un error inesperado", "error")

        return redirect(
            url_for("modulo_cobros.listado")
        )


@bp.route("/actualizar_cobro/<id>", methods=["GET", "POST"])
@login_and_permission_required("charge_update")
def actualizar_cobro(id: int):
    """Modifies the info of the charge sended"""
    charge = Cobro.get_charge(id)

    if request.method == "GET":
        riders = riders_index()
        employees = team_index()
        return render_template(
            "charges_module/index_update.html", charge=charge, pay_methods=PayMethod, riders=riders, employees=employees
        )

    elif request.method == "POST":

        data = request.form.to_dict()    
        is_valid = validate_partial_charge(data)

        if not is_valid["valid"]:
            for error in is_valid["errors"]:
                flash(f'{error["msg"]}', "error")

        else: 
            changed = charge.update_charge(**data)

            if changed != {}:
                flash(f"Se actualizaron los datos del cobro", "info")
            else:
                flash(f"No se actualizaron los datos en el cobro", "info")

        return redirect(
            url_for("modulo_cobros.listado")
        )


@bp.route("/cambiar_estado_jya/<dni>", methods=["GET", "POST"])
@login_and_permission_required("charge_update")
def cambiar_estado_jya(dni: int):
    """Togles the rider status in his pays"""
    if Equitador.togle_pay_status(dni):
        if Equitador.tiene_deudas:
            flash(f"Se marcó al J&A con DNI {dni} con deudas de pagos", "info")
        else:
            flash(f"Se marcó al J&A con DNI {
                  dni} al día con los pagos", "info")
    else:
        flash(f"No se pudo cambiar el estado de pagos al J&A con DNI {
              dni}", "error")
    return redirect(url_for("modulo_cobros.checkear_estado_jya", page_receive=0))


@bp.route("/eliminar_cobro/<id>", methods=["GET", "POST"])
@login_and_permission_required("charge_destroy")
def eliminar_cobro(id: int):
    """Deletes a charge permanently"""
    if Cobro.delete_charge(id):
        flash(f"Se elimino el cobro", "info")
    else:
        flash(f"No se pudo eliminar el cobro", "error")
    return redirect(url_for("modulo_cobros.listado"))


@bp.route("/mostrar_cobro/<id>", methods=["GET", "POST"])
@login_and_permission_required("charge_show")
def mostrar_cobro(id: int):
    """Shows the info of the charge sended"""
    charge = Cobro.get_charge(id)

    return render_template("charges_module/index_show.html", charge=charge)


@bp.post("/saldar_cobro/<id>")
def saldar_cobro(id: int):
    """Pays a charge"""
    Cobro.pay_charge(id)
    flash(f"Se saldó el cobro", "info")
    return redirect(url_for("modulo_cobros.listado"))
