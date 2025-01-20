from src.core.models.teams.employee import Empleado
from src.core.database import commit_db
from src.core.models.teams.handlers.update_member import update as update_member
from src.web.controllers.teams.handlers.files.constant import File_Names


def team_index():
    """
    List all the team members, optionally sorted by a given field and order.
    """
    team_members = Empleado.query.all()
    return team_members


def team_create(**kwargs):
    """
    Create a new team member.
    """
    new_team_member = Empleado(**kwargs)
    commit_db(new_team_member)
    return new_team_member


def team_update(dni: int, params):
    """
    Update a team member.
    """
    team_member = search_by_dni(dni)
    update_member(team_member, params)
    commit_db(team_member)
    return team_member


def search_by_email(email: str):
    """
    Search a team member by email
    """
    team_member = Empleado.query.filter_by(email=email).first()
    return team_member


def search_by_dni(dni: int):
    """
    Search a team member by dni
    """
    team_member = Empleado.query.filter_by(dni=dni).first()
    return team_member


def search_by_number(number: int):
    """
    Search a team member by number
    """
    team_member = Empleado.query.filter_by(numero_afiliado=number).first()
    return team_member


def search_by_job_position(job_position: str):
    """
    Search a team member by job position
    """
    team_member = Empleado.query.filter_by(puesto_laboral=job_position).all()
    return team_member


def upload_file(file_name, extension, dni):
    """
    Uploads the files to the model
    """
    member = Empleado.query.filter_by(dni=dni).first()

    setattr(member, file_name, f"{file_name}.{extension}")
    commit_db(member)
    return member


def get_files_by_dni(dni: int):
    """
    Get the files of a team member by dni
    """
    member = search_by_dni(dni)
    files = {"curriculum_vitae": None, "copia_dni": None, "titulo": None}
    for file_name in File_Names:
        files[file_name] = getattr(member, file_name)
    return files
