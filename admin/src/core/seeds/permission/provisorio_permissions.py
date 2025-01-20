from src.core.models import Permiso


def create_permissions():
    """
    Create permissions for the users provisorios module.
    """
    permisson1 = Permiso.create_permission(nombre="provisorio_index")
    permisson2 = Permiso.create_permission(nombre="provisorio_new")
