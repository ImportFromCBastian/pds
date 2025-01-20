from src.core.models.riders.rider import PropuestaTrabajo
from src.core.models.payments.payment import PaymentType
from src.core.models.teams.employee import ConditionType
from src.core.models.equestrian.Horse import Sede, JyAType


def get_job_count_by_rider(riders):
    """
    Returns a dictionary with the count of riders for each job in PropuestaTrabajo.
    """

    job_counts = {
        institutional_job: sum(
            1 for rider in riders if rider.trabajo_institucional.tipo_trabajo == institutional_job)
        for institutional_job in PropuestaTrabajo
    }

    return sort(job_counts)


def get_payment_count(payments):
    """
    Returns a dictionary with the count of payments for each payment method.
    """

    payment_counts = {
        payment_method: sum(
            1 for payment in payments if payment.tipo_pago == payment_method)
        for payment_method in PaymentType
    }

    return sort(payment_counts)


def get_active_members_by_conditions(teams):
    """
    Returns the count of active members in the teams by condition type.
    """
    active_members = {
        condition_type: sum(
            1 for team in teams if team.activo)
        for condition_type in ConditionType
    }

    return sort(active_members)


def get_active_horses_by_sede_and_activity(horses):
    """
    Returns the count of active horses by sede and activity.
    """
    active_horses = {
        sede: {
            activity: sum(
                1 for horse in horses if horse.sede_asignada == sede and horse.tipo_de_JyA_asignado == activity)
            for activity in JyAType
        }
        for sede in Sede
    }

    for sede in active_horses:
        active_horses[sede] = sort(active_horses[sede])
    return active_horses


def sort(list):
    """
    Sorts a dictionary by its values in descending order.
    """
    return dict(
        sorted(list.items(), key=lambda item: item[1], reverse=True))
