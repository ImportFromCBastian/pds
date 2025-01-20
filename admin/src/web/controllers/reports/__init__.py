from flask import Blueprint, render_template
from src.core.models import riders as riders_module
from src.core.models.charges_module.charge import Cobro
from src.core.models import teams as teams_module
from src.core.models import payments as payments_module
from src.core.models import equestrian as equestrian_module
from src.core.models.equestrian.Horse import Sede, JyAType
from src.core.models.teams.employee import ConditionType
from src.core.models.payments.payment import PaymentType
from src.core.models.riders.rider import PropuestaTrabajo
from src.web.controllers.reports.utils import get_job_count_by_rider, get_payment_count, get_active_members_by_conditions, get_active_horses_by_sede_and_activity
from src.web.handlers.auth import login_and_permission_required

bp = Blueprint('reports', __name__, url_prefix='/reportes')


@bp.get('/')
@login_and_permission_required("report_index")
def index():
    riders_debt = Cobro.get_loans()
    riders = riders_module.rider_index()
    teams = teams_module.team_index()
    payments = payments_module.payment_index()
    horses = equestrian_module.equestrian_index()

    riders_job_count = get_job_count_by_rider(riders)
    payments_count = get_payment_count(payments)
    active_members = get_active_members_by_conditions(teams)
    active_horses = get_active_horses_by_sede_and_activity(horses)

    return render_template("reports/index.html", riders_debt=riders_debt, job_count=riders_job_count, payments_count=payments_count, active_members=active_members, active_horses=active_horses, sedes=Sede, activities=JyAType, conditions=ConditionType, payment_types=PaymentType, job_types=PropuestaTrabajo)
