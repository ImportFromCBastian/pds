from src.core.models import Permiso


def create_permissions():
    """
    Create permissions for the team module.
    """
    permisson1 = Permiso.create_permission(nombre="team_index")
    permisson2 = Permiso.create_permission(nombre="team_new")
    permisson3 = Permiso.create_permission(nombre="team_submit_files")
    permisson4 = Permiso.create_permission(nombre="team_update")
    permisson5 = Permiso.create_permission(nombre="team_show")
