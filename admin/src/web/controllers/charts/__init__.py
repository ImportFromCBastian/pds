from src.web.handlers.auth import login_and_permission_required
from flask import Blueprint, render_template
from src.core.models import teams
from src.core.models import payments
from src.core.models import riders
from datetime import date
from src.web.controllers.charts.utils import generate_bar_chart_img
from src.core.models.teams.employee import ProfessionType


bp = Blueprint('charts', __name__, url_prefix='/estadisticas')


@bp.get('/')
@login_and_permission_required('chart_index')
def index():
    current_year = date.today().year
    last_year = date.today().year - 1

    # Total de empleados por profesión:
    team = teams.team_index()
    professions = [profession.value for profession in ProfessionType]
    counts = [len([member for member in team if member.profesion == profession])
              for profession in ProfessionType]
    total_professions = generate_bar_chart_img(
        professions, counts, "Cantidad", "Cantidad de empleados por profesión")

    # Total de ingresos por Jinetes y Amazonas:
    riders_last_year_earned = riders.rider_charges(last_year, current_year)
    total_earnings = None
    if riders_last_year_earned:
        x_riders = [f"{rider.dni} - {rider.nombre}"
                    for rider in riders_last_year_earned]
        earnings = [rider.total_monto for rider in riders_last_year_earned]
        total_earnings = generate_bar_chart_img(
            x_riders, earnings, "Total ganado en un año", "Ingresos por Jinetes y Amazonas")

    # Total de pagos realizados por mes:
    payments_by_month = payments.payments_by_month(current_year)
    total_payments = None

    if payments_by_month:
        months = list(payments_by_month.keys())
        counts = [len(payments_by_month[month]) for month in months]
        total_payments = generate_bar_chart_img(
            months, counts, "Cantidad", "Cantidad de pagos por mes")

    return render_template("charts/index.html", profession_chart=total_professions, payments_chart=total_payments, charges_chart=total_earnings)
