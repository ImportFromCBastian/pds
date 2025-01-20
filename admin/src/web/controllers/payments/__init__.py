from flask import Blueprint, render_template, request, redirect, url_for, flash
from src.core.models.payments.payment import PaymentType
from src.core.models import teams
from src.core.models import payments as payments_module
from src.web.handlers.auth import login_and_permission_required
from src.web.controllers.payments.handlers.validators.validator import (
    validate_payment,
    validate_partial_payment,
)
from src.web.controllers.payments.handlers.search import filter_payments, apply_order

bp = Blueprint("payments", __name__, url_prefix="/equipo/pagos")


@bp.get("/")
@login_and_permission_required("payment_index")
def index():
    """
    Returns all payments.
    """
    payment = payments_module.payment_index()
    args = request.args.to_dict()

    page = int(args.get("page", 1))
    per_page = int(args.get("per_page") if args.get("per_page") else 5)

    if args:

        filtered_payments = filter_payments(payment, args, page, per_page)
        pagination = filtered_payments["pagination"]
        payments = filtered_payments["payments"]

        if len(payments) == 0:
            return render_template(
                "payments/index.html",
                payments=payments,
                pagination=pagination,
                payment_type=PaymentType,
                empty=True,
                args=args
            )

        order = args.get("sort_order", "desc")
        payments = apply_order(payments, order)

        return render_template(
            "payments/index.html", payments=payments, pagination=pagination, payment_type=PaymentType, args=args
        )

    payment_filtered = filter_payments(
        payments_module.payment_index(), {}, page, per_page)
    pagination = payment_filtered["pagination"]
    payment = payment_filtered["payments"]
    return render_template(
        "payments/index.html",
        payments=payment,
        payment_type=PaymentType,
        pagination=pagination,
        args={"sort_order": "desc"},
    )


@bp.get("/agregar")
@login_and_permission_required("payment_new")
def new():
    """
    returns the form of a new payment.
    """
    team = teams.team_index()
    return render_template(
        "payments/new.html", payment_type=PaymentType, team=team, errors={}
    )


@bp.post("/agregar")
@login_and_permission_required("payment_new")
def create():
    """
    Creates a new payment.
    """
    body = request.form

    is_valid = validate_payment(body)
    team = teams.team_index()

    errors = {}
    if not is_valid["valid"]:
        for error in is_valid["errors"]:
            field = error["loc"][0]
            errors[field] = error["msg"]
        return render_template(
            "payments/new.html",
            payment_type=PaymentType,
            team=team,
            errors=errors,
        )
    try:
        payment = payments_module.payment_create(**body)
    except Exception as e:
        return f"Error creating team member: {str(e)}", 500
    flash("Pago creado con éxito", "success")
    return redirect(url_for("payments.index"))


@bp.get("/editar/<int:id>")
@login_and_permission_required("payment_update")
def edit(id):
    """
    Returns the form to edit a payment.
    """
    payment = payments_module.search_by_id(id)
    return render_template(
        "payments/edit.html", payment=payment, payment_type=PaymentType, errors={}
    )


@bp.post("/editar/<int:id>")
@login_and_permission_required("payment_update")
def update(id):
    """
    Updates a payment.
    """
    body = request.form.to_dict()
    payment = payments_module.search_by_id(id)

    is_valid = validate_partial_payment(body)

    if not is_valid["valid"]:
        errors = {}
        for error in is_valid["errors"]:
            field = error["loc"][0]
            errors[field] = error["msg"]
        return render_template(
            "payments/edit.html",
            payment=payment,
            payment_type=PaymentType,
            errors=errors,
        )

    payments_module.payment_update(id, body)

    payment = payments_module.payment_index()
    return render_template(
        "payments/index.html",
        payments=payment,
        payment_type=PaymentType,
        success="Pago actualizado con éxito",
        args={"sort_order": "desc"},
    )
